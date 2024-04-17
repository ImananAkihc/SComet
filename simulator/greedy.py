#!/usr/bin/python3
import scheduler
import time
import math
import sys
import random
sys.path.append('/home/wjy/SComet')
import exe

class Greedy(scheduler.Scheduler):

    def __init__(self, benchmark_set_, tasks, main_ip_, passwd_):
        super().__init__(benchmark_set_, tasks, main_ip_, passwd_)

    def algorithm(self):
        available = []
        maxmin_slack = 0
        for index in range(len(self.node_list.keys())):
            ip = list(self.node_list.keys())[index]
            QoS_status, slack_list = self.node_list[ip].get_QoS_status()
            min_slack = slack_list[0][1][0]
            if QoS_status == -1 and self.node_list[ip].be_containers:
                self.be_tasks.append(self.node_list[ip].be_containers[-1].task)
                self.node_list[ip].be_containers[-1].remove()
                del self.node_list[ip].be_containers[-1]
                time.sleep(60)
            elif QoS_status == 1:
                if maxmin_slack < min_slack:
                    available = [index]
                    maxmin_slack = min_slack
        if available and self.be_tasks:
            be_host = list(self.node_list.keys())[available[0]]
            return self.be_tasks[0], be_host
        return None, None



                



