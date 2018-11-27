#!/bin/bash
ArrivalRate=0.9
ServiceRate=1.0
SampleNum=100000
InName=./data/input/poisson01.csv
OutName=./data/output/poisson01.csv
./gen_poisson.py ${ArrivalRate} ${SampleNum} ${InName}
./MD1_sim.py ${ServiceRate} ${InName} ${OutName}
./plot_dist.py ${ArrivalRate} ${ServiceRate} ${OutName}

