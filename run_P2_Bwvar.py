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
period       = 2.0

# Figure Plot Parameter
ecdf_samples = 10000
x_lim = 20.0
y_lim = 1.0
xy_lim = (x_lim, y_lim)

x_axis = np.linspace(0, x_lim, ecdf_samples)
#=============== Simulation ================
y_curves = []
# Generate Theoretical Curve
y_theo = []
for item in x_axis:
	value = MD1_response_CDF(arrival_rate, service_rate, item)
	y_theo.append(value)

y_curves.append(y_theo)

# Generate Emprical Samples
arrival_evt = gen_poisson_process(arrival_rate, sample_num)
# Stimulate the server

for budget in [1.2, 1.4, 1.6, 1.8, 2.0]:
	(atserver_evt, leave_evt) = run_D_FIFO_DS_server(budget, period, service_rate, arrival_evt)
	response_time = np.subtract(leave_evt, arrival_evt)
	ecdf = sm.distributions.ECDF(response_time);
	y_empr = ecdf(x_axis);
	y_curves.append(y_empr)


plot_curves_with_same_x(x_axis, y_curves, ['M/D/1 Theoretical', 'Bw=60%', 'Bw=70%', 'Bw=80%', 'Bw=90%', 'Bw=100%'], xy_lim, u'M/D(DS)/1, P=2.0, \u03BB=0.5, \u03BC=1.0')
