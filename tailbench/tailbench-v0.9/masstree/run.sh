#!/bin/bash

if [[ -z "${NTHREADS}" ]]; then NTHREADS=1; fi

QPS=1000
MAXREQS=3000
WARMUPREQS=14000

if (($# >= 3)); then
    QPS=$1
    MAXREQS=$2
    WARMUPREQS=$3
fi 

if (($# >= 4)); then
    NTHREADS=$4
fi 

echo ${QPS}
echo ${MAXREQS}
echo ${WARMUPREQS}
echo ${NTHREADS}

TBENCH_QPS=${QPS} TBENCH_MAXREQS=${MAXREQS} TBENCH_WARMUPREQS=${WARMUPREQS} \
    TBENCH_MINSLEEPNS=10000 ./mttest_integrated -j${NTHREADS} \
    mycsba masstree

