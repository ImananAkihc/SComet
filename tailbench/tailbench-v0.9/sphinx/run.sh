#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
source ${DIR}/../configs.sh

QPS=1
MAXREQS=10
WARMUPREQS=10
THREADS=1

if (($# >= 3)); then
    QPS=$1
    MAXREQS=$2
    WARMUPREQS=$3
fi 

if (($# >= 4)); then
    THREADS=$4
fi 
AUDIO_SAMPLES='audio_samples'

LD_LIBRARY_PATH=./sphinx-install/lib:${LD_LIBRARY_PATH} \
    TBENCH_QPS=${QPS} TBENCH_MAXREQS=${MAXREQS} TBENCH_WARMUPREQS=${WARMUPREQS} TBENCH_MINSLEEPNS=10000 \
    TBENCH_AN4_CORPUS=${DATA_ROOT}/sphinx TBENCH_AUDIO_SAMPLES=${AUDIO_SAMPLES} \
    ./decoder_integrated -t $THREADS
