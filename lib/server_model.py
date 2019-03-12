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

	next_period   = period + offset;
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

# ====== Deterministic FIFO Saving Server Model ================
# This is a modification based on deferrable server: enable carry-over
# Server Parameters:
#   service rate: i.e. \mu whose inverse is the service_duration
#   (budget, period, saving): Saving Server Parameter
# 
# in this design, the remain_budget is no longer caped by expensible 
# amount of current period

# deposit_with cap
def deposit_saving(saving, remain_saving, deposit_amt):
	new_saving = remain_saving + deposit_amt
	if (new_saving >= saving):
		return saving
	else:
		return new_saving

# Everytime when execute or idle for sometime, we need to update the status of SS
# Most likely, the saving will change
def update_SS_after_idle(budget,        period,      saving, 
                         remain_budget, next_period, remain_saving,
                         cur_time):
	if (cur_time >= next_period):
		# Step 1. Refill Saving
		# Deposit the remain_budget of the first period
		remain_saving = deposit_saving(saving, remain_saving, remain_budget)
		future_period = (math.floor(cur_time / period) + 1) * period
		# How many intact "end_of_period" do we pass?
		# Deposit m * budget into the saving account
		m = round((future_period - next_period) / period) - 1
		remain_saving = deposit_saving(saving, remain_saving, m * budget)
		# =======================	

		# Step 2. Update the next_period
		next_period = future_period
		remain_budget = budget
		
	return (remain_budget, remain_saving, next_period)

def get_max_burnable(remain_budget, remain_saving, next_period, cur_time):
	# max_burnable will be caped 
	max_burnable = next_period - cur_time

	# Avaliable budget (taking saving into consideration)
	all_remain   = remain_budget + remain_saving 
	if(all_remain >= max_burnable):
		return max_burnable
	else:
		return all_remain

def burn_budget(remain_budget, remain_saving, service_dur):
	# Priority: Burn Budget first
	if(service_dur > remain_budget):
		remain_saving -= (service_dur - remain_budget)
		remain_budget = 0.0;
	else:
		remain_budget -= service_dur
	return (remain_budget, remain_saving)


# Deterministic Saving Server
def run_D_FIFO_SS_server(budget, period, saving, service_rate, arrival_evt):
	service_dur  = 1.0 / service_rate

	atserver_evt = []
	leave_evt    = []

	index = 0

	# Give full budget, full saving at start
	state = 0; # IDLE
	cur_time = 0.0;
	remain_budget = budget
	next_period   = period
	remain_saving = saving

	while (index < len(arrival_evt)):
		if(0 == state): # IDLE
			cur_time = arrival_evt[index]
			(remain_budget, remain_saving, next_period) = update_SS_after_idle(budget, period, saving, remain_budget, next_period, remain_saving, cur_time)
			state = 1 
		if(1 == state): # Execution
			while((index < len(arrival_evt)) and (cur_time >= arrival_evt[index])):
				atserver_evt.append(cur_time)

				# Core fxn: burn budget
				max_burnable = get_max_burnable(remain_budget, remain_saving, next_period, cur_time)

				# If current period can still handle
				if(max_burnable >= service_dur): 
					cur_time += service_dur
					(remain_budget, remain_saving) = burn_budget(remain_budget, remain_saving, service_dur)
					# next_period = next_period   # next_period unchanged

				# If we need more than current period to handle
				else:
					# First, burn up all the remain debris
					# In this case, should be max_burnable
					(remain_budget, remain_saving) = burn_budget(remain_budget, remain_saving, max_burnable)
					service_remain = service_dur - max_burnable
					# At the end of current period, deposit remain_budget to saving
					remain_saving = deposit_saving(saving, remain_saving, remain_budget)

					# Update Time slot
					cur_time = next_period
					next_period += period
					remain_budget = budget # budget replenish
					
					# Use Multiple whole SS period for serving
					# Yes, you can directly compute it if you want
					max_burnable = get_max_burnable(remain_budget, remain_saving, next_period, cur_time)
					while(service_remain > max_burnable): 
						(remain_budget, remain_saving) = burn_budget(remain_budget, remain_saving, max_burnable)
						service_remain -= max_burnable

						cur_time = next_period
						next_period += period
						remain_budget = budget # budget replenish
						max_burnable = get_max_burnable(remain_budget, remain_saving, next_period, cur_time)

					# Now the last potion of service_remain is less than max_burnable:
					# We should burn: service_remain
					cur_time += service_remain
					(remain_budget, remain_saving) = burn_budget(remain_budget, remain_saving, service_remain)

				leave_evt.append(cur_time);
				index += 1
			state = 0

	return (atserver_evt, leave_evt)

# ====== Deterministic FIFO Deferrable Server in Discrete Time Model ==========
# Server Parameters:
# service rate: i.e. \mu whose inverse is the service_duration
# (budget, period): Deferrable Server Parameter

# Everytime when execute or idle for sometime, we need to update the status of DS
def update_DS_after_idle_DT(budget, period, remain_budget, next_period, cur_time):
	if (cur_time >= next_period): # Now it's a new period
		next_period   = ((cur_time / period) + 1) * period
		remain_budget = budget	  # New Period with budget replenishment

	# Regardless of new or old period: budget cap is max_remain
	max_remain = next_period - cur_time
	if (remain_budget > max_remain):
		remain_budget = max_remain	
	
	return (remain_budget, next_period)

# Deterministic Deferrable Server
def run_D_FIFO_DS_server_DT(budget, period, service_dur, arrival_evt):
	# Sanity Check
	assert(int(budget) == budget)
	assert(int(period) == period)
	assert(int(service_dur) == service_dur)
	for item in arrival_evt:
		assert(int(item) == item)

	atserver_evt = []
	leave_evt    = []

	index = 0

	state = 0; # IDLE
	cur_time = 0;
	remain_budget = budget;
	next_period   = period;
	while (index < len(arrival_evt)):
		if(0 == state): # IDLE
			cur_time = arrival_evt[index]
			(remain_budget, next_period) = update_DS_after_idle_DT(budget, period, remain_budget, next_period, cur_time)
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

# ====== Deterministic FIFO Perodic Server Model Discrete Time ==========
# Server Parameters:
# service rate: i.e. \mu whose inverse is the service_duration
# (budget, period): Deferrable Server Parameter
# In simulation, I will set the Offset as P-B,
# so the Periodic Server can represent a worst case senario of a Deferrable Server

def run_D_FIFO_PS_server_DT(budget, period, service_dur, arrival_evt):
	# Sanity Check
	assert(int(budget) == budget)
	assert(int(period) == period)
	assert(int(service_dur) == service_dur)
	for item in arrival_evt:
		assert(int(item) == item)

	atserver_evt = []
	leave_evt    = []

	index = 0

	state = 0; # IDLE

	# Set the initial Offset = P - B
	offset = period - budget
	cur_time = offset;

	next_period   = period + offset;
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
