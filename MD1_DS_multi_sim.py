#!/usr/bin/python
# Deferrable Server Parameter Control Test
import matplotlib.pyplot as plt
import numpy as np
import math
import csv
import sys
from md1_cdf import MD1_Response_CDF

def usage():
	print "MD1_DS_multisim.py [Arrival_Rate] [Service_Rate] [Input File]"
	print "lambda and mu for Theoretical Plot"
	return

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

if (len(sys.argv) != 4):
	usage()
	sys.exit(-1)

arrival_rate = float(sys.argv[1])
service_rate = float(sys.argv[2])
infile       =       sys.argv[3]

# Read Arrival Event
arrival_evt = read_arrival_data(infile)

allleave_evt = []
# Run Simluation
period = 1.0
for budget in [0.6, 0.7, 0.8, 0.9, 1.0]:
	(atserver_evt, leave_evt) = run_MD1_DS_server(budget, period, service_rate, arrival_evt)
	response_time = np.subtract(leave_evt, arrival_evt)
	allleave_evt.append(response_time)

