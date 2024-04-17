#!/usr/bin/python3
import time
import math
import sys
import random
import json
import allocater
import scheduler
import container
sys.path.append('/home/wjy/SComet')
import exe

GB = 1024 * 1024
MB = 1024

class Rhythm(scheduler.Scheduler):

    RR_wheel = 0

    def __init__(self, benchmark_set_, tasks, main_ip_, passwd_):
        self.benchmark_set = benchmark_set_
        self.lc_tasks = ['redis-master', 'redis-slave']
        self.be_tasks = tasks['be_tasks']
        self.max_load = {'redis-master': 15, 'redis-slave': 15}
        self.threads = {'redis-master': 1, 'redis-slave': 1}
        self.lc_target = {'redis-master': '172.17.1.119', 'redis-slave': '172.17.1.60'}
        self.main_ip = main_ip_
        self.passwd = passwd_
        QoS = {'172.17.1.119': {'redis-master': 0.4, 'redis-slave': 0.5}, '172.17.1.60': {'redis-master': 0.4, 'redis-slave': 0.5}}
        for ip in passwd_.keys():
            self.node_list[ip] = allocater.Allocater(self.benchmark_set, QoS[ip], self.main_ip)
        self.RR_wheel = 0

    def algorithm(self):
        available = []
        slack_dict = {}
        for index in range(len(self.node_list.keys())):
            ip = list(self.node_list.keys())[index]
            QoS_status, slack_dict[ip] = self.node_list[ip].get_QoS_status()
            if QoS_status == -1 and self.node_list[ip].be_containers:
                self.be_tasks.append(self.node_list[ip].be_containers[-1].task)
                self.node_list[ip].be_containers[-1].remove()
                del self.node_list[ip].be_containers[-1]
                time.sleep(60)
            elif QoS_status == 1:
                min_slack = slack_dict[ip][0][1][0]
                if self.node_list[ip].lc_containers[0].task == 'redis-master' and min_slack >= 0.25:
                    available.append(index)
                if self.node_list[ip].lc_containers[0].task == 'redis-slave' and min_slack >= 0.3:
                    available.append(index)
        if available and self.be_tasks:
            self.RR_wheel = (self.RR_wheel + 1) % len(self.node_list.keys())
            while self.RR_wheel not in available:
                self.RR_wheel = (self.RR_wheel + 1) % len(self.node_list.keys())
            be_host = list(self.node_list.keys())[self.RR_wheel]
            return self.be_tasks[0], be_host
        return None, None

    def run(self):
        start_time = time.time()
        timestamp = start_time
        cnt = 0
        while True:
            time.sleep(10)
            print('\ntime %d:' % (time.time() - start_time))
            print(time.asctime(time.localtime()))
            if time.time() - timestamp > 300:
                cnt += 1
                timestamp = time.time()
                for ip in self.node_list.keys():
                    for index in range(len(self.node_list[ip].lc_containers)):
                        self.lc_tasks.append(self.node_list[ip].lc_containers[index].task)
                        self.node_list[ip].lc_containers[index].remove()
                        del self.node_list[ip].lc_containers[index]
                        with open('%s_latency_result.txt' % ip, mode='w') as result_f:
                            result_f.write(json.dumps(self.node_list[ip].latency_result))
                        with open('%s_violate_result.txt' % ip, mode='w') as result_f:
                            result_f.write(json.dumps(self.node_list[ip].violate_result))

            self.prune()
            for ip in self.node_list.keys():
                print("lc on %s: " % ip, self.node_list[ip].lc_containers)
                print("be on %s: " % ip, self.node_list[ip].be_containers)

            if self.lc_tasks:
                self.lc_tasks.clear()
                exe.cmd_and_wait('echo "y" | docker system prune')
                exe.cmd_and_wait('docker network create -d overlay  --attachable scomet')
                master_host = self.lc_target['redis-master']
                slave_host = self.lc_target['redis-slave']
                self.node_list[master_host].lc_containers.append(
                    container.Container('scomet', 'lc_container%d' % self.node_list[master_host].unused_lc_index(), master_host,
                                        self.passwd[master_host], net=True))
                self.node_list[slave_host].lc_containers.append(
                    container.Container('scomet', 'lc_container%d' % self.node_list[slave_host].unused_lc_index(), slave_host,
                                        self.passwd[slave_host], net=True))

                self.node_list[master_host].lc_containers[-1].run_task(self.benchmark_set, 'redis-master')
                docker_host = self.node_list[master_host].lc_containers[-1].get_ip()
                self.node_list[slave_host].lc_containers[-1].run_task(self.benchmark_set, 'redis-slave', docker_host)
                time.sleep(60)

                rps = cnt // 2
                rps = rps % 30 + 1
                if rps > 15:
                    rps = 31 - rps
                self.node_list[master_host].lc_containers[-1].run_accompany_task(self.benchmark_set, 'redis-master-cli', '20 %d' % rps)
                self.node_list[slave_host].lc_containers[-1].run_accompany_task(self.benchmark_set, 'redis-slave-cli', '20 %d' % rps)
                
            be, be_host = self.algorithm()
            if be:
                self.be_tasks.remove(be)
                self.node_list[be_host].be_containers.append(
                    container.Container('scomet', 'be_container%d' % self.node_list[be_host].unused_be_index(), be_host,
                                        self.passwd[be_host]))
                self.node_list[be_host].be_containers[-1].run_task(self.benchmark_set, be)
                print('be task remain %d :' % len(self.be_tasks), self.be_tasks)
                time.sleep(60)
            if not self.be_tasks:
                finished = True
                for ip in self.node_list.keys():
                    if self.node_list[ip].be_containers:
                        finished = False
                if finished:
                    print('finished')
                    for ip in self.node_list.keys():
                        print(ip)
                        with open('%s_latency_result.txt' % ip, mode='w') as result_f:
                            result_f.write(json.dumps(self.node_list[ip].latency_result))
                        with open('%s_violate_result.txt' % ip, mode='w') as result_f:
                            result_f.write(json.dumps(self.node_list[ip].violate_result))
                        for container_instance in self.node_list[ip].lc_containers + self.node_list[ip].be_containers:
                            container_instance.remove()
                    break





                



