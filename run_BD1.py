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

# ================Parameters ===============
# For Bernoulli Process
p = 0.35
sample_num   = 20

# For imbedded queue server, service_time = 1
service_dur = 1

# DS:
budget = 2
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
print arrival_evt

write_arrival_data(processfile, arrival_evt)

# Stimulate the server
#(atserver_evt, leave_evt) = run_D_FIFO_DS_server_DT(budget, period, service_dur, arrival_evt)


#print "DS Departure Time"
#print leave_evt

#print "DS Response  Time"
#response_time = np.subtract(leave_evt, arrival_evt)
#print response_time

(atserver_evt, leave_evt) = run_D_FIFO_PS_server_DT(budget, period, service_dur, arrival_evt)

print "PS Departure Time"
print leave_evt


print "PS Response  Time"
response_time = np.subtract(leave_evt, arrival_evt)
print response_time
