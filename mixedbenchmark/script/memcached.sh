cd /home/wjy/SComet/mixedbenchmark/script
rps=50000
thread=1
if (( $# >= 1 )); then
    rps=$1
fi
if (( $# >= 2 )); then
    thread=$2
fi
rm -rf ../QoS/memcached.log
/usr/bin/memcached -t ${thread} -u root -p 11211 -m 64m -d
for((i=0;i<4;i++))
do
    echo "create thread ${i}"
    /home/wjy/SComet/mutated/client/mutated_memcache 127.0.0.1:11211 ${rps} -n 4 -w 5s -c 5s -s 600s  >> ../QoS/memcached.log &
    sleep 0.1
done
wait