#!/usr/bin/python
# Compare Exponential CDF between Theoretical and Emprical
import sys
import numpy as np
from lib.utils import *

def usage():
	print "MD1_sim.py [Service_Rate] [Input File] [Out File]"
	return

# Deterministic Server
def run_MD1_server(service_rate, arrival_evt):
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


# ================= Main ===================

if (len(sys.argv) != 4):
	usage()
	sys.exit(-1)

service_rate = float(sys.argv[1])
infile       = sys.argv[2]
outfile      = sys.argv[3]

# Read Arrival Event
arrival_evt = read_arrival_data(infile)

# Run Simluation
(atserver_evt, leave_evt) = run_MD1_server(service_rate, arrival_evt)

# Save Event
write_trace_data(outfile, arrival_evt, atserver_evt, leave_evt)
