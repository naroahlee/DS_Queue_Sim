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
