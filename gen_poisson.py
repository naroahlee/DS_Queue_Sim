#!/usr/bin/python
# Compare Exponential CDF between Theoretical and Emprical
import matplotlib.pyplot as plt
import numpy as np
import csv
import sys

def usage():
	print "gen_possion.py [Rate] [#Sample] [Filename]"
	return

def gen_poisson_process(arrival_rate, sample_num):
	beta = 1.0 / arrival_rate
	alldata = np.random.exponential(beta, sample_num)

	arrival_evt = []
	cur_time = 0.0
	for evt in alldata:
		cur_time += evt
		arrival_evt.append(cur_time)

	return arrival_evt


# ================= Main ===================

if (len(sys.argv) != 4):
	usage()
	sys.exit(-1)

arrival_rate = float(sys.argv[1])
sample_num   =   int(sys.argv[2])
filename     = sys.argv[3]

# Generate Emprical Samples
arrival_evt = gen_poisson_process(arrival_rate, sample_num)

# Save to CSV
with open(filename, 'w') as outfile:
	for item in arrival_evt:
		outfile.write('%f\n' % (item))
 

