rm -rf stream_*
rm -rf ../script/*
M=1048576
for((size=100;size<=400;size*=2))
do
    real_size=`expr ${size} \* ${M}`
    for((offset=0;offset<=2048;offset=offset*4+6))
    do
        file_name="../script/stream_${size}M_${offset}.sh"
        gcc -O -mcmodel=medium -DSTREAM_ARRAY_SIZE=${real_size} -DOFFSET=${offset} stream.c -o stream_${size}M_${offset}
        echo "cd /home/wjy/SComet/stream/src" > ${file_name}
        echo "./stream_${size}M_${offset}" >> ${file_name}
    done
done