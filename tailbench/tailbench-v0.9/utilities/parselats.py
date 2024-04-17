#!/usr/bin/python

import sys
import os
import numpy as np
from scipy import stats

class Lat(object):
    def __init__(self, fileName):
        f = open(fileName, 'rb')
        a = np.fromfile(f, dtype=np.uint64)
        self.reqTimes = a.reshape((a.shape[0]/4, 4))
        f.close()

    def parseQueueTimes(self):
        return self.reqTimes[:, 0]

    def parseSvcTimes(self):
        return self.reqTimes[:, 1]

    def parseSojournTimes(self):
        return self.reqTimes[:, 2]

    def parseQps(self):
        return self.reqTimes[:, 3][0]

if __name__ == '__main__':
    def getLatPct(latsFile):
        assert os.path.exists(latsFile)

        latsObj = Lat(latsFile)

        qTimes = [l/1e3 for l in latsObj.parseQueueTimes()]
        svcTimes = [l/1e3 for l in latsObj.parseSvcTimes()]
        sjrnTimes = [l/1e3 for l in latsObj.parseSojournTimes()]
        qps = int(latsObj.parseQps())
        f = open('lats.txt','w')

        # f.write('%12s | %12s | %12s\n\n' \
        #        % ('QueueTimes', 'ServiceTimes', 'SojournTimes'))

        # for (q, svc, sjrn) in zip(qTimes, svcTimes, sjrnTimes):
        #    f.write("%12s | %12s | %12s | %12s\n" \
        #            % ('%.3f' % q, '%.3f' % svc, '%.3f' % sjrn, '%d' % qps))
        for i in range(0, len(sjrnTimes) - qps * 10, qps):
            histogram = sjrnTimes[i: i + qps * 10]

            for my_percentile in range(5, 100, 5):
                f.write('%dth percentile latency %d\n' % (my_percentile, int(stats.scoreatpercentile(histogram, my_percentile))))
            for my_percentile in range(9900, 10000, 10):
                f.write('%.2fth percentile latency %d\n' % (my_percentile / 100.0, int(stats.scoreatpercentile(histogram, my_percentile / 100.0))))
        f.close()


        p99 = stats.scoreatpercentile(sjrnTimes, 99)
        maxLat = max(sjrnTimes)
        print "99th percentile latency %.3f us | max latency %.3f us" \
                % (p99, maxLat)

    latsFile = sys.argv[1]
    getLatPct(latsFile)
        
