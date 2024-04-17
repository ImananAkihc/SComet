#!/usr/bin/python3
import os
import sys
import random
import time
import scheduler
import PARTIES
import roundrobin
import greedy
import Rhythm
import SComet_PARTIES
import SComet_roundrobin
import SComet_greedy
import SComet_Rhythm
sys.path.append('/home/wjy/SComet')
import exe

PASSWD = {'172.17.1.119': 'example', '172.17.1.60': 'example'}
LC_TASKS = ['memcached', 'nginx', 'masstree', 'silo', 'redis-master', 'redis-slave', 'redis-master-cli', 'redis-slave-cli']
LC_TARGET = {'memcached': '172.17.1.119', 'nginx': '172.17.1.60', 'masstree': '172.17.1.119', 'silo': '172.17.1.60', 'redis-master': '172.17.1.119', 'redis-slave': '172.17.1.60'}
QOS = {}
MAX_LOAD = {}
THREADS = {}
RESOURCES = {}

REPEAT = 1
ALGORITHM = 'Rhythm'

benchmark_set = 'microbenchmark'
if len(sys.argv) > 1:
    benchmark_set = sys.argv[1]
    print('benchmark set: %s' % benchmark_set)
else:
    print('Microbench name needed')
    exit(0)
if '-a' in sys.argv:
    ALGORITHM = sys.argv[sys.argv.index('-a') + 1]

exe.cmd_and_wait('rm -rf /home/wjy/SComet/'+ benchmark_set +'/QoS/*')
exe.cmd_and_wait('echo "y" | docker system prune')
exe.cmd_and_wait('docker network create -d overlay  --attachable scomet')

benchmark_list = []
lc_tasks = []
be_tasks = []
for root, dirs, files in os.walk('/home/wjy/SComet/'+ benchmark_set +'/script'):
    for file in files:
        if file.split('.')[-1] == 'sh':
            benchmark_name = '.'.join(file.split('.')[0:-1])
            benchmark_list.append(benchmark_name)
            for LC in LC_TASKS:
                if LC in benchmark_name:
                    lc_tasks.append(benchmark_name)
                    break
            if benchmark_name not in LC_TASKS:
#                for r in range(REPEAT):
#                    be_tasks.append(benchmark_name + '_%d' % r)
                be_tasks.append(benchmark_name)


if ALGORITHM == 'PARTIES' or ALGORITHM == 'SComet_PARTIES':
    lc_tasks = lc_tasks[0:1]
    print('lc list:')
    print(lc_tasks)
    print('be list:')
    random.seed(2017)
    random.shuffle(be_tasks)
    print(be_tasks)
    QOS['172.17.1.119'] = {'memcached': 2000, 'nginx': 1000, 'masstree': 4000, 'silo': 2000}
    MAX_LOAD['172.17.1.119'] = {'memcached': 3000, 'nginx': 36000, 'masstree': 5000, 'silo': 5000}
    THREADS['172.17.1.119'] = {'memcached': 4, 'nginx': 4, 'masstree': 4, 'silo': 2}
    RESOURCES['172.17.1.119'] = {'cpu': 8, 'memory': 100000000 * 1024}
    tasks = {'lc_tasks': lc_tasks, 'be_tasks': be_tasks, 'QoS': QOS, 'max_load': MAX_LOAD, 'threads': THREADS,
             'lc_target': LC_TARGET}
    # s = PARTIES.PARTIES_Scheduler(benchmark_set, tasks, '172.17.1.119', {'172.17.1.119': 'example'}, RESOURCES)
    s = SComet_PARTIES.SComet_Scheduler(benchmark_set, tasks, '172.17.1.119', {'172.17.1.119': 'example'}, RESOURCES)
elif ALGORITHM == 'Rhythm' or ALGORITHM == 'SComet_Rhythm':
    lc_tasks = ['redis-master', 'redis-slave']
    print('lc list:')
    print(lc_tasks)
    print('be list:')
    random.seed(2017)
    random.shuffle(be_tasks)
    print(be_tasks)
    QoS = {'172.17.1.119': {'redis-master': 0.4, 'redis-slave': 0.5}, '172.17.1.60': {'redis-master': 0.4, 'redis-slave': 0.5}}
    MAX_LOAD = {'172.17.1.119': {'redis-master': 15, 'redis-slave': 15}, '172.17.1.60': {'redis-master': 15, 'redis-slave': 15}}
    MAX_LOAD = {'172.17.1.119': {'redis-master': 1, 'redis-slave': 1}, '172.17.1.60': {'redis-master': 1, 'redis-slave': 1}}
    tasks = {'lc_tasks': lc_tasks, 'be_tasks': be_tasks, 'QoS': QOS, 'max_load': MAX_LOAD, 'threads': THREADS,
             'lc_target': LC_TARGET}
    s = Rhythm.Rhythm(benchmark_set, tasks, '172.17.1.119', {'172.17.1.119': 'example', '172.17.1.60': 'example'})
    # s = SComet_Rhythm.SComet_Rhythm(benchmark_set, tasks, '172.17.1.119', {'172.17.1.119': 'example', '172.17.1.60': 'example'})
else:
    lc_tasks = lc_tasks[0:2]
    print('lc list:')
    print(lc_tasks)
    print('be list:')
    random.seed(2017)
    random.shuffle(be_tasks)
    print(be_tasks)
    QOS['172.17.1.119'] = {'memcached': 2000, 'nginx': 1000, 'masstree': 4000, 'silo': 2000}
    MAX_LOAD['172.17.1.119'] = {'memcached': 3000, 'nginx': 36000, 'masstree': 5000, 'silo': 5000}
    THREADS['172.17.1.119'] = {'memcached': 4, 'nginx': 4, 'masstree': 4, 'silo': 2}
    QOS['172.17.1.60'] = {'memcached': 2000, 'nginx': 5000, 'masstree': 40000, 'silo': 1000}
    MAX_LOAD['172.17.1.60'] = {'memcached': 5000, 'nginx': 60000, 'masstree': 16000, 'silo': 8000}
    THREADS['172.17.1.60'] = {'memcached': 1, 'nginx': 8, 'masstree': 8, 'silo': 4}
    tasks = {'lc_tasks': lc_tasks, 'be_tasks': be_tasks, 'QoS': QOS, 'max_load': MAX_LOAD, 'threads': THREADS,
             'lc_target': LC_TARGET}
    # s = roundrobin.RoundRobin(benchmark_set, tasks, '172.17.1.119', {'172.17.1.119': 'example', '172.17.1.60': 'example'})
    # s = SComet_roundrobin.SComet_RoundRobin(benchmark_set, tasks, '172.17.1.119', {'172.17.1.119': 'example', '172.17.1.60': 'example'})
    # s = greedy.Greedy(benchmark_set, tasks, '172.17.1.119', {'172.17.1.119': 'example', '172.17.1.60': 'example'})
    s = SComet_greedy.SComet_Greedy(benchmark_set, tasks, '172.17.1.119', {'172.17.1.119': 'example', '172.17.1.60': 'example'})

s.run()



