#!/usr/bin/python
# Compare Exponential CDF between Theoretical and Emprical
import sys
import math
import numpy as np
import statsmodels.api as sm
from lib.utils           import *
from lib.arrival_process import *
from lib.server_model    import *
from lib.md1_cdf import MD1_response_CDF
from lib.analytics import get_BD1_V0

# ================Parameters ===============
# For Bernoulli Process
p = 0.5
sample_num   = 100000

# For imbedded queue server, service_time = 1
service_dur = 1

# Server:
budget = 3
period = 5

# Logs
processfile  = './data/input/run01.csv'
resultfile   = './data/output/run01.csv'


#=============== Simulation ================
# Generate Emprical Samples
# Bernoulli Process
arrival_evt = gen_bernoulli_process(p, sample_num)
# arrival_evt = read_arrival_data(processfile)
print "Arrival   Time"
#print arrival_evt

write_arrival_data(processfile, arrival_evt)

queuing_proc = [0]
current_qlen = 0
next_period  = period
index = 0
while(index < len(arrival_evt)):
	arrival_cnt = 0
	while (index < len(arrival_evt) and arrival_evt[index] < next_period):
		index += 1
		arrival_cnt += 1
	current_qlen = max([0, current_qlen + arrival_cnt - budget])

	queuing_proc.append(current_qlen)
	next_period += period

#print queuing_proc
cnt = [0] * 20
for item in queuing_proc:
	if (item < 20):
		cnt[item] += 1

pi_j = get_BD1_V0(budget, period, p)

print "         Simulation   Analytical(Numerical)"
for i in range(0, len(cnt)):
	print "pi%2d = %12.8f   %12.8f" % (i, 100.0 * cnt[i] / len(queuing_proc), 100.0 * pi_j[i])


#for i in range(0, 10):
#	print "pi%2d/pi%2d = %12.8f" % (i+1, i, (float(cnt[i+1]) / cnt[i]))





# ==================================================================
# Stimulate the server
#(atserver_evt, leave_evt) = run_D_FIFO_DS_server_DT(budget, period, service_dur, arrival_evt)


#print "DS Departure Time"
#print leave_evt

#print "DS Response  Time"
#response_time = np.subtract(leave_evt, arrival_evt)
#print response_time

#(atserver_evt, leave_evt) = run_D_FIFO_PS_server_DT(budget, period, service_dur, arrival_evt)

#print "PS Departure Time"
#print leave_evt


#print "PS Response  Time"
#response_time = np.subtract(leave_evt, arrival_evt)
#print response_time
