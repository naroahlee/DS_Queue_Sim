#!/usr/bin/python
# Compare Exponential CDF between Theoretical and Emprical
import matplotlib.pyplot as plt
import numpy as np
import math
import csv
import sys

def usage():
	print "MD1_sim.py [Service_Rate] [Budget] [Period] [Input File] [Out File]"
	return

def read_arrival_data(infile):
	arrival_evt = []
	with open(infile, 'rb') as csvfile:
		myreader = csv.reader(csvfile, delimiter=',', quotechar='|')
		for row in myreader:
			for item in row:
				arrival_evt.append(float(item));
	return arrival_evt

# Everytime when execute or idle for sometime, we need to update the status of DS
def update_DS_after_idle(budget, period, remain_budget, next_period, cur_time):
	if (cur_time >= next_period): # Now it's a new period
		next_period = (math.floor(cur_time / period) + 1) * period
		remain_budget = budget	  # New Period with budget replenishment

	# Regardless of new or old period: budget cap is max_remain
	max_remain = next_period - cur_time
	if (remain_budget > max_remain):
		remain_budget = max_remain	
	
	return (remain_budget, next_period)

# Deterministic Deferrable Server
def run_MD1_DS_server(budget, period, service_rate, arrival_evt):
	service_dur  = 1.0 / service_rate

	atserver_evt = []
	leave_evt    = []

	index = 0

	state = 0; # IDLE
	cur_time = 0.0;
	remain_budget = budget;
	next_period   = period;
	while (index < len(arrival_evt)):
		if(0 == state): # IDLE
			cur_time = arrival_evt[index]
			(remain_budget, next_period) = update_DS_after_idle(budget, period, remain_budget, next_period, cur_time)
			state = 1 
		if(1 == state): # Execution
			while((index < len(arrival_evt)) and (cur_time >= arrival_evt[index])):
				atserver_evt.append(cur_time);

				if(remain_budget >= service_dur): # If old period can still handle
					cur_time += service_dur
					remain_budget -= service_dur
					# next_period = next_period   # next_period unchanged
				else:
					# First, burn up all the remain debris
					cur_time = next_period	# Uneven Budget Replenishment
					next_period += period
					service_remain = service_dur - remain_budget
					
					# Use Multiple whole DS period for serving
					# Yes, you can directly compute it if you want
					while(service_remain > budget): 
						cur_time = next_period
						next_period += period
						service_remain -= budget

					# Now the last potion of service_remain is less than budget:
					cur_time += service_remain
					remain_budget = budget - service_remain

				leave_evt.append(cur_time);
				index += 1
			state = 0

	return (atserver_evt, leave_evt)

#		else: # Active

# ================= Main ===================

if (len(sys.argv) != 6):
	usage()
	sys.exit(-1)

service_rate = float(sys.argv[1])
budget       = float(sys.argv[2])
period       = float(sys.argv[3])
infile       =       sys.argv[4]
outfile      =       sys.argv[5]

# Read Arrival Event
arrival_evt = read_arrival_data(infile)

# Run Simluation
(atserver_evt, leave_evt) = run_MD1_DS_server(budget, period, service_rate, arrival_evt)

# Save Event
with open(outfile, 'w') as outfile:
	for index in range(0, len(arrival_evt)):
		outfile.write('%f,%f,%f\n' % (arrival_evt[index], atserver_evt[index], leave_evt[index]))

