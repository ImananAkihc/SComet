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
# import matplotlib.pyplot as plt
import numpy as np

if len(sys.argv) > 1:
    benchmark_set = sys.argv[1]
else:
    print('Microbench name needed')
    exit(0)

LC_TASKS = ['memcached', 'nginx', 'masstree', 'silo', 'redis-cli', 'redis-server']

benchmark_list = []
for root, dirs, files in os.walk('./' + benchmark_set + '/script'):
    for file in files:
        if file.split('.')[-1] == 'sh' and '.'.join(file.split('.')[0:-1]) not in LC_TASKS:
            benchmark_list.append('.'.join(file.split('.')[0:-1]))
benchmark_list.sort()
print('benchmark list:')
print(benchmark_list)

ipcs_list = []
perf_result = {}
linear_result = {}

related_events = []
with open('extracted_list/related_event.txt', mode='r') as pmu_events_f:
    pmu_events = pmu_events_f.readlines()
    related_events = [event.strip() for event in pmu_events]
    related_events = [event for event in related_events if event != '']
print(related_events)

with open('perf_result_microbench.txt', 'r') as log_f:
    logs = log_f.readlines()
    microbenchmark_list = logs[0].split()
    ipcs = [float(ipc_str) for ipc_str in logs[1].split()[1:]]
    for i in range(2, len(logs)):
        event = logs[i].split()[0]
        if event not in related_events:
            continue
        perf_result[event] = [float(r) for r in logs[i].split()[1:-2]]
        linear_result[event] = list(np.polyfit(perf_result[event], ipcs , 1))
        print('%s %f %f %f' % (event, perf_result[event][7], ipcs[7],
                               linear_result[event][0] * perf_result[event][7] + linear_result[event][1]))
        # for j in range(len(microbenchmark_list)):
        #     print('%s %f %f %f' % (event, perf_result[event][j], ipcs[j], linear_result[event][0] * perf_result[event][j] + linear_result[event][1]))
        # print()

# count = {}
print('{')
for benchmark in benchmark_list:
    try:
        with open('%s/log/%s_related_full.txt.log' % (benchmark_set, benchmark), mode='r') as log_f:
            log_list = log_f.readlines()
            for log in log_list:
                if 'instructions' in log:
                    ins = float(log.split()[0].strip().replace(',', ''))
                    break
    except:
        continue
    predicted_list = []
    predicted_list_idle = []
    for event in related_events:
        if event == 'instructions':
            continue
        with open('%s/log/%s_related_full.txt.log' % (benchmark_set, benchmark), mode='r') as log_f:
            log_list = log_f.readlines()
        for log in log_list:
            if event in log:
                perf = float(log.split()[0].strip().replace(',', ''))
        predicted_list.append(perf * linear_result[event][0] / ins + linear_result[event][1])
    predicted_result = (sum(predicted_list) / len(predicted_list))
    print('\'%s\': %f,' % (benchmark, predicted_result))
print('}')

# sorted_count = sorted(count.items(), reverse=True, key=lambda x:x[1])
# print(sorted_count)

