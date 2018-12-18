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
bandwidth    = budget / period
# Empirical Normalization Factor
empr_scale   = 100.0

# Figure Plot Parameter
ecdf_samples = 10000
x_lim = 20.0
y_lim = 1.0
xy_lim = (x_lim, y_lim)
x_axis = np.linspace(0, x_lim, ecdf_samples)

# Logs
processfile      = './data/input/run01.csv'
resultfile       = './data/output/run01.csv'
empiricalfile    = './data/res/MD1_Empirical_Exp01.csv'
empiricalds2file = './data/res/VM1.csv'

# ============== 1 Theoretical Curve =============
# Generate Theoretical Curve
y_theo = []
for item in x_axis:
	value = MD1_response_CDF(arrival_rate, service_rate, item)
	y_theo.append(value)

# ============== 2 M/D(DS)/1 Simulation ================
arrival_evt = read_arrival_data(processfile)

# Stimulate the server
(atserver_evt, leave_evt) = run_D_FIFO_DS_server(budget, period, service_rate, arrival_evt)

# Figure out Response Time
response_time = np.subtract(leave_evt, arrival_evt)
ecdf1 = sm.distributions.ECDF(response_time);
y_mdds1_sim = ecdf1(x_axis);

# ============== 3 M/D(PS)/1 Simulation ================
# Stimulate the server
(atserver_evt, leave_evt) = run_D_FIFO_PS_server(budget, period, service_rate, arrival_evt)
response_time = np.subtract(leave_evt, arrival_evt)
ecdf2 = sm.distributions.ECDF(response_time);
y_mdps1_sim = ecdf2(x_axis);

# ============== 5 Empirical M/D(DS)/1 Scheduable ================
response_time = read_arrival_data(empiricalds2file)
res_array = (1.0 / empr_scale) * np.array(response_time)
ecdf5 = sm.distributions.ECDF(res_array);
y_empr_ds2 = ecdf5(x_axis);

mytitle = "VM1 P=%.1f, Bw=%2d%%, %c=%.1f, %c=%.1f" % (period, int(bandwidth * 100), u'\u03BB', arrival_rate, u'\u03BC', service_rate)
plot_curves_with_same_x(x_axis, [y_theo, y_mdds1_sim, y_mdps1_sim, y_empr_ds2], ['M/D/1 Theo', 'M/D(DS)/1 Sim', 'M/D(PS)/1 Sim', 'M/D(DS)/1 Empr S'], xy_lim, mytitle)



 

