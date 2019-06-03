#!/usr/bin/python
# Sweep Bandwidth to show the performance
import sys
import math
import numpy as np
import statsmodels.api as sm
from lib.utils           import *
from lib.arrival_process import *
from lib.server_model    import *
from lib.analytics import get_MDDS1_from_BDDS1
import matplotlib.pyplot as plt
import pickle

def test_plot(x_bd, y_bd_lists):
	x_lim = 0.4
	figwidth  = 3.5
	figheight = 2.8
	plt.figure(figsize=(figwidth, figheight))
	plt.subplots_adjust(left=0.18,top=0.95, bottom=0.18)

	markers = ['x', 's', 'o', '^']
	colors  = ['black', 'orange', 'blue', 'red']

	for i in [3, 2, 1, 0]:
		y_bd = y_bd_lists[i]
		plt.plot(x_bd, y_bd, marker=markers[i], linestyle='-', color=colors[i], drawstyle='default', clip_on=True, linewidth=2.0)

	plt.xlabel('Period', fontsize = 12)
	plt.ylabel('90-th Percentile Latency', fontsize = 12)
	#plt.yticks(np.arange(0, 16, 5.0))
	#plt.xlim([0.4, 1.0])
	plt.ylim([1, 7])
	plt.legend(['W=100%','W=80%', 'W=70%', 'W=60%'])

	plt.savefig('./figure/constantWsweepP.eps', format='eps', dpi=1000)
	plt.show()

def search_norm_xpercent_latency(arrival_rate, bandwidth, period, percentile, N):
	if(arrival_rate >= bandwidth):
		print "Unstable!"
		return -1

	budget = period * bandwidth
	(x_bd, y_bd) = get_MDDS1_from_BDDS1(arrival_rate, 1.0, budget, period, N)

	i = 0
	while(y_bd[i] < percentile):
		i = i + 1
	
	x = x_bd[i-1] + (x_bd[i] - x_bd[i - 1]) * (percentile - y_bd[i-1]) / (y_bd[i] - y_bd[i-1])
	print "P=[%f] W=[%f], [%2d-th] percentile latency [%f]" % (period, bandwidth, int(100 * percentile), x)

	return x
	
# =================== Search Percentile =====================
arrival_rate = 0.4
periods      = [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0]
#periods      = [1.0, 2.0]
bandwidths   = [0.60, 0.70, 0.80, 1.00]
percentile   = 0.90
N            = 20

my90th_lists = []

ISCREATENEW  = False

if (True == ISCREATENEW):
	for bandwidth in bandwidths:
		my90th = []
		for period in periods:
			x = search_norm_xpercent_latency(arrival_rate, bandwidth, period, percentile, N)
			my90th.append(x)
		my90th_lists.append(my90th)
	with open('./data/res/constWsweepP.dat', 'wb') as myfile:
		pickle.dump(my90th_lists, myfile)
else:
	with open('./data/res/constWsweepP.dat', 'rb') as myfile:
		my90th_lists = pickle.load(myfile)


test_plot(periods, my90th_lists)


