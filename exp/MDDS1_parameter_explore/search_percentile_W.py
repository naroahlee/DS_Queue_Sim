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

	markers = ['x', 'x', 'o', '^']
	colors  = ['black', 'black', 'blue', 'red']

	for i in [3, 2, 0]:
		y_bd = y_bd_lists[i]
		plt.plot(x_bd, y_bd, marker=markers[i], linestyle='-', color=colors[i], drawstyle='default', clip_on=True, linewidth=2.0)

	plt.xlabel('Bandwidth', fontsize = 12)
	plt.ylabel('90-th Percentile Latency', fontsize = 12)
	plt.yticks(np.arange(0, 16, 5.0))
	plt.xlim([0.4, 1.0])
	plt.ylim([0, 15])
	plt.legend(['P=8.0','P=4.0', 'P=1.0'])

	plt.savefig('./figure/constantPsweepW.eps', format='eps', dpi=1000)
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
periods      = [1.0, 2.0, 4.0, 8.0]
#periods      = [1.0, 2.0]
bandwidths   = [0.45, 0.50, 0.55, 0.60, 0.65, 0.70, 0.75, 0.80, 0.85, 0.90, 0.95, 1.00]
percentile   = 0.90
N            = 20

my90th_lists = []

ISCREATENEW  = False

if (True == ISCREATENEW):
	for period in periods:
		my90th = []
		for bandwidth in bandwidths:
			x = search_norm_xpercent_latency(arrival_rate, bandwidth, period, percentile, N)
			my90th.append(x)
		my90th_lists.append(my90th)
	with open('./data/res/constPsweepW.dat', 'wb') as myfile:
		pickle.dump(my90th_lists, myfile)
else:
	with open('./data/res/constPsweepW.dat', 'rb') as myfile:
		my90th_lists = pickle.load(myfile)

test_plot(bandwidths, my90th_lists)


