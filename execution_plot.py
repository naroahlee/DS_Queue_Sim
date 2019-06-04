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
from lib.analytics import get_dist_from_exec
import matplotlib.pyplot as plt

lstyles      = ['-', '--', ':']
N = 20

x_lim_l = 8.0
x_lim_h = 10.0
y_lim = 1.0

# For paper 3.5x2.8 for PPT 5x4
figwidth  = 3.5
figheight = 2.8
plt.figure(figsize=(figwidth, figheight))

# For paper: Enable
plt.subplots_adjust(left=0.18,top=0.95, bottom=0.18)

sample_num   = 20000
ecdf_samples = 10000
x_axis = np.linspace(x_lim_l, x_lim_h, ecdf_samples)

resultfile  = './data/res/redis_sort_calib.csv'
response_time = read_arrival_data(resultfile)
response_time = np.array(response_time)

N = 60
exe_dist = get_dist_from_exec(response_time, N)
print exe_dist



ecdf2 = sm.distributions.ECDF(response_time)
y_empr = ecdf2(x_axis);

print "Average [%f]" % (sum(response_time) / len(response_time))
print "Worst   [%f]" % (max(response_time))

plt.plot(x_axis, y_empr, linestyle='-', color='black', drawstyle='steps', clip_on=True, linewidth=2.0)


#====================== Draw Figure ======================
plt.xlabel('Execution Time (ms)', fontsize = 12)
plt.ylabel('Proportion', fontsize = 12)
#plt.title(mytitle, fontsize = 12)
plt.xlim([x_lim_l, x_lim_h])
plt.ylim([0, y_lim])

plt.legend(['Redis'])
plt.savefig('./figure/redis_sort_calib.eps', format='eps', dpi=1000)
plt.show()

