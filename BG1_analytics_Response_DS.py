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
from lib.analytics import get_BG1_V0_iter
from lib.analytics import get_BG1_DS_VU_T_list
from lib.analytics import get_BG1_DS_R_list

# ================Parameters ===============

# For DS server
#bandwidth    = 0.6
budget       = 4
period       = 5
#budget       = bandwidth * period

# For B arrival
succeed_rate = 0.10
sample_num   = 20000


# Figure Plot Parameter
ecdf_samples = 10000
x_lim = 60.0
y_lim = 1.0
xy_lim = (x_lim, y_lim)

# Logs
#processfile  = './data/input/redis_sort.csv'
#resultfile   = './data/res/redis_sort.csv'


#=============== Simulation ================

# Generate Emprical Samples
arrival_evt = gen_bernoulli_process(succeed_rate, sample_num)

a  = 2
b  = 6
pa = 0.5
exe_dist = [(2, 0.5), (6, 0.5)]
service_rate = 1.0 / ((a * pa) + b * (1 - pa))

execute_dur = gen_binary_distribution_execution(a, b, pa, sample_num)

# Stimulate the server
(atserver_evt, leave_evt) = run_G_FIFO_DS_server(budget, period, execute_dur, arrival_evt)

#============ Post Processing ==============
# Figure out Response Time
response_time = np.subtract(leave_evt, arrival_evt)

cnt_upper = 40
cnt = [0] * cnt_upper
for item in response_time:
	if (item < len(cnt)):
		cnt[int(round(item))] += 1
	 
cnt = np.array(cnt)
dist = (cnt) / float(len(response_time))

# Generate Simulation Curve
y_pos = np.array(range(0, len(cnt)))

#=============== Analytical ===============
VectorWidth = 800
Error_cap   = 0.0001
V0 = get_BG1_V0_iter(budget, period, succeed_rate, exe_dist, VectorWidth, Error_cap)
(nz_list, VU_T) = get_BG1_DS_VU_T_list(budget, period, succeed_rate, exe_dist, V0)
R = get_BG1_DS_R_list(budget, period, succeed_rate, exe_dist, VU_T, nz_list)

response_aly = R[0:cnt_upper]

plt.bar(y_pos - 0.2, response_aly, width=0.4, align='center', alpha=0.5)
plt.bar(y_pos + 0.2, dist, width=0.4, align='center', alpha=0.5)
plt.legend(['Numerical', 'Simulation'])
plt.xticks(range(0, 31))
plt.xlabel('Response Time (Time Unit)')
plt.ylabel('Probability (Frequency)')
plt.xlim([0, 30])
mytitle = 'P=%d, B=%d, d=%d, %c=%3.2f' % (period, budget, int(1.0/ service_rate), u'\u03B7', succeed_rate)
plt.title(mytitle)
plt.show()

# Record the process for later usage
#write_arrival_data(processfile, arrival_evt)
#write_trace_data(resultfile, arrival_evt, atserver_evt, leave_evt)


 

