#!/usr/bin/python
# Run M/G(DS)/1 Simulation
import sys
import math
import numpy as np
import statsmodels.api as sm
from lib.utils           import *
from lib.arrival_process import *
from lib.server_model    import *
from lib.md1_cdf import MD1_response_CDF
from lib.analytics import get_dist_from_exec
from lib.analytics import get_MDDS1_from_BDDS1
from lib.analytics import get_MGDS1_from_BGDS1

# ================Parameters ===============
NEWARRIVAL = False

# For DS server
#bandwidth    = 0.6
budget       = 1.4
period       = 2.0
#budget       = bandwidth * period

# For Poisson arrival
arrival_rate = 0.50
sample_num   = 20000

# For Gaussian Execution
g_mean  = 1.0
g_sqvar = 0.3


# Figure Plot Parameter
ecdf_samples = 10000
x_lim = 20.0
y_lim = 1.0
xy_lim = (x_lim, y_lim)
x_axis = np.linspace(0, x_lim, ecdf_samples)

# Logs
processfile  = './data/input/MGDS1_arrival.csv'
executefile  = './data/input/MGDS1_execute.csv'
resultfile   = './data/res/MGDS1_synth.csv'
if (True == NEWARRIVAL):
	arrival_evt = gen_poisson_process(arrival_rate, sample_num)
	execute_dur = np.random.normal(g_mean, g_sqvar, sample_num)
else:
	arrival_evt = read_arrival_data(processfile)
	execute_dur = read_arrival_data(executefile)

#=============== Simulation M/G(DS)/1 ================
# Generate Emprical Samples
# Stimulate the server
(atserver_evt, leave_evt) = run_G_FIFO_DS_server(budget, period, execute_dur, arrival_evt)
response_time = np.subtract(leave_evt, arrival_evt)
ecdf = sm.distributions.ECDF(response_time)
y_simu = ecdf(x_axis);

#=============== Empirical M/G(DS)/1 =================
response_time = read_arrival_data(resultfile)
response_time = np.array(response_time)
response_time = response_time / 100.0
print max(response_time)
ecdf          = sm.distributions.ECDF(response_time)
y_empr        = ecdf(x_axis);




#=============== Simulation M/G/1 ================
# Generate Emprical Samples
# Stimulate the server
#(atserver_evt, leave_evt) = run_G_FIFO_server(arrival_evt, execute_dur)
#response_time = np.subtract(leave_evt, arrival_evt)
#ecdf = sm.distributions.ECDF(response_time)
#y_simu2 = ecdf(x_axis);


#=============== Analytical: M/G(DS)/1 ===============
# Step 1. Get exe_dist
N_arr = 20
N_exe = 20
exe_dist = get_dist_from_exec(execute_dur, N_exe, N_arr)
(x_bg, y_bg) = get_MGDS1_from_BGDS1(arrival_rate, exe_dist, budget, period, N_arr)

#=============== Analytical: M/D(DS)/1 ===============
#N_arr = 20
#(x_bd, y_bd) = get_MDDS1_from_BDDS1(arrival_rate, 1.0, budget, period, N_arr)

if (True == NEWARRIVAL):
	write_arrival_data(processfile, arrival_evt)
	write_arrival_data(executefile, execute_dur)


# ============= Draw Figure =============== 
figwidth  = 5
figheight = 4
plt.figure(figsize=(figwidth, figheight))
#plt.plot(x_axis, y_simu2, linestyle='-', color='black', drawstyle='steps', clip_on=True, linewidth=2.0)
plt.plot(x_axis, y_empr, linestyle='-', color='black', drawstyle='steps', clip_on=True, linewidth=2.2)
plt.plot(x_axis, y_simu, linestyle=':', color='blue', drawstyle='steps', clip_on=True, linewidth=1.8)
plt.plot(x_bg  , y_bg  , linestyle='--', color='red', drawstyle='default', clip_on=True, linewidth=2.0)
#plt.plot(x_bd  , y_bd  , linestyle='--', color='green', drawstyle='steps', clip_on=True, linewidth=2.0)
plt.xlabel('Normalized Response Time', fontsize = 12)
plt.ylabel('Proportion', fontsize = 12)
mytitle = '%c=%3.2f, d=%.1f, %c=%.1f P=%.1f, B=%.1f' % (u'\u03BB', arrival_rate, g_mean, u'\u03C3', g_sqvar, period, budget)
plt.title(mytitle)
plt.xlim([0, 15])
plt.ylim([0, y_lim])
#plt.legend(['M/G/1 Simu', 'M/G(DS)/1 Simu', 'M/G(DS)/1 Numer', 'M/D(DS)/1 Numer'])
plt.legend(['M/G(DS)/1 Empr', 'M/G(DS)/1 Simu', 'M/G(DS)/1 Numer'])
#plt.legend(['M/G(DS)/1 Simu', 'M/G(DS)/1 Empr'])
plt.show()
