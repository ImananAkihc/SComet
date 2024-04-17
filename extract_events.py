#!/usr/bin/python
import os
import sys
import shutil

perf_list = ''
if len(sys.argv) > 1:
    perf_list = sys.argv[1]
else:
    print('perf_list needed')
    exit(0)

with open(perf_list, mode='r') as log_f:
    logs = log_f.readlines()

type_black_list = ['DSB', 'FLOPS', 'Frontend', 'Frontend_Bandwidth', 'Memory_BW', 'Memory_Bound', 'Memory_Lat', 'Pipeline', 'Ports_Utilization', 'Power', 'SMT', 'Summary', 'TLB', 'TopDownL1', ]
event_black_list = ['ipi:ipi_send_cpumask']

logs_category={'basic':[]}
curr_type = 'basic'
for i in range(len(logs)):
    log = logs[i].strip()
    if len(log) == 0:
        continue
    if log[-1] == ':' and logs[i][0] != ' ':
        curr_type = log[0:-1]
        logs_category[curr_type] = []
    else:
        logs_category[curr_type].append(log)

event_lists = {}
event_per_list = 80
for key in logs_category.keys():
    if key in type_black_list:
        continue
    print(key)
    joined = ''.join(logs_category[key])
    splited = joined.split(']')
    count = -1
    for l in splited:
        if '[' not in l:
            continue
        l = l.split('[')[0].strip()
        if ' OR ' in l:
            l = l.split(' OR ')[0]
        if l in event_black_list:
            continue
        if len(l) > 0:
            count += 1
            if count % event_per_list == 0:
                event_lists[key + str(int(count / event_per_list))] = []
            event_lists[key + str(count // event_per_list)].append(l)

if os.path.exists('extracted_list'):
    shutil.rmtree('extracted_list')
os.makedirs('extracted_list', mode = 777)
with open('profiling.sh', mode='w') as shell_f:
    shell_f.write('export PATH=$PATH:/home/wjy/pmu-tools\n')
    shell_f.write('if [ $# = 1 ]; then\n')
    for key in event_lists.keys():
        with open('extracted_list/%s_extracted_%s.txt' % (perf_list.split('.txt')[0], key.replace(' ', '_')),mode='w') as log_f:
            log_f.writelines([event + '\n' for event in event_lists[key]])
        shell_f.write('\tpython perf.py $1 -e extracted_list/%s_extracted_%s.txt\n' % (perf_list.split('.txt')[0], key.replace(' ', '_')))
    shell_f.write('fi\n')
    shell_f.write('if [ $# = 2 ]; then\n')
    for key in event_lists.keys():
        shell_f.write('\tpython perf.py $1 -e extracted_list/%s_extracted_%s.txt --benchmark $2\n' % (perf_list.split('.txt')[0], key.replace(' ', '_')))
    shell_f.write('fi\n')



