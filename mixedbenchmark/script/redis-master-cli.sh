cd /home/wjy/SComet/mixedbenchmark/script
thread=50
pipeline=1
if (( $# >= 1 )); then
    thread=$1
fi
if (( $# >= 2 )); then
    pipeline=$2
fi
/home/wjy/SComet/redis-7.2.4/src/redis-benchmark -n `expr ${thread} \* ${pipeline} \* 5000` -c ${thread} -t get,set -P ${pipeline} -l > ../QoS/redis.log &
# /home/wjy/SComet/redis-7.2.4/src/redis-benchmark -n `expr ${rps} \* 15` -c 100 -t get,set -P `expr ${rps} \/ 100` -l > ../QoS/redis.log &
sleep 600
ps -ef | grep redis-benchmark | grep -v grep | awk "{print \$2}" | xargs kill -9
exit