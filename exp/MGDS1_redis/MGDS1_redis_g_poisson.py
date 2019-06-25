#!/usr/bin/python
# Run M/G(DS)/1 Simulation for redis sort
import sys
import math
import numpy as np
import statsmodels.api as sm
from lib.utils           import *
from lib.arrival_process import *
from lib.server_model    import *
from lib.md1_cdf import MD1_response_CDF
from lib.analytics import get_dist_from_exec
from lib.analytics import get_dist_from_exec_with_d
from lib.analytics import get_MDDS1_from_BDDS1
from lib.analytics import get_MGDS1_from_BGDS1

# ================Parameters ===============
NEWARRIVAL = False

# For DS server
#bandwidth    = 0.6
budget       = 2.4
period       = 4.0
#budget       = bandwidth * period

# For Poisson arrival
arrival_rate = 0.40
sample_num   = 10000

# Figure Plot Parameter
ecdf_samples = 10000
x_lim = 20.0
y_lim = 1.0
xy_lim = (x_lim, y_lim)
x_axis = np.linspace(0, x_lim, ecdf_samples)

# Logs
processfile  = './data/input/redis_g_arrival.csv'
#arrival_evt = gen_poisson_process(arrival_rate, sample_num)
arrival_evt = read_arrival_data(processfile)

executefile  = './data/res/redis_g_calib.csv'
execute_dur = read_arrival_data(executefile)
execute_dur = np.array(execute_dur)
execute_dur = execute_dur / 10.0
#mymean = np.mean(execute_dur)
#execute_dur = execute_dur / mymean

#=============== Simulation ================
# Generate Emprical Samples
# Stimulate the server
(atserver_evt, leave_evt) = run_G_FIFO_DS_server(budget, period, execute_dur, arrival_evt)
response_time = np.subtract(leave_evt, arrival_evt)
ecdf = sm.distributions.ECDF(response_time)
y_simu = ecdf(x_axis);

#=============== Empirical M/G(DS)/1 =================
resultfile  = './data/res/redis_g_partial.csv'
response_time = read_arrival_data(resultfile)
response_time = np.array(response_time)
response_time = response_time / 10.0
ecdf          = sm.distributions.ECDF(response_time)
y_empr        = ecdf(x_axis);


#=============== Analytical: M/G(DS)/1 ===============
# Step 1. Get exe_dist
N_arr = 20
N_exe = 20
exe_dist = get_dist_from_exec_with_d(execute_dur, 1.0 ,N_exe, N_arr)
(x_bg, y_bg) = get_MGDS1_from_BGDS1(arrival_rate, exe_dist, budget, period, N_arr)


write_arrival_data(processfile, arrival_evt)

# ============= Draw Figure =============== 
figwidth  = 5
figheight = 4
plt.figure(figsize=(figwidth, figheight))
#plt.plot(x_axis, y_simu, linestyle='-', color='blue', drawstyle='steps', clip_on=True, linewidth=2.0)
plt.plot(x_axis, y_empr, linestyle='-', color='black', drawstyle='steps', clip_on=True, linewidth=2.2)
plt.plot(x_bg  , y_bg  , linestyle='--', color='blue', drawstyle='default', clip_on=True, linewidth=2.0)
plt.xlabel('Normalized Response Time', fontsize = 12)
plt.ylabel('Proportion', fontsize = 12)
#mytitle = 'Redis %c=%3.2f, d=%.1f, %c=%.1f P=%.1f, B=%.1f' % (u'\u03BB', arrival_rate, g_mean, u'\u03C3', g_sqvar, period, budget)
#plt.title(mytitle)
plt.xlim([0, 20])
plt.ylim([0, y_lim])
plt.legend(['M/G(DS)/1 Empr', 'M/G(DS)/1 Numer'])
plt.show()
