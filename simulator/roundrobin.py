#!/usr/bin/python3
import scheduler
import time
import math
import sys
import random
sys.path.append('/home/wjy/SComet')
import exe

class RoundRobin(scheduler.Scheduler):

    RR_wheel = 0

    def __init__(self, benchmark_set_, tasks, main_ip_, passwd_):
        super().__init__(benchmark_set_, tasks, main_ip_, passwd_)
        self.RR_wheel = 0

    def algorithm(self):
        available = []
        for index in range(len(self.node_list.keys())):
            ip = list(self.node_list.keys())[index]
            QoS_status, slack_list = self.node_list[ip].get_QoS_status()
            if QoS_status == -1 and self.node_list[ip].be_containers:
                self.be_tasks.append(self.node_list[ip].be_containers[-1].task)
                self.node_list[ip].be_containers[-1].remove()
                del self.node_list[ip].be_containers[-1]
                time.sleep(60)
            elif QoS_status >= 0:
                available.append(index)
        if available and self.be_tasks:
            self.RR_wheel = (self.RR_wheel + 1) % len(self.node_list.keys())
            while self.RR_wheel not in available:
                self.RR_wheel = (self.RR_wheel + 1) % len(self.node_list.keys())
            be_host = list(self.node_list.keys())[self.RR_wheel]
            return self.be_tasks[0], be_host
        return None, None



                



