#!/usr/bin/python3
import time
import math
import sys
import random
import roundrobin
sys.path.append('/home/wjy/SComet')
import exe

GB = 1024 * 1024
MB = 1024


class SComet_RoundRobin(roundrobin.RoundRobin):

    pollu_dict = {
        'breadthFirstSearch.backForwardBFS': 0.966389,
        'breadthFirstSearch.serialBFS': 0.962199,
        'classify.decisionTree': 0.962469,
        'comparisonSort.sampleSort': 0.964068,
        'comparisonSort.serialSort': 0.970957,
        'convexHull.quickHull': 0.972328,
        'convexHull.serialHull': 0.976813,
        'delaunayRefine.incrementalRefine': 0.821400,
        'delaunayTriangulation.incrementalDelaunay': 0.851043,
        'histogram.parallel': 0.960833,
        'histogram.sequential': 0.967998,
        'integerSort.parallelRadixSort': 0.965403,
        'integerSort.serialRadixSort': 0.954942,
        'invertedIndex.parallel': 0.951692,
        'invertedIndex.sequential': 0.951065,
        'longestRepeatedSubstring.doubling': 0.907019,
        'maximalIndependentSet.incrementalMIS': 0.968589,
        'maximalIndependentSet.serialMIS': 0.965375,
        'maximalMatching.incrementalMatching': 0.915638,
        'maximalMatching.serialMatching': 0.950162,
        'minSpanningForest.parallelFilterKruskal': 0.919565,
        'minSpanningForest.serialMST': 0.948152,
        'nBody.parallelCK': 0.985751,
        'nearestNeighbors.octTree': 0.963134,
        'rangeQuery2d.parallelPlaneSweep': 0.890239,
        'rangeQuery2d.serial': 0.866934,
        'rayCast.kdTree': 0.913396,
        'removeDuplicates.parlayhash': 0.961734,
        'removeDuplicates.serial_hash': 0.964902,
        'spanningForest.ndST': 0.935266,
        'spanningForest.serialST': 0.949323,
        'stream_100M_2046': 0.938775,
        'stream_100M_510': 0.933811,
        'stream_200M_2046': 0.935980,
        'stream_200M_510': 0.934868,
        'stream_400M_2046': 0.948286,
        'stream_400M_510': 0.950792,
        'suffixArray.parallelRange': 0.941632,
        'suffixArray.serialDivsufsort': 0.950680,
        'wordCounts.histogram': 0.947111,
        'wordCounts.serial': 0.921046,
        'microbench_pollu1': 0.37
    }


    def __init__(self, benchmark_set_, tasks, main_ip_, passwd_):
        super().__init__(benchmark_set_, tasks, main_ip_, passwd_)

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
                available.append(index)
        if available and self.be_tasks:
            self.RR_wheel = (self.RR_wheel + 1) % len(self.node_list.keys())
            while self.RR_wheel not in available:
                self.RR_wheel = (self.RR_wheel + 1) % len(self.node_list.keys())
            be_host = list(self.node_list.keys())[self.RR_wheel]
            min_slack = slack_dict[be_host][0][1][0]
            self.be_tasks.sort(reverse=True, key=lambda x:self.pollu_dict[x])
            if self.be_tasks:
                if min_slack < 0.15:
                    return None, None
                if min_slack >= 0.15 and min_slack < 0.3:
                    return self.be_tasks[0], be_host
                if min_slack >= 0.3 and min_slack < 0.5:
                    return self.be_tasks[len(self.be_tasks) // 2], be_host
                if min_slack >= 0.5:
                    return self.be_tasks[-1], be_host
        return None, None

                



