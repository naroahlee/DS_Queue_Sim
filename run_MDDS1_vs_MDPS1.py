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
arrival_rate = 0.5
sample_num   = 10000

# For D_FIFO_DS server
service_rate = 1.0
budget       = 1.3
period       = 2.0

# Figure Plot Parameter
ecdf_samples = 10000
x_lim = 20.0
y_lim = 1.0
xy_lim = (x_lim, y_lim)

# Logs
processfile  = './data/input/run01.csv'
resultfile   = './data/output/run01.csv'

x_axis = np.linspace(0, x_lim, ecdf_samples)


#=============== Simulation ================
# Generate Emprical Samples
arrival_evt = gen_poisson_process(arrival_rate, sample_num)

#=============== For DS Best ===============
# Stimulate the server
(atserver_evt, leave_evt) = run_D_FIFO_DS_server(budget, period, service_rate, arrival_evt)
response_time = np.subtract(leave_evt, arrival_evt)
ecdf1 = sm.distributions.ECDF(response_time);
y_empr_ds = ecdf1(x_axis);

#=============== For DS Worst ===============
# Stimulate the server
(atserver_evt, leave_evt) = run_D_FIFO_PS_server(budget, period, service_rate, arrival_evt)
response_time = np.subtract(leave_evt, arrival_evt)
ecdf2 = sm.distributions.ECDF(response_time);
y_empr_ps = ecdf2(x_axis);

# Generate Theoretical Curve
y_theo = []
for item in x_axis:
	value = MD1_response_CDF(arrival_rate, service_rate, item)
	y_theo.append(value)

mytitle = u'P=2.0, Bw=65%, \u03BB=0.5, \u03BC=1.0'

plot_curves_with_same_x(x_axis, [y_theo, y_empr_ds, y_empr_ps], ['M/D/1 Theoretical', 'M/D(DS)/1 Best', 'M/D(DS)/1 Worst'], xy_lim, mytitle)

