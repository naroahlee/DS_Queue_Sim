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

GEN_NEW_DATA = False
# Real Value
arrival_rate_real = 0.04
service_dur_real  = 8.6
period_real       = 10.0
bandwidth         = 0.6

# Normalization
arrival_rate = arrival_rate_real * service_dur_real
service_rate = 1.0
period       = period_real / service_dur_real
budget       = period * bandwidth

GEN_NEW_DATA = False

N = 60

runfile='redis_sort'

x_lim = 20.0
y_lim = 1.0
xy_lim = (x_lim, y_lim)

#================= M/D(DS)/1 Theoretical ==================
(x_bd, y_bd) = get_MDDS1_from_BDDS1(arrival_rate, 1.0, budget, period, N)

x_bd = x_bd[0 : int(x_lim * N)]
y_bd = y_bd[0 : int(x_lim * N)]

#================= M/D(DS)/1 Simulation ==================
scale_when_doing_exp_in_ms = 10.0
sample_num   = 20000
ecdf_samples = 10000
x_axis = np.linspace(0, x_lim, ecdf_samples)
#
## Record the Data
processfile  = './data/input/' + runfile + '.csv'
#
if (True == GEN_NEW_DATA):
	arrival_evt = gen_poisson_process(arrival_rate, sample_num)
	write_arrival_data(processfile, arrival_evt)
else:
	arrival_evt = read_arrival_data(processfile)

arrival_evt = np.array(arrival_evt)
arrival_evt = arrival_evt * scale_when_doing_exp_in_ms / service_dur_real

(atserver_evt, leave_evt) = run_D_FIFO_DS_server(budget, period, service_rate, arrival_evt)
response_time = np.subtract(leave_evt, arrival_evt)
ecdf2 = sm.distributions.ECDF(response_time)
y_simu_ds = ecdf2(x_axis);

#================= M/D(DS)/1 Empirical ==================
scale = 10.0

resultfile  = './data/res/' + runfile + '.csv'
response_time = read_arrival_data(resultfile)
response_time = np.array(response_time)
response_time = response_time / scale 
ecdf2 = sm.distributions.ECDF(response_time)
y_empr_ds = ecdf2(x_axis);

#====================== Draw Figure ======================
mytitle = "Response Time CDF: P=%.2f, W=%2d%%, %c=%.2f, %c=%.2f" % (period, int(bandwidth * 100), u'\u03BB', arrival_rate, u'\u03BC', service_rate)

figwidth  = 6
figheight = 5
plt.figure(figsize=(figwidth, figheight))
plt.plot(x_axis, y_simu_ds, linestyle='--', color='blue', drawstyle='steps', clip_on=False, linewidth=2.0)
plt.plot(x_bd, y_bd, linestyle='--', color='red', drawstyle='steps', clip_on=False, linewidth=2.0)
plt.plot(x_axis, y_empr_ds, linestyle='--', color='black', drawstyle='steps', clip_on=False, linewidth=2.0)
plt.xlabel('Normalized Response Time', fontsize = 12)
plt.ylabel('Proportion', fontsize = 12)
plt.title(mytitle, fontsize = 12)
plt.xlim([0, x_lim])
plt.ylim([0, y_lim])
plt.legend(['Simulation', 'Numerical approx N=%d' % (N), 'Redis Empr'])
#plt.legend(['M/D(DS)/1 Sim','B/D(DS)/1 approx N=%d' % (N), 'M/D(DS)/1 Empr'])

plt.show()

