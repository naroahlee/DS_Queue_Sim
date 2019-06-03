#!/usr/bin/python
# Compare Exponential CDF between Theoretical and Emprical
import sys
import math
import numpy as np
import statsmodels.api as sm
from lib.utils           import *
from lib.arrival_process import *
from lib.server_model    import *
from lib.analytics import get_MDPS1_from_BDPS1
import matplotlib.pyplot as plt

arrival_rate = 0.4
service_rate = 1.0
bandwidth    = 0.6
period       = 2.0
budget       = bandwidth * period
N = 20

x_lim = 20.0
y_lim = 1.0
xy_lim = (x_lim, y_lim)

(x_bd, y_bd) = get_MDPS1_from_BDPS1(arrival_rate, 1.0, budget, period, N)

x_bd = x_bd[0 : int(x_lim * N)]
y_bd = y_bd[0 : int(x_lim * N)]

#================= M/D(PS)/1 Simulation ==================
sample_num   = 20000
ecdf_samples = 10000
x_axis = np.linspace(0, x_lim, ecdf_samples)
arrival_evt = gen_poisson_process(arrival_rate, sample_num)
(atserver_evt, leave_evt) = run_D_FIFO_PS_server(budget, period, service_rate, arrival_evt)
response_time = np.subtract(leave_evt, arrival_evt)
ecdf2 = sm.distributions.ECDF(response_time);
y_empr_ps = ecdf2(x_axis);

#====================== Draw Figure ======================
mytitle = "Response Time CDF: P=%.1f, Bw=%2d%%, %c=%.1f, %c=%.1f" % (period, int(bandwidth * 100), u'\u03BB', arrival_rate, u'\u03BC', service_rate)

figwidth  = 6
figheight = 5
plt.figure(figsize=(figwidth, figheight))
plt.plot(x_axis, y_empr_ps, linestyle='-', color='blue', drawstyle='steps', clip_on=False, linewidth=2.8)
plt.plot(x_bd, y_bd, linestyle='--', color='orange', drawstyle='steps', clip_on=False, linewidth=2.0)
plt.xlabel('Normalized Response Time', fontsize = 12)
plt.ylabel('Proportion', fontsize = 12)
plt.title(mytitle, fontsize = 12)
plt.xlim([0, x_lim])
plt.ylim([0, y_lim])
plt.legend(['M/D(PS)/1 Sim','B/D(PS)/1 approx N=%d' % (N)])

plt.show()

