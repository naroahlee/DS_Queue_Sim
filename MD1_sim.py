#!/usr/bin/python
# Compare Exponential CDF between Theoretical and Emprical
import matplotlib.pyplot as plt
import numpy as np
import statsmodels.api as sm
import csv
import sys


# \lambda
arrival_rate = 0.5
sample_num   = 500
service_rate = 1.0
service_dur  = 1.0 / service_rate

# Generate Emprical Samples
beta = 1.0 / arrival_rate
alldata = np.random.exponential(beta, sample_num)

arrival_evt = []
cur_time = 0.0
for evt in alldata:
	cur_time += evt
	arrival_evt.append(cur_time)

# Deterministic Server

arrival_evt  = [1.0, 1.1, 1.2, 4, 4.1, 6.0, 8.0]
atserver_evt = []
leave_evt    = []

index = 0
cur_time = 0.0;
state = 0; # IDLE
while (index < len(arrival_evt)):
	if(0 == state):
		cur_time = arrival_evt[index]
		state = 1 # Active
	else: # Active
		while((index < len(arrival_evt)) and (cur_time >= arrival_evt[index])):
			atserver_evt.append(cur_time);
			cur_time += service_dur
			leave_evt.append(cur_time);
			index += 1
		state = 0


print arrival_evt
print atserver_evt
print leave_evt
