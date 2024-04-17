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

if len(sys.argv) > 1:
    benchmark_set = sys.argv[1]
else:
    print('Microbench name needed')
    exit(0)

bound = {'memcached': [500, 5000, 500], 'nginx': [20000, 60000, 4000], 'masstree': [400, 6000, 400], 'silo': [2000, 20000, 2000]}
# bound = {'memcached': [1000, 10000, 1000], 'nginx': [100000, 300000, 20000], 'masstree': [2000, 30000, 2000], 'silo': [1000, 10000, 1000]}

test_time = 60
if '-t' in sys.argv:
    test_time = int(sys.argv[sys.argv.index('-t') + 1])

threads = range(1,9)
if '-T' in sys.argv:
    threads = sys.argv[sys.argv.index('-T') + 1]
    threads = [int(num) for num in threads.split(',')]

repeat_time = 5
if '-r' in sys.argv:
    repeat_time = int(sys.argv[sys.argv.index('-r') + 1])

specific_benchmark = ''
if '--benchmark' in sys.argv:
    specific_benchmark = sys.argv[sys.argv.index('--benchmark') + 1]

benchmark_list = []
for root, dirs, files in os.walk('./'+ benchmark_set +'/script'):
    for file in files:
        if file.split('.')[-1] == 'sh' and file.split('.')[0] in bound.keys():
            benchmark_list.append('.'.join(file.split('.')[0:-1]))
if specific_benchmark in benchmark_list:
    benchmark_list = [specific_benchmark]
benchmark_list.sort()
print('benchmark list:')
print(benchmark_list)

for benchmark in benchmark_list:
    exe.cmd_and_wait('rm -rf %s_tail_latency.txt' % benchmark)
    exe.cmd_and_wait('rm -rf %s_count.txt' % benchmark)
    for thread in threads:
        max_return = 0
        for rps in numpy.arange(bound[benchmark][0], bound[benchmark][1] + bound[benchmark][2], bound[benchmark][2]):
            total_sum = 0
            total_len = 0
            for n in range(repeat_time):
                exe.cmd_and_wait('docker stop container')
                exe.cmd_and_wait('docker rm container')
                instr = 'docker run -v /home/wjy/SComet:/home/wjy/SComet -id --privileged --name container scomet sh -c "sh /home/wjy/SComet/%s/script/%s.sh %d %d"' % (
                benchmark_set, benchmark, int(rps), thread)
                print(instr)
                cmd_result = exe.cmd(instr)
                if test_time <= 0:
                    cmd_result.wait()
                else:
                    time.sleep(test_time)
                    print('%d second passed...' % test_time)
                log_path = '/home/wjy/SComet/%s/QoS/%s.log' % (benchmark_set, benchmark)
                if benchmark == 'memcached':
                    exe.cmd_and_wait('docker cp container:%s %s' % (log_path, log_path))
                elif benchmark == 'nginx':
                    result_path = '/home/wjy/SComet/wrk2/result.txt'
                    exe.cmd_and_wait('docker cp container:%s %s' % (result_path, log_path))
                elif benchmark == 'masstree' or benchmark == 'silo' or benchmark == 'sphinx':
                    result_path = '/home/wjy/SComet/tailbench/tailbench-v0.9/%s/lats.bin' % benchmark
                    exe.cmd_and_wait('docker cp container:%s %s' % (result_path, result_path))
                    exe.cmd_and_wait('python /home/wjy/SComet/tailbench/tailbench-v0.9/utilities/parselats.py %s' % result_path)
                    exe.cmd_and_wait('mv lats.txt %s' % log_path)
                exe.cmd_and_wait('docker stop container')
                exe.cmd_and_wait('docker rm container')
                exe.cmd_and_wait('echo "y" | docker system prune')
                output = []
                with open(log_path, mode='r') as log_f:
                    logs = log_f.readlines()
                    for log in logs:
                        if '99.00th percentile latency' in log and '99.99th percentile latency' not in log:
                            output.append(float(log.split()[-1]))
                print(output)
                total_sum += sum(output)
                total_len += len(output)
            curr_return = total_len * 1.0 / repeat_time
            if max_return < curr_return:
                max_return = curr_return
            with open('%s_count.txt' % benchmark, mode='a') as result_f:
                if total_len == 0:
                    result_f.write('0 ')
                else:
                    result_f.write(str(curr_return))
                    result_f.write(' ')
            with open('%s_tail_latency.txt' % benchmark, mode='a') as result_f:
                if total_len == 0:
                    result_f.write('0 ')
                else:
                    result_f.write(str(total_sum/ total_len))
                    result_f.write(' ')
        with open('%s_tail_latency.txt' % benchmark, mode='a') as result_f:
            result_f.write('\n')
        with open('%s_count.txt' % benchmark, mode='a') as result_f:
            result_f.write('\n')



 


