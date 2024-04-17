cd /home/wjy/SComet/mixedbenchmark/script
rm -rf /var/log/redis
mkdir /var/log/redis
ps -ef | grep redis-server | grep -v grep | grep -v redis-server.sh | awk "{print \$2}" | xargs kill -9 2&>/dev/null
ps -ef | grep redis-sentinel | grep -v grep | awk "{print \$2}" | xargs kill -9 2&>/dev/null
cd /home/wjy/SComet/redis-7.2.4/src
echo $1
if (( $# >= 1 )); then
    echo 'slave'
    sed -i "1c replicaof $1 6379" ../redis-slave.conf
    # sed -i "92c sentinel monitor mymaster $1 6379 2" ../sentinel-slave.conf 
    ./redis-server ../redis-slave.conf
    # ./redis-sentinel ../sentinel-slave.conf
else
    echo 'master'
    ./redis-server ../redis-master.conf
    # ./redis-sentinel ../sentinel-master.conf
fi
