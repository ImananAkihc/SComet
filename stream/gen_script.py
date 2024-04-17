#!/usr/bin/python
import os

for root, dirs, files in os.walk('./log_test_time'):
    for file in files:
        benchmark_name=file[0:file.index('_ocperf_list_extracted_basic0')]
        print(benchmark_name)
        with open('./log_test_time/%s' % file, mode='r') as log_f:
            logs = log_f.readlines()
            for log in logs:
                if 'seconds time elapsed' in log:
                    run_time = float(log.split()[0])
                    break
        if run_time < 1:
            break
        with open('./script/%s.sh' % benchmark_name, mode='w') as script_f:
            script_f.write('cd /home/wjy/SComet/stream/src\n')
            for i in range(int(600 / run_time) + 1):
                script_f.write('./%s\n' % benchmark_name)



