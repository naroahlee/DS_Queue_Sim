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
#budget       = 2.4
budget       = 3.2
period       = 4.0
#budget       = bandwidth * period

# For Poisson arrival
arrival_rate = 0.30
sample_num   = 20000

# For Gaussian Execution
g_mean  = 2.0

# Figure Plot Parameter
ecdf_samples = 10000
x_lim = 20.0
y_lim = 1.0
xy_lim = (x_lim, y_lim)
x_axis = np.linspace(0, x_lim, ecdf_samples)

# Logs
arrivalfile  = './data/input/MGDS1_flink_arrival.csv'
executefile  = './data/res/flink_exe_calib.csv'
resultfile   = './data/res/flink_exe_full.csv'
resultfile2  = './data/res/flink_exe_p4s.csv'

execute_dur = read_arrival_data(executefile)
#execute_dur = np.random.normal(myavg, 2 * mystd, sample_num)

#=============== Empirical M/G/1 =================
response_time = read_arrival_data(resultfile)
response_time = np.array(response_time)
response_time = response_time / 1000.0
ecdf          = sm.distributions.ECDF(response_time)
y_empr        = ecdf(x_axis);

#=============== Empirical M/G(DS)/1 =================
response_time = read_arrival_data(resultfile2)
response_time = np.array(response_time)
response_time = response_time / 1000.0
ecdf          = sm.distributions.ECDF(response_time)
y_empr2       = ecdf(x_axis);

#=============== Analytical: M/G(DS)/1 ===============
# Step 1. Get exe_dist

# Normalized
execute_dur_n  = np.array(execute_dur)
execute_dur_n  = execute_dur_n / g_mean
arrival_rate_n = arrival_rate * g_mean
budget_n = budget / g_mean
period_n = period / g_mean

N_arr = 20
N_exe = 20
exe_dist = get_dist_from_exec(execute_dur_n, N_exe, N_arr)
(x_bg_n, y_bg) = get_MGDS1_from_BGDS1(arrival_rate_n, exe_dist, budget_n, period_n, N_arr)

# Denormalized
x_bg = x_bg_n * g_mean

(x_bg1_n, y_bg1) = get_MGDS1_from_BGDS1(arrival_rate_n, exe_dist, period_n, period_n, N_arr)
x_bg1 = x_bg1_n * g_mean

# ============= Draw Figure =============== 
figwidth  = 5
figheight = 4
plt.figure(figsize=(figwidth, figheight))
plt.plot(x_axis, y_empr, linestyle='-', color='blue', drawstyle='steps', clip_on=True, linewidth=2.0)
plt.plot(x_bg1 , y_bg1 , linestyle=':', color='blue', drawstyle='default', clip_on=True, linewidth=2.0)

plt.plot(x_axis, y_empr2, linestyle='-', color='red', drawstyle='steps', clip_on=True, linewidth=2.0)
plt.plot(x_bg  , y_bg  , linestyle=':', color='red', drawstyle='default', clip_on=True, linewidth=2.0)
plt.xlabel('Response Time (s)', fontsize = 12)
plt.ylabel('Proportion', fontsize = 12)
mytitle = '%c=%3.2f, d=%.1f, P=%.1f, B=%.1f' % (u'\u03BB', arrival_rate, g_mean, period, budget)
plt.title(mytitle)
plt.xlim([0, x_lim])
plt.ylim([0, y_lim])
plt.legend(['M/G/1 Empr', 'M/G/1 Numer', 'M/G(DS)/1 Empr', 'M/G(DS)/1 Numer'])
plt.show()
