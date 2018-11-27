#!/usr/bin/python
# Compare Exponential CDF between Theoretical and Emprical
import matplotlib.pyplot as plt
import numpy as np
import csv
import sys

def usage():
	print "MD1_sim.py [Service_Rate] [Input File] [Out File]"
	return

def read_arrival_data(infile):
	arrival_evt = []
	with open(infile, 'rb') as csvfile:
		myreader = csv.reader(csvfile, delimiter=',', quotechar='|')
		for row in myreader:
			for item in row:
				arrival_evt.append(float(item));
	return arrival_evt

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
with open(outfile, 'w') as outfile:
	for index in range(0, len(arrival_evt)):
		outfile.write('%f,%f,%f\n' % (arrival_evt[index], atserver_evt[index], leave_evt[index]))





