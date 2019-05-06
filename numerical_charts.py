#!/usr/bin/python
# Compare Exponential CDF between Theoretical and Emprical
import sys
import math
import numpy as np
import statsmodels.api as sm
from lib.utils           import *
from lib.arrival_process import *
from lib.server_model    import *
from lib.analytics import get_MDDS1_from_BDDS1
import matplotlib.pyplot as plt

ISVARBANDWIDTH = False

arrival_rate = 0.4
service_rate = 1.0

if (True == ISVARBANDWIDTH):
	period       = 2.0
	bandwidths   = [0.6, 0.8, 1.0]
	runfiles     = ['run01', 'run02', 'run03']
else:
	periods      = [1.0, 2.0, 4.0]
	bandwidth    = 0.6
	runfiles     = ['run05', 'run01', 'run04']

lstyles      = ['-', '--', ':']
N = 20

x_lim = 20.0
y_lim = 1.0
xy_lim = (x_lim, y_lim)

figwidth  = 6
figheight = 5
plt.figure(figsize=(figwidth, figheight))

for i in range(0, 3):
	if (True == ISVARBANDWIDTH):
		bandwidth = bandwidths[i]
	else:
		period    = periods[i]

	runfile   = runfiles[i]
	budget    = bandwidth * period

	(x_bd, y_bd) = get_MDDS1_from_BDDS1(arrival_rate, 1.0, budget, period, N)

	x_bd = x_bd[0 : int(x_lim * N)]
	y_bd = y_bd[0 : int(x_lim * N)]

	plt.plot(x_bd, y_bd, linestyle=lstyles[i], color='red', drawstyle='steps', clip_on=False, linewidth=2.0)


#====================== Draw Figure ======================
if (True == ISVARBANDWIDTH):
	mytitle = "Numerical CDF: P=%.1f, %c=%.1f, %c=%.1f" % (period, u'\u03BB', arrival_rate, u'\u03BC', service_rate)
else:
	mytitle = "Numerical CDF: W=%2d%%, %c=%.1f, %c=%.1f" % (int(bandwidth * 100), u'\u03BB', arrival_rate, u'\u03BC', service_rate)

plt.xlabel('Normalized Response Time', fontsize = 12)
plt.ylabel('Proportion', fontsize = 12)
plt.title(mytitle, fontsize = 12)
plt.xlim([0, x_lim])
plt.ylim([0, y_lim])
if (True == ISVARBANDWIDTH):
	plt.legend(['W=60%','W=80%', 'W=100%'])
else:
	plt.legend(['P=1.0','P=2.0', 'P=4.0'])

plt.show()

