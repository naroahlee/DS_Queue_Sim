#!/usr/bin/python
# Compare Exponential CDF between Theoretical and Emprical
import sys
import math
import numpy as np
import statsmodels.api as sm
from lib.utils           import *
from lib.arrival_process import *
from lib.server_model    import *
from lib.md1_cdf import MD1_response_CDF

# ================Parameters ===============
# For Poisson Process

sample_num   = 100000
utilization  = 0.5
service_rate = 1.0
arrival_rate = utilization * service_rate

tail_perc    = 90



# Figure Plot Parameter
x_lim = 20.0
y_lim = 1.0
xy_lim = (x_lim, y_lim)


# Generate Emprical Samples
arrival_evt = gen_poisson_process(arrival_rate, sample_num)

#=============== Simulation ================
# Stimulate the server
(atserver_evt, leave_evt) = run_D_FIFO_server(service_rate, arrival_evt)
response_time        = np.subtract(leave_evt, arrival_evt)
ref_tail = np.percentile(response_time, tail_perc)

# For D_FIFO_DS server
bandwidth    = 0.8
period       = 1.0

ds_tails = []
x_axis1 = np.multiply(range(1, 10), 0.1)
x_axis2 = np.multiply(range(1, 21), 1.0)
x_axis = np.append(x_axis1, x_axis2)
for period in x_axis:
	budget       = bandwidth * period
	(atserver_evt, leave_evt) = run_D_FIFO_DS_server(budget, period, service_rate, arrival_evt)
	response_time_DS = np.subtract(leave_evt, arrival_evt)
	temp_tail = np.percentile(response_time_DS, tail_perc)
	ds_tails.append(temp_tail)

figwidth  = 6
figheight = 5
plt.figure(figsize=(figwidth, figheight))

# Disable The Frame
spinelist = plt.gca().spines.values()
spinelist[1].set_visible(False)
spinelist[3].set_visible(False)

# Don't Clip_on
plt.subplots_adjust(left=0.18,top=0.90, bottom=0.2)

plt.plot(x_axis, ds_tails, linestyle='-', clip_on=False, linewidth=2.0)

plt.plot([0, max(x_axis)], [ref_tail, ref_tail], linestyle='-', color='black', clip_on=False, linewidth=2.0)

plt.xlabel('VCPU Period', fontsize = 12)
plt.ylabel(" %d th Tail Latency" % (tail_perc), fontsize = 12)
mytitle = "Bw=%2d%%, U=%2d%%, %c=%.1f" % (int(bandwidth * 100), int(utilization * 100), u'\u03BC', service_rate)
plt.title(mytitle, fontsize = 12)

#(x_lim, y_lim) = xy_lim
plt.xlim([0, 20])
plt.legend(['Highest Priority VCPU', 'Full CPU (M/D/1)'])
plt.show()

