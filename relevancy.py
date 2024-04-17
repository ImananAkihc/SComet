import json
import copy
import os
import sys
import time
import subprocess
import signal
import random
import exe
from scipy.stats import pearsonr
import numpy as np

if len(sys.argv) > 1:
    benchmark_set = sys.argv[1]
else:
    print('Microbench name needed')
    exit(0)

test_time = 180
if '-t' in sys.argv:
    test_time = int(sys.argv[sys.argv.index('-t') + 1])

benchmark_list = []
for root, dirs, files in os.walk('./'+ benchmark_set +'/script'):
    for file in files:
        if file.split('.')[-1] == 'sh':
            benchmark_list.append('.'.join(file.split('.')[0:-1]))
benchmark_list.sort()
print('benchmark list:')
print(benchmark_list)

ipcs = {}

for benchmark in benchmark_list:
    exe.cmd_and_wait('echo 0 > /proc/sys/kernel/nmi_watchdog')
    exe.cmd_and_wait('docker run -id -v /home/wjy/SComet:/home/wjy/SComet --privileged --name container0 scomet /bin/bash')
    exe.cmd_and_wait('docker run -id -v /home/wjy/SComet:/home/wjy/SComet --privileged --name container1 scomet /bin/bash')
    instr0 = 'perf stat -a -o temp.log docker exec container0 sh -c "sh /home/wjy/SComet/microbenchmark/script/microbench.sh"'
    instr1 = 'docker exec container1 sh -c "sh /home/wjy/SComet/%s/script/%s.sh"' % (benchmark_set, benchmark)
    print(instr0)
    print(instr1)
    print('waiting for perf...')
    cmd_result_0 = exe.cmd(instr0)
    cmd_result_1 = exe.cmd(instr1)
    time.sleep(test_time)
    print('%d second passed...' % test_time)
    exe.cmd_and_wait('docker stop container0')
    exe.cmd_and_wait('docker stop container1')
    exe.cmd_and_wait('docker rm container0')
    exe.cmd_and_wait('docker rm container1')
    exe.cmd_and_wait('echo 1 > /proc/sys/kernel/nmi_watchdog')

    with open('temp.log', 'r') as log_f:
        logs = log_f.readlines()
    for log in logs:
        if 'insn per cycle' in log:
            print(log)
            ipc = log.split()[log.split().index('#') + 1]
            ipcs[benchmark] = float(ipc)
            print(ipcs)
            break
    exe.cmd_and_wait('rm -rf temp.log')

dict = {}
for root, dirs, files in os.walk('./'+ benchmark_set +'/log'):
    for file in files:
        if file == 'analysis.log':
            continue
        benchmark_name = file[0:file.index('_ocperf_list_extracted_')]
        if benchmark_name not in dict.keys():
            dict[benchmark_name] = {}
        event_list_name = file[file.index('_ocperf_list_extracted_')+ 21: file.index('.txt.log')]
        with open(benchmark_set + '/log/' + file, 'r') as result_f:
            result_list = result_f.readlines()
        for result in result_list:
            if 'seconds time elapsed' in result:
                break
            if '# started on' in result or 'Performance counter stats' in result:
                continue
            if '<not supported>' in result or '<not counted>' in result:
                continue
            result_tuple = result.split()
            if len(result_tuple) >= 3 and result_tuple[1] == 'MiB':
                dict[benchmark_name][result_tuple[2].strip()] = result_tuple[0].strip().replace(',', '')
            elif len(result_tuple) >= 2:
                dict[benchmark_name][result_tuple[1].strip()] = result_tuple[0].strip().replace(',', '')


with open(benchmark_set + '/log/analysis.log', 'w') as result_f:
    result_f.write(''.ljust(80, ' '))
    for benchmark_name in benchmark_list:
        result_f.write(benchmark_name.ljust(80, ' '))
    result_f.write('\n')

    result_f.write('ipc'.ljust(80, ' '))
    for benchmark_name in benchmark_list:
        result_f.write(str(ipcs[benchmark_name]).ljust(80, ' '))
    result_f.write('\n')

    pearson_result = {}
    event_list = dict[benchmark_list[0]].keys()
    for event in event_list:
        y = []
        # result_f.write(event.ljust(80, ' '))
        for benchmark_name in benchmark_list:
            num = float(dict[benchmark_name][event]) / float(dict[benchmark_name]['instructions'])
            y.append(num)
            # result_f.write(str(num).ljust(80, ' '))
        x = np.array(ipcs.values())
        y = np.array(y)
        pc = pearsonr(x, y)
        if pc[0] == pc[0]:
            pearson_result[event] = [' '.join(y.astype(str)), pc[0], pc[1]]
        # result_f.write(str(pc[0]) + ' ' + str(pc[1]) + ' \n')

    sorted_result = sorted(pearson_result.items(), key=lambda x: abs(x[1][1]), reverse=True)
    for i in range(100):
        result_f.write('%s %s %f %f\n' % (sorted_result[i][0], sorted_result[i][1][0], sorted_result[i][1][1], sorted_result[i][1][2]))

        



 


