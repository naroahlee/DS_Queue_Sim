#!/usr/bin/python
# Arrival Process Generator
# Now support Poisson Process (inter-arrival time ~ exponential distribution)
import numpy as np

# ============== Poisson Process =====================
# Parameters:
# arrival_rate: \lambda
def gen_poisson_process(arrival_rate, sample_num):
	beta = 1.0 / arrival_rate
	alldata = np.random.exponential(beta, sample_num)

	arrival_evt = []
	cur_time = 0.0
	for evt in alldata:
		cur_time += evt
		arrival_evt.append(cur_time)

	return arrival_evt

# ============= Bernoulli Process ===================
# Parameters:
# arrival possibility in a slot: p

def gen_bernoulli_process(p, sample_num):
	alldata = np.random.geometric(p, sample_num)

	arrival_evt = []
	cur_time = 0
	for evt in alldata:
		cur_time += evt
		arrival_evt.append(cur_time)

	return arrival_evt

def gen_binary_distribution_execution(a, b, pa, sample_num):
	alldata = np.random.uniform(0, 100, sample_num)
	for i in range(0, len(alldata)):
		if (alldata[i] < pa * 100.0):
			alldata[i] = a
		else:
			alldata[i] = b
	return alldata

