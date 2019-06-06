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
if (True == NEWARRIVAL):
	arrival_evt = gen_poisson_process(arrival_rate, sample_num)
	execute_dur = np.random.normal(g_mean, g_sqvar, sample_num)
else:
	arrival_evt = read_arrival_data(processfile)
	execute_dur = read_arrival_data(executefile)
#resultfile   = './data/res/redis_sort.csv'

#=============== Simulation ================
# Generate Emprical Samples
# Stimulate the server
(atserver_evt, leave_evt) = run_G_FIFO_DS_server(budget, period, execute_dur, arrival_evt)
response_time = np.subtract(leave_evt, arrival_evt)
ecdf = sm.distributions.ECDF(response_time)
y_simu = ecdf(x_axis);


#=============== Analytical ===============
# Step 1. Get exe_dist
N_arr = 20
N_exe = 20
exe_dist = get_dist_from_exec(execute_dur, N_exe, N_arr)
(x_bg, y_bg) = get_MGDS1_from_BGDS1(arrival_rate, exe_dist, budget, period, N_arr)

#V0 = get_BG1_V0_iter(budget, period, succeed_rate, exe_dist, VectorWidth, Error_cap)
#(nz_list, VU_T) = get_BG1_DS_VU_T_list(budget, period, succeed_rate, exe_dist, V0)
#R = get_BG1_DS_R_list(budget, period, succeed_rate, exe_dist, VU_T, nz_list)
if (True == NEWARRIVAL):
	write_arrival_data(processfile, arrival_evt)
	write_arrival_data(executefile, execute_dur)


# ============= Draw Figure =============== 
plt.plot(x_axis, y_simu, linestyle='-', color='blue', drawstyle='steps', clip_on=True, linewidth=2.0)
plt.plot(x_bg  , y_bg  , linestyle='--', color='red', drawstyle='steps', clip_on=True, linewidth=2.0)
plt.xlabel('Response Time', fontsize = 12)
plt.ylabel('Proportion', fontsize = 12)
plt.xlim([0, x_lim])
plt.ylim([0, y_lim])
plt.legend(['Simulation', 'Numerical'])
plt.show()
