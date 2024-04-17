import json
import copy
import os
import sys
import time
import subprocess
import signal
import random
import exe

LC_TASKS = ['memcached', 'nginx', 'masstree', 'silo', 'redis-cli', 'redis-server']

if len(sys.argv) > 1:
    benchmark_set = sys.argv[1]
else:
    print('Microbench name needed')
    exit(0)

event_set = '/home/wjy/SComet/extracted_list/ocperf_list_extracted_basic0.txt'
if '-e' in sys.argv:
    event_set = sys.argv[sys.argv.index('-e') + 1]
    print('event set: %s' % event_set)
event_set_name = event_set.split('/')[-1]

test_time = 60
if '-t' in sys.argv:
    test_time = int(sys.argv[sys.argv.index('-t') + 1])

specific_benchmark = ''
if '--benchmark' in sys.argv:
    specific_benchmark = sys.argv[sys.argv.index('--benchmark') + 1]

benchmark_list = []
for root, dirs, files in os.walk('./'+ benchmark_set +'/script'):
    for file in files:
        if file.split('.')[-1] == 'sh' and '.'.join(file.split('.')[0:-1]) not in LC_TASKS:
            benchmark_list.append('.'.join(file.split('.')[0:-1]))
if specific_benchmark in benchmark_list:
    benchmark_list = [specific_benchmark]
benchmark_list.sort()
print('benchmark list:')
print(benchmark_list)

for benchmark in benchmark_list:

    exe.cmd_and_wait('touch %s/log/%s_%s.log' % (benchmark_set, benchmark, event_set_name))
    exe.cmd_and_wait('rm -rf %s/log/%s_%s.log' % (benchmark_set, benchmark, event_set_name))
    exe.cmd_and_wait('echo 0 > /proc/sys/kernel/nmi_watchdog')
    exe.cmd_and_wait('export PATH=$PATH:/home/wjy/pmu-tools')
    exe.cmd_and_wait('docker stop container')
    exe.cmd_and_wait('docker rm container')
    exe.cmd_and_wait('docker run -id -v /home/wjy/SComet:/home/wjy/SComet --privileged --name container scomet /bin/bash')

    instr = 'ocperf stat -a'
    with open(event_set, mode='r') as pmu_events_f:
        pmu_events = pmu_events_f.readlines()
    for pmu_event in pmu_events:
        pmu_event_tuple = pmu_event.split()
        if pmu_event_tuple:
            instr = instr + ' -e ' + pmu_event_tuple[0]

    instr = instr + ' -o ' + '%s/log/%s_%s.log' % (benchmark_set, benchmark, event_set_name)
    instr = instr + ' docker exec container sh -c "sh /home/wjy/SComet/%s/script/%s.sh"' % (benchmark_set, benchmark)

    print(instr)
    print('waiting for perf...')
    cmd_result = exe.cmd(instr)
    if test_time <= 0:
        cmd_result.wait()
    else:
        time.sleep(test_time)
        print('%d second passed...' % test_time)
    exe.cmd_and_wait('docker stop container')
    exe.cmd_and_wait('docker rm container')
    exe.cmd_and_wait('echo "y" | docker system prune')
    exe.cmd_and_wait('echo 1 > /proc/sys/kernel/nmi_watchdog')

    with open('%s/log/%s_%s.log' % (benchmark_set, benchmark, event_set_name), 'r') as result_f:
        result_list = result_f.readlines()
    for result in result_list:
        if 'seconds time elapsed' in result:
            break
        result_tuple = result.split()
        if len(result_tuple) >= 2 and result_tuple[0] == '<not' and result_tuple[1] == 'counted>':
            continue
        elif len(result_tuple) >= 3 and result_tuple[1] == 'MiB':
            print(result_tuple[2].strip().ljust(50, ' ') + ' ' + result_tuple[0].strip() + ' ' + result_tuple[1].strip())
        elif len(result_tuple) >= 2:
            print(result_tuple[1].strip().ljust(50, ' ') + ' ' + result_tuple[0].strip())
 


