cd /home/wjy/SComet/mixedbenchmark/script
rps=1000
thread=1
if (( $# >= 1 )); then
    rps=$1
fi
if (( $# >= 2 )); then
    thread=$2
fi
cd /home/wjy/SComet/tailbench/tailbench-v0.9/masstree/
sh run.sh ${rps} `expr ${rps} \* 600` ${rps} ${thread}
