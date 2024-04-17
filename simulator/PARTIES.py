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

class PARTIES_Allocater(allocater.Allocater):

    resource_list = []
    max_cpu = 0
    max_memory = 0
    lc_cpu = []
    lc_memory = []
    be_cpu = []
    be_memory = []
    PARTIES_wheel = 0

    def __init__(self, benchmark_set_, QoS_, main_ip_, resources):
        super().__init__(benchmark_set_, QoS_, main_ip_)
        self.resource_list = ['cpu', 'memory']
        self.max_cpu = resources['cpu']
        self.max_memory = resources['memory']
        self.lc_cpu = []
        self.lc_memory = []
        self.be_cpu = []
        self.be_memory = []
        self.PARTIES_wheel = 0

    def wheel_next(self):
        self.PARTIES_wheel += 1
        self.PARTIES_wheel = self.PARTIES_wheel % len(self.resource_list)

    def set_cpu(self, container_instance, cpu):
        instr = '%s "find \\\"/sys/fs/cgroup/cpuset/docker/\\\" -name \\\"*%s*\\\""' % (container_instance.ssh_pre(), container_instance.get_id())
        cpu_file, err = exe.cmd_and_wait(instr)
        cpu_file = cpu_file[0].decode('utf-8').strip()
        cpu_str = ','.join([str(i) for i in cpu])
        exe.cmd_and_wait('%s "echo %s > %s/cpuset.cpus"' % (container_instance.ssh_pre(), cpu_str, cpu_file))

    def set_memory(self, container_instance, memory):
        instr = '%s "find \\\"/sys/fs/cgroup/memory/docker/\\\" -name \\\"*%s*\\\""' % (container_instance.ssh_pre(), container_instance.get_id())
        memory_file, err = exe.cmd_and_wait(instr)
        memory_file = memory_file[0].decode('utf-8').strip()
        exe.cmd_and_wait('%s "echo %d > %s/memory.limit_in_bytes"' % (container_instance.ssh_pre(), memory, memory_file))

    def assign_resource(self):
        for index in range(len(self.lc_cpu)):
            self.set_cpu(self.lc_containers[index], self.lc_cpu[index])
        for index in range(len(self.lc_memory)):
            self.set_memory(self.lc_containers[index], self.lc_memory[index])
        for index in range(len(self.be_cpu)):
            self.set_cpu(self.be_containers[index], self.be_cpu[index])
        for index in range(len(self.be_memory)):
            self.set_memory(self.be_containers[index], self.be_memory[index])

    def print_resource(self):
        print('resource allocation result:')
        for container_index in range(len(self.lc_containers)):
            print(self.lc_containers[container_index], self.lc_cpu[container_index], self.lc_memory[container_index])
        for container_index in range(len(self.be_containers)):
            print(self.be_containers[container_index], self.be_cpu[container_index], self.be_memory[container_index])
        spared_cpu, spared_memory = self.spared_resource()
        print('spared resource: ', spared_cpu, spared_memory)

    def spared_resource(self):
        spared_cpu = [n for n in range(self.max_cpu)]
        for cpu_allocated in self.lc_cpu + self.be_cpu:
            spared_cpu = [x for x in spared_cpu if x not in cpu_allocated]
        memory_used = sum(self.lc_memory) + sum(self.be_memory)
        spared_memory = self.max_memory - memory_used
        return spared_cpu, spared_memory
    
    def resource_reclaim(self):
        spared_cpu, spared_memory = self.spared_resource()
        for index in range(len(spared_cpu)):
            upsized_be = random.randint(0, len(self.be_cpu) - 1)
            self.be_cpu[upsized_be].append(spared_cpu[index])
        memory_increase = int(spared_memory / len(self.be_memory))
        for index in range(len(self.be_memory)):
            self.be_memory[index] += memory_increase
            spared_memory -= memory_increase
        if spared_memory > 0:
            self.be_memory[0] += spared_memory
        self.assign_resource()
        
    def prune(self):
        unfinished_lc = []
        unfinished_be = []
        container_index = 0
        while container_index < len(self.lc_containers):
            if self.lc_containers[container_index].running:
                if self.lc_containers[container_index].running.poll() != None:
                    print('lc task %s finished' % self.lc_containers[container_index].get_running_task())
                    unfinished_lc.append(self.lc_containers[container_index].get_running_task())
                    self.lc_containers[container_index].remove()
                    del self.lc_containers[container_index]
                    del self.lc_cpu[container_index]
                    del self.lc_memory[container_index]
                    continue
            container_index += 1
        container_index = 0
        while container_index < len(self.be_containers):
            if self.be_containers[container_index].running:
                if self.be_containers[container_index].running.poll() != None:
                    print('be task %s finished' % self.be_containers[container_index].get_running_task())
                    self.be_containers[container_index].remove()
                    del self.be_containers[container_index]
                    del self.be_cpu[container_index]
                    del self.be_memory[container_index]
                    continue
                if not self.be_cpu[container_index] or not self.be_memory[container_index]:
                    print('be task %s killed' % self.be_containers[container_index].get_running_task())
                    unfinished_be.append(self.be_containers[container_index].get_running_task())
                    self.be_containers[container_index].remove()
                    del self.be_containers[container_index]
                    del self.be_cpu[container_index]
                    del self.be_memory[container_index]
            container_index += 1
        return unfinished_lc, unfinished_be

    def resource_allocate(self):
        print('resource allocation:')
        QoS_status, slack_list = self.get_QoS_status()
        if QoS_status == 1:
            self.wheel_next()
            victim = slack_list[-1][0]
            print('downsize %s: %s' % (self.lc_containers[victim].task, self.resource_list[self.PARTIES_wheel]))
            if self.resource_list[self.PARTIES_wheel] == 'cpu':
                if len(self.lc_cpu[victim]) > 1:
                    self.lc_cpu[victim].pop(-1)
            if self.resource_list[self.PARTIES_wheel] == 'memory':
                self.lc_memory[victim] = int(self.lc_memory[victim] * 0.9)
            self.assign_resource()
        elif QoS_status == 0:
            print('hold')
        elif QoS_status == -1:
            self.wheel_next()
            vulnerable = slack_list[0][0]
            spared_cpu, spared_memory = self.spared_resource()
            if spared_cpu or spared_memory:
                print('upsize %s: spared resource' % (self.lc_containers[vulnerable].task))
                if spared_cpu:
                    self.lc_cpu[vulnerable].append(spared_cpu[-1])
                if spared_memory:
                    self.lc_memory[vulnerable] += min(spared_memory, int(self.lc_memory[vulnerable] * 0.1))
                self.assign_resource()
            else:
                victim_index = len(slack_list) - 1
                if self.resource_list[self.PARTIES_wheel] == 'cpu':
                    while slack_list[victim_index][1][0] < 0.15 or slack_list[victim_index][1][1] < 0.15 or len(self.lc_cpu[slack_list[victim_index][0]]) <= 1:
                        victim_index -= 1
                        if victim_index == -1:
                            break
                if self.resource_list[self.PARTIES_wheel] == 'memory':
                    while slack_list[victim_index][1][0] < 0.15 or slack_list[victim_index][1][1] < 0.15:
                        victim_index -= 1
                        if victim_index == -1:
                            break
                if victim_index != -1:
                    victim = slack_list[victim_index][0]
                    print('upsize %s: %s' % (self.lc_containers[vulnerable].task, self.resource_list[self.PARTIES_wheel]))
                    print('victim %s: %s' % (self.lc_containers[victim].task, self.resource_list[self.PARTIES_wheel]))
                    if self.resource_list[self.PARTIES_wheel] == 'cpu':
                        if len(self.lc_cpu[victim]) > 1:
                            spared_cpu = self.lc_cpu[victim].pop(-1)
                            self.lc_cpu[vulnerable].append(spared_cpu)
                    if self.resource_list[self.PARTIES_wheel] == 'memory':
                        spared_memory = self.lc_memory[victim] - int(self.lc_memory[victim] * 0.9)
                        self.lc_memory[victim] = self.lc_memory[victim] - spared_memory
                        self.lc_memory[vulnerable] += spared_memory
                    self.assign_resource()
                elif self.be_containers:
                    print('upsize %s: %s' % (self.lc_containers[vulnerable].task, self.resource_list[self.PARTIES_wheel]))
                    print('victim be task')
                    if self.resource_list[self.PARTIES_wheel] == 'cpu':
                        spared_cpu = self.be_cpu[-1].pop(-1)
                        self.lc_cpu[vulnerable].append(spared_cpu)
                    if self.resource_list[self.PARTIES_wheel] == 'memory':
                        spared_memory = self.be_memory[-1]
                        self.lc_memory[vulnerable] += spared_memory
                        self.be_memory[-1] = 0
                    self.assign_resource()
                else:
                    print('downsize failed, no victim task')
        self.print_resource()
        return QoS_status

