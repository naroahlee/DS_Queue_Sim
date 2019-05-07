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
arrival_rate = 0.04
sample_num   = 10000

# For D_FIFO_DS server
service_rate = 1.0
bandwidth    = 0.6
period       = 10.0
budget       = bandwidth * period

# Figure Plot Parameter
ecdf_samples = 10000
x_lim = 60.0
y_lim = 1.0
xy_lim = (x_lim, y_lim)

# Logs
processfile  = './data/input/redis_sort.csv'
resultfile   = './data/res/redis_sort.csv'


#=============== Simulation ================

# Generate Emprical Samples
# arrival_evt = gen_poisson_process(arrival_rate, sample_num)
# Stimulate the server
arrival_evt = read_arrival_data(processfile)
(atserver_evt, leave_evt) = run_D_FIFO_DS_server(budget, period, service_rate, arrival_evt)

#============ Post Processing ==============
# Figure out Response Time
response_time = np.subtract(leave_evt, arrival_evt)

# Generate Empirical Curve
x_axis = np.linspace(0, x_lim, ecdf_samples)
ecdf = sm.distributions.ECDF(response_time);
y_simu = ecdf(x_axis);

# Generate Theoretical Curve

response_time = read_arrival_data(resultfile)
response_time = np.array(response_time)
ecdf2 = sm.distributions.ECDF(response_time)
y_empr = ecdf2(x_axis);

plot_curves_with_same_x(x_axis, [y_simu, y_empr], ['Deferrable Server Sim', 'Empr'], xy_lim, 'Title')

# Record the process for later usage
#write_arrival_data(processfile, arrival_evt)
#write_trace_data(resultfile, arrival_evt, atserver_evt, leave_evt)


 

