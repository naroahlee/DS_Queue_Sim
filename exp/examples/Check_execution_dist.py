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

#=============== Empirical Distribution =================
ecdf          = sm.distributions.ECDF(execute_dur)
y_empr        = ecdf(x_axis);

print np.mean(execute_dur)
print np.std(execute_dur)


# ============= Draw Figure =============== 
figwidth  = 5
figheight = 4
plt.figure(figsize=(figwidth, figheight))
plt.plot(x_axis, y_empr, linestyle='-', color='blue', drawstyle='steps', clip_on=True, linewidth=2.0)
plt.xlabel('Execution Time', fontsize = 12)
plt.ylabel('Proportion', fontsize = 12)
mytitle = 'd=%.1f, %c=%.1f' % (g_mean, u'\u03C3', g_sqvar)
plt.title(mytitle)
plt.xlim([0, 2])
plt.ylim([0, y_lim])
plt.show()
