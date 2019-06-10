#!/usr/bin/python
# Run M/G(DS)/1 Simulation
import sys
import math
import numpy as np
import statsmodels.api as sm
import datetime
from lib.utils           import *
from lib.arrival_process import *
from lib.server_model    import *
from lib.md1_cdf import MD1_response_CDF
from lib.analytics import get_dist_from_exec
from lib.analytics import get_MDDS1_from_BDDS1
from lib.analytics import get_MGDS1_from_BGDS1

# ================Parameters ===============
NEWMEASURE = False

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

executefile  = './data/input/MGDS1_execute.csv'
execute_dur = read_arrival_data(executefile)
# Logs
Bins = [1, 2, 4, 5, 10, 20]
x_pts = [1, 3, 7, 9, 19, 39]
t_list = []
timefile  = './data/input/MGDS1_time.csv'



if (True == NEWMEASURE):
	# Step 1. Get exe_dist
	#=============== Analytical: M/G(DS)/1 ===============
	for N_exe in Bins:

		t_start = datetime.datetime.now()
		N_arr = 20
		exe_dist = get_dist_from_exec(execute_dur, N_exe, N_arr)
		(x_bg, y_bg) = get_MGDS1_from_BGDS1(arrival_rate, exe_dist, budget, period, N_arr)
		t_end  = datetime.datetime.now()
		t_delta = t_end - t_start

		
		t_list.append(t_delta.total_seconds())

	write_arrival_data(timefile, t_list)	
else:
	t_list = read_arrival_data(timefile)

print t_list



# ============= Draw Figure =============== 
figwidth  = 5
figheight = 4
plt.figure(figsize=(figwidth, figheight))
cdfsty='default'
#cdfsty='steps'
plt.plot(x_pts, t_list, linestyle='-', marker='o', color='blue', drawstyle=cdfsty, clip_on=True, linewidth=2.0)
plt.xlabel('Bin Size', fontsize = 12)
plt.ylabel('Computation Time (s)', fontsize = 12)
plt.xlim([0, 40])
plt.ylim([0, 80])
#plt.legend(['M/G(DS)/1 Simu', 'M/D(DS)/1', '7 Bins'])
plt.show()