class PARTIES_Scheduler(scheduler.Scheduler):
    
    RR_wheel = 0

    def __init__(self, benchmark_set_, tasks, main_ip_, passwd_, resources_):
        super().__init__(benchmark_set_, tasks, main_ip_, passwd_)
        for ip in passwd_.keys():
            self.node_list[ip] = PARTIES_Allocater(self.benchmark_set, tasks['QoS'][ip], self.main_ip, resources_[ip])
        self.RR_wheel = 0

    def algorithm(self):
        available = []
        for ip in self.node_list.keys():
            QoS_status = self.node_list[ip].resource_allocate()
            self.prune()
            if QoS_status == 1 and self.node_list[ip].lc_containers:
                spared_cpu, spared_memory = self.node_list[ip].spared_resource()
                if spared_cpu and spared_memory:
                    available.append(ip)
        if available and self.be_tasks:
            be_host = available[len(self.be_tasks) % len(available)]
            return self.be_tasks[0], be_host
        for ip in self.node_list.keys():
            if self.node_list[ip].lc_containers and self.node_list[ip].be_containers:
                if not self.be_tasks:
                    self.node_list[ip].resource_reclaim()
                elif len(self.node_list[ip].lc_containers) + len(self.node_list[ip].be_containers) == self.node_list[ip].max_cpu:
                    self.node_list[ip].resource_reclaim()
        return None, None

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
                spared_cpu, spared_memory = self.node_list[lc_host].spared_resource()
                self.node_list[lc_host].lc_cpu.append(spared_cpu[0: len(spared_cpu) // (len(self.lc_tasks) + 1)])
                self.node_list[lc_host].lc_memory.append(spared_memory // (len(self.lc_tasks) + 1))
                self.node_list[lc_host].assign_resource()
                self.node_list[lc_host].print_resource()
                rps_delta = int(time.time() - start_time) % 21600
                rps_delta = 1 - (abs(rps_delta - 10800) / 10800)
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
                spared_cpu, spared_memory = self.node_list[be_host].spared_resource()
                self.node_list[be_host].be_cpu.append(spared_cpu)
                self.node_list[be_host].be_memory.append(spared_memory)
                self.node_list[lc_host].assign_resource()
                self.node_list[be_host].print_resource()
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





                



