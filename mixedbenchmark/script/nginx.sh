cd /home/wjy/SComet/mixedbenchmark/script
rps=10000
thread=1
if (( $# >= 1 )); then
    rps=$1
fi
if (( $# >= 2 )); then
    thread=$2
fi
rm -rf /usr/local/nginx/logs/*.log
sed -i "3s/worker_processes.*/worker_processes  ${thread};/" /usr/local/nginx/conf/nginx.conf
sed -i "5s/#error_log  logs\/error.log/error_log off/" /usr/local/nginx/conf/nginx.conf
sed -i "25s/#access_log  logs\/access.log  main/access_log off/" /usr/local/nginx/conf/nginx.conf
/usr/local/nginx/sbin/nginx
/home/wjy/SComet/wrk2/wrk -t4 -c100 -d600s -R${rps} --latency http://127.0.0.1:80/html.index