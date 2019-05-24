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
from lib.md1_cdf import MD1_response_CDF
import matplotlib.pyplot as plt

arrival_rate  = 0.4
service_durs  = 1.0
period        = 2.0
bandwidths    = [0.6, 0.8, 1.0]

lstyles       = [':', '-.', '--']
colors        = ['blue', 'red', 'orange']
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


# Generate Theoretical Curve
ecdf_samples = 10000
x_axis = np.linspace(0, x_lim, ecdf_samples)
y_theo = []
for item in x_axis:
	value = MD1_response_CDF(arrival_rate, service_durs, item)
	y_theo.append(value)

plt.plot(x_axis, y_theo, linestyle='-', color='black', drawstyle='steps', clip_on=True, linewidth=2.5)

for i in range(0, 3):

	budget    = bandwidths[i] * period
	(x_bd, y_bd) = get_MDDS1_from_BDDS1(arrival_rate, 1.0, budget, period, N)

	x_bd = x_bd[0 : int(x_lim * N)]
	y_bd = y_bd[0 : int(x_lim * N)]

	plt.plot(x_bd, y_bd, linestyle=lstyles[i], color=colors[i], drawstyle='steps', clip_on=True, linewidth=1.8)


#====================== Draw Figure ======================
plt.xlabel('Normalized Response Time', fontsize = 12)
plt.ylabel('Proportion', fontsize = 12)
#plt.title(mytitle, fontsize = 12)
plt.xlim([0, x_lim])
plt.ylim([0, y_lim])
plt.legend(['M/D/1', 'W=60%', 'W=80%', 'W=100%'])
plt.savefig('./figure/sweep_w.eps', format='eps', dpi=1000)

plt.show()

