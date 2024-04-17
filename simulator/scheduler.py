#!/usr/bin/python3
import allocater
import container
import time
import math
import sys
import json
sys.path.append('/home/wjy/SComet')
import exe

class Scheduler:
    benchmark_set = ''
    lc_tasks = []
    be_tasks = []
    max_load = {}
    threads = {}
    lc_target = {}
    main_ip = ''
    passwd = {}
    node_list = {}

    def __init__(self, benchmark_set_, tasks, main_ip_, passwd_):
        self.benchmark_set = benchmark_set_
        self.lc_tasks = tasks['lc_tasks']
        self.be_tasks = tasks['be_tasks']
        self.max_load = tasks['max_load']
        self.threads = tasks['threads']
        self.lc_target = tasks['lc_target']
        self.main_ip = main_ip_
        self.passwd = passwd_
        for ip in passwd_.keys():
            self.node_list[ip] = allocater.Allocater(self.benchmark_set, tasks['QoS'][ip], self.main_ip)

    def algorithm(self):
        available = []
        for ip in self.node_list.keys():
            QoS_status, slack_list = self.node_list[ip].get_QoS_status()
            if QoS_status == -1 and self.node_list[ip].be_containers:
                self.be_tasks.append(self.node_list[ip].be_containers[-1].task)
                self.node_list[ip].be_containers[-1].remove()
                del self.node_list[ip].be_containers[-1]
                time.sleep(60)
            elif QoS_status == 1:
                available.append(ip)
        if available and self.be_tasks:
            be_host = available[len(self.be_tasks) % len(available)]
            return self.be_tasks[0], be_host
        return None, None
    
    def prune(self):
        for ip in self.node_list.keys():
            unfinished_lc, unfinished_be = self.node_list[ip].prune()
            self.lc_tasks += unfinished_lc
            self.be_tasks += unfinished_be

    def run(self):
        start_time = time.time()
        while True:
            time.sleep(10)
            print('\ntime %d:' % (time.time() - start_time))
            self.prune()
            for ip in self.node_list.keys():
                print("lc on %s: " % ip, self.node_list[ip].lc_containers)
                print("be on %s: " % ip, self.node_list[ip].be_containers)

            if self.lc_tasks:
                lc = self.lc_tasks.pop()
                lc_host = self.lc_target[lc]
                self.node_list[lc_host].lc_containers.append(
                    container.Container('scomet', 'lc_container%d' % self.node_list[lc_host].unused_lc_index(), lc_host,
                                        self.passwd[lc_host]))
                rps_delta = int(time.time() - start_time) % 10800
                rps_delta = 1 - (abs(rps_delta - 5400) / 5400)
                rps = int(self.max_load[lc_host][lc] * rps_delta * 3 / 4 + self.max_load[lc_host][lc] / 4)
                self.node_list[lc_host].lc_containers[-1].run_task(self.benchmark_set, lc,
                                                                   '%d %d' % (rps, self.threads[lc_host][lc]))
                time.sleep(60)
                continue
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
                



