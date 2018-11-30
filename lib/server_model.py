#!/usr/bin/python
# Server Models
# Now we have three model
# 1. Deterministic FIFO Model
# 2. Deterministic FIFO Deferrable Server Model
# 3. Deterministic FIFO Periodic   Server Model
#    Note, A highest priority periodic server with offset 
#    of P-B can be the worst case senario of a schedulable corresponding Deferrable Server in terms of total waiting time 
# Stimulate the server with an arrival_evt;
# We can get when each job starts getting service
#    and when each job leaves

import math
import numpy as np

# ================ Deterministic FIFO Model ==================
# Server Parameters:
# service rate: i.e. \mu whose inverse is the service_duration
def run_D_FIFO_server(service_rate, arrival_evt):
	service_dur  = 1.0 / service_rate

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

	return (atserver_evt, leave_evt)

# ====== Deterministic FIFO Deferrable Server Model ==========
# Server Parameters:
# service rate: i.e. \mu whose inverse is the service_duration
# (budget, period): Deferrable Server Parameter

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
def run_D_FIFO_DS_server(budget, period, service_rate, arrival_evt):
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

# ====== Deterministic FIFO Perodic Server Model ==========
# Server Parameters:
# service rate: i.e. \mu whose inverse is the service_duration
# (budget, period): Deferrable Server Parameter
# In simulation, I will set the Offset as P-B,
# so the Periodic Server can represent a worst case senario of a Deferrable Server

def run_D_FIFO_PS_server(budget, period, service_rate, arrival_evt):
	service_dur  = 1.0 / service_rate

	atserver_evt = []
	leave_evt    = []

	index = 0

	state = 0; # IDLE

	# Set the initial Offset = P - B
	offset = period - budget
	cur_time = offset;

	next_period   = period;
	while (index < len(arrival_evt)):
		if(0 == state): # IDLE
			cur_time = arrival_evt[index]
			if(cur_time <= offset):			# Align the fist period
				cur_time = offset

			while(cur_time >= next_period): # Update Period Based on Cur_time
				next_period += period

			# Check which phase cur_time in a period: available or N/A
			if(cur_time >= (next_period - period + budget)): # Not available, miss the first B time of current period
				cur_time = next_period
				next_period += period

			state = 1 

		if(1 == state): # Execution
			while((index < len(arrival_evt)) and (cur_time >= arrival_evt[index])):
				atserver_evt.append(cur_time);

				remain_budget = (next_period - period + budget) - cur_time
				if(remain_budget >= service_dur): # If old period can still handle
					cur_time += service_dur
					# next_period = next_period   # next_period unchanged
				else:
					# First, burn up all the remain debris
					cur_time = next_period	# Uneven Budget Replenishment
					next_period += period
					service_remain = service_dur - remain_budget
					
					# Use Multiple whole PS period for serving
					# Yes, you can directly compute it if you want
					while(service_remain > budget): 
						cur_time = next_period
						next_period += period
						service_remain -= budget

					# Now the last potion of service_remain is less than budget:
					cur_time += service_remain

				leave_evt.append(cur_time);
				index += 1
			state = 0

	return (atserver_evt, leave_evt)
