import json
import copy
import os
import sys
import time
import subprocess
import signal
import random
import exe
import numpy

node_list = {'172.17.1.119': 'example', '172.17.1.60': 'example'}

benchmark_set = 'mixedbenchmark'
if len(sys.argv) > 1:
    benchmark_set = sys.argv[1]
else:
    print('Microbench name needed')
    exit(0)

bound = {'redis': [3, 60, 3]}


test_time = 60
if '-t' in sys.argv:
    test_time = int(sys.argv[sys.argv.index('-t') + 1])


repeat_time = 5
if '-r' in sys.argv:
    repeat_time = int(sys.argv[sys.argv.index('-r') + 1])

background = ''
if '-b' in sys.argv:
    background = sys.argv[sys.argv.index('-b') + 1]

benchmark_list = ['redis']

benchmark = 'redis'
for index in range(len(node_list.keys())):
    exe.cmd_and_wait('rm -rf %s_tail_latency%d.txt' % (benchmark, index))
    exe.cmd_and_wait('rm -rf %s_count%d.txt' % (benchmark, index))
    exe.cmd_and_wait('rm -rf %s_throughput%d.txt' % (benchmark, index))

for rps in numpy.arange(bound[benchmark][0], bound[benchmark][1] + bound[benchmark][2], bound[benchmark][2]):
    total_sum = [0] * len(node_list.keys())
    total_len = [0] * len(node_list.keys())
    throughput_sum = [0] * len(node_list.keys())
    throughput_len = [0] * len(node_list.keys())
    for n in range(repeat_time):
        exe.cmd_and_wait('docker network rm scomet')
        exe.cmd_and_wait('docker network create -d overlay  --attachable scomet')
        for index in range(len(node_list.keys())):
            ip = node_list.keys()[index]
            exe.cmd_and_wait('sshpass -p \'%s\' ssh root@%s "docker stop container%d"' %(node_list[ip], ip, index))
            exe.cmd_and_wait('sshpass -p \'%s\' ssh root@%s "docker rm container%d"' % (node_list[ip], ip, index))
            exe.cmd_and_wait('sshpass -p \'%s\' ssh root@%s "systemctl stop firewalld"' % (node_list[ip], ip))
            exe.cmd_and_wait(
                'sshpass -p \'%s\' ssh root@%s "docker run -v /home/wjy/SComet:/home/wjy/SComet -id --privileged --name container%d --net=scomet scomet /bin/bash"' % (
                node_list[ip], ip, index))
            if background:
                exe.cmd_and_wait('sshpass -p \'%s\' ssh root@%s "docker stop be_container%d"' % (node_list[ip], ip, index))
                exe.cmd_and_wait('sshpass -p \'%s\' ssh root@%s "docker rm be_container%d"' % (node_list[ip], ip, index))
                exe.cmd(
                    'sshpass -p \'%s\' ssh root@%s "docker run -v /home/wjy/SComet:/home/wjy/SComet -id --privileged --name be_container%d scomet sh -c \\\"sh /home/wjy/SComet/%s/script/%s.sh\\\""' % (
                    node_list[ip], ip, index, benchmark_set, background))


        master_ip = list(node_list.keys())[0]
        exe.cmd_and_wait('sshpass -p \'%s\' ssh root@%s "docker exec container0 sh -c \\\"sh /home/wjy/SComet/%s/script/redis-master.sh\\\""' % (node_list[master_ip], master_ip, benchmark_set))
        output, err = exe.cmd_and_wait(
            'sshpass -p \'%s\' ssh root@%s "docker exec container0 ifconfig"' % (
                node_list[master_ip], master_ip))
        for index in range(len(output)):
            if 'eth0' in output[index]:
                host = output[index + 1].split()[1]
        print(host)

        for index in range(1, len(node_list.keys())):
            ip = node_list.keys()[index]
            exe.cmd_and_wait(
                'sshpass -p \'%s\' ssh root@%s "docker exec container%d sh -c \\\"sh /home/wjy/SComet/%s/script/redis-slave.sh %s\\\""' % (
                node_list[ip], ip, index, benchmark_set, host))
        time.sleep(60)

        cmd_result = exe.cmd(
            'sshpass -p \'%s\' ssh root@%s "docker exec container0 sh -c \\\"sh /home/wjy/SComet/%s/script/redis-master-cli.sh 20 %d\\\""' % (
            node_list[master_ip], master_ip, benchmark_set, int(rps)))

        for index in range(1, len(node_list.keys())):
            ip = node_list.keys()[index]
            exe.cmd(
                'sshpass -p \'%s\' ssh root@%s "docker exec container%d sh -c \\\"sh /home/wjy/SComet/%s/script/redis-slave-cli.sh 20 %d\\\""' % (
                node_list[ip], ip, index, benchmark_set, int(rps)))

        if test_time <= 0:
            cmd_result.wait()
        else:
            time.sleep(test_time)
            print('%d second passed...' % test_time)
        log_path = ['/home/wjy/SComet/%s/QoS/%s.log' % (benchmark_set, benchmark), '/home/wjy/SComet/%s/QoS/%s_2.log' % (benchmark_set, benchmark)]
        for index in range(len(node_list.keys())):
            ip = node_list.keys()[index]
            exe.cmd_and_wait('sshpass -p \'%s\' ssh root@%s \'docker cp container%d:%s %s\'' % (node_list[ip], ip, index, log_path[0], log_path[0]))
            exe.cmd_and_wait('sshpass -p \'%s\' scp root@%s:%s %s' % (node_list[ip], ip, log_path[0], log_path[index]))

        for index in range(len(node_list.keys())):
            ip = node_list.keys()[index]
            exe.cmd_and_wait('sshpass -p \'%s\' ssh root@%s docker stop container%d' % (node_list[ip], ip, index))
            exe.cmd_and_wait('sshpass -p \'%s\' ssh root@%s docker rm container%d' % (node_list[ip], ip, index))
            exe.cmd_and_wait('sshpass -p \'%s\' ssh root@%s "echo \"y\" | docker system prune"' % (node_list[ip], ip))

        output = []
        throughput = []
        for index in range(len(node_list.keys())):
            output.append([])
            throughput .append([])
            with open(log_path[index], mode='r') as log_f:
                logs = log_f.readlines()
                for log in logs:
                    if '99.00th percentile latency' in log and '99.99th percentile latency' not in log:
                        output[index].append(float(log.split()[-1]))
                    if 'throughput summary' in log:
                        throughput[index].append(float(log.split()[2]))
            total_sum[index] += sum(output[index])
            total_len[index] += len(output[index])
            throughput_sum[index] += sum(throughput[index])
            throughput_len[index] += len(throughput[index])
        print(output)
        print(throughput)

    for index in range(len(node_list.keys())):
        curr_return = total_len[index] * 1.0 / repeat_time
        with open('%s_count%d.txt' % (benchmark, index), mode='a') as result_f:
            if total_len[index] == 0:
                result_f.write('0 ')
            else:
                result_f.write(str(curr_return))
                result_f.write(' ')
        with open('%s_tail_latency%d.txt' % (benchmark, index), mode='a') as result_f:
            if total_len[index] == 0:
                result_f.write('0 ')
            else:
                result_f.write(str(total_sum[index] / total_len[index]))
                result_f.write(' ')
        with open('%s_throughput%d.txt' % (benchmark, index), mode='a') as result_f:
            if throughput_len[index] == 0:
                result_f.write('0 ')
            else:
                result_f.write(str(throughput_sum[index] / throughput_len[index]))
                result_f.write(' ')



 


