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

# For paper 3.5x2.8 for PPT 5x4
figwidth  = 3.5
figheight = 2.8
plt.figure(figsize=(figwidth, figheight))

# For paper: Enable
plt.subplots_adjust(left=0.18,top=0.95, bottom=0.18)

sample_num   = 20000
ecdf_samples = 10000
x_axis = np.linspace(0, x_lim, ecdf_samples)

for i in range(0, 3):
	if (True == ISVARBANDWIDTH):
		bandwidth = bandwidths[i]
	else:
		period    = periods[i]

	runfile   = runfiles[i]
	budget    = bandwidth * period


	scale = 100.0

	resultfile  = './data/res/' + runfile + '.csv'
	response_time = read_arrival_data(resultfile)
	response_time = np.array(response_time)
	response_time = response_time / scale 
	ecdf2 = sm.distributions.ECDF(response_time)
	y_empr_ds = ecdf2(x_axis);

	plt.plot(x_axis, y_empr_ds, linestyle=lstyles[i], color='black', drawstyle='steps', clip_on=False, linewidth=2.0)


#====================== Draw Figure ======================
if (True == ISVARBANDWIDTH):
	mytitle = "Emprical CDF: P=%.1f, %c=%.1f, %c=%.1f" % (period, u'\u03BB', arrival_rate, u'\u03BC', service_rate)
else:
	mytitle = "Emprical CDF: W=%2d%%, %c=%.1f, %c=%.1f" % (int(bandwidth * 100), u'\u03BB', arrival_rate, u'\u03BC', service_rate)

plt.xlabel('Normalized Response Time', fontsize = 12)
plt.ylabel('Proportion', fontsize = 12)
#plt.title(mytitle, fontsize = 12)
plt.xlim([0, x_lim])
plt.ylim([0, y_lim])

if (True == ISVARBANDWIDTH):
	plt.legend(['W=60%','W=80%', 'W=100%'])
	plt.savefig('./figure/syn_cdf_empr.eps', format='eps', dpi=1000)
else:
	plt.legend(['P=1.0','P=2.0', 'P=4.0'])
	plt.savefig('./figure/syn_cdf_empr_vp.eps', format='eps', dpi=1000)

plt.show()

