make clean
make all
length=1000000

<< 'COMMENT'
for((i=1;i<=7;i++))
do
    for((j=1;j<=1024;j*=4))
    do
        file_name="../script/microbench_pollu_${i}_${j}.sh"
        echo "cd /home/wjy/SComet/microbenchmark/src" > ${file_name}
        echo "./microbench_pollu ${j} ${length} ${i}" >> ${file_name}
    done
done

for((i=1;i<=7;i++))
do
    file_name="../script/microbench_pollu_${i}.sh"
    echo "cd /home/wjy/SComet/microbenchmark/src" > ${file_name}
    echo "./microbench_pollu 0 ${length} ${i}" >> ${file_name}
done

file_name="../script/microbench.sh"
echo "cd /home/wjy/SComet/microbenchmark/src" > ${file_name}
echo "./microbench 0 ${length}" >> ${file_name}
COMMENT

for((i=1;i<=12;i++))
do
    file_name="../script/microbench_pollu${i}.sh"
    echo "cd /home/wjy/SComet/microbenchmark/src" > ${file_name}
    echo "./microbench_pollu 0 100000 7" >> ${file_name}
done