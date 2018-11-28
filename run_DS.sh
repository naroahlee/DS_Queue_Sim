#!/bin/bash
ArrivalRate=0.5
ServiceRate=1
Budget=1.5
Period=2
SampleNum=10000
InName=./data/input/poisson02.csv
OutName=./data/output/poisson02_DS.csv
./gen_poisson.py ${ArrivalRate} ${SampleNum} ${InName}
./MD1_DS_sim.py ${ServiceRate} ${Budget} ${Period} ${InName} ${OutName}
./plot_dist.py ${ArrivalRate} ${ServiceRate} ${OutName}

