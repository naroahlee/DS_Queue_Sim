#!/usr/bin/python
# Sweep Lambda to show the performance
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

arrival_rates = [0.2, 0.3, 0.4, 0.5]
service_rate  = 1.0
period        = 2.0
bandwidth     = 0.6
budget    = bandwidth * period

lstyles       = [':', '-.', '-', '--']
colors        = ['blue', 'red', 'black', 'orange']
N = 20

x_lim = 20.0
y_lim = 1.0
xy_lim = (x_lim, y_lim)

# For paper 3.5x2.8 for PPT 5x4
figwidth  = 3.5
figheight = 2.8
plt.figure(figsize=(figwidth, figheight))

# For paper: Enable
plt.subplots_adjust(left=0.18,top=0.95, bottom=0.18)

for i in range(0, 4):
	(x_bd, y_bd) = get_MDDS1_from_BDDS1(arrival_rates[i], 1.0, budget, period, N)

	x_bd = x_bd[0 : int(x_lim * N)]
	y_bd = y_bd[0 : int(x_lim * N)]

	plt.plot(x_bd, y_bd, linestyle=lstyles[i], color=colors[i], drawstyle='steps', clip_on=False, linewidth=2.0)


#====================== Draw Figure ======================
#if (True == ISVARBANDWIDTH):
#	mytitle = "Numerical CDF: P=%.1f, %c=%.1f, %c=%.1f" % (period, u'\u03BB', arrival_rate, u'\u03BC', service_rate)
#else:
#	mytitle = "Numerical CDF: W=%2d%%, %c=%.1f, %c=%.1f" % (int(bandwidth * 100), u'\u03BB', arrival_rate, u'\u03BC', service_rate)

plt.xlabel('Normalized Response Time', fontsize = 12)
plt.ylabel('Proportion', fontsize = 12)
#plt.title(mytitle, fontsize = 12)
plt.xlim([0, x_lim])
plt.ylim([0, y_lim])
plt.legend([u'\u03BB'+'=0.2',u'\u03BB'+'=0.3', u'\u03BB'+'=0.4', u'\u03BB'+'=0.5'])
plt.savefig('./figure/sweep_lambda.eps', format='eps', dpi=1000)

plt.show()

