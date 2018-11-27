#!/bin/bash
ArrivalRate=0.5
ServiceRate=1.0
SampleNum=10000
InName=./data/input/poisson01.csv
OutName=./data/output/poisson01.csv
./gen_poisson.py ${ArrivalRate} ${SampleNum} ${InName}
./MD1_sim.py ${ServiceRate} ${InName} ${OutName}
./plot_dist.py ${ArrivalRate} ${ServiceRate} ${OutName}

