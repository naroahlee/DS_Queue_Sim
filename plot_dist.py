#!/usr/bin/python
# Compare Exponential CDF between Theoretical and Emprical
import matplotlib.pyplot as plt
import numpy as np
import statsmodels.api as sm
import math
import sys
from lib.md1_cdf import MD1_response_CDF
from lib.utils import *


# Plot Global Parameter
gXLIM = 20

def usage():
	print "plot_dist.py [Arrival_Rate] [Service_Rate] [Result File]"
	return


# ==================== Main ==============================
if (len(sys.argv) != 4):
	usage()
	sys.exit(-1)

arrival_rate = float(sys.argv[1])
service_rate = float(sys.argv[2])
infile       = sys.argv[3]

# Read Data
(arrival_evt, atserver_evt, leave_evt) = read_trace_data(infile)

# Figure out Response Time
response_time = np.subtract(leave_evt, arrival_evt)

# Generate Empirical Curve
x_axis = np.linspace(0, gXLIM, 10000)
ecdf = sm.distributions.ECDF(response_time);
y_empr = ecdf(x_axis);
# Generate Theoretical Curve
y_theo = []
for item in x_axis:
	value = MD1_response_CDF(arrival_rate, service_rate, item)
	y_theo.append(value)

plot_curves_with_same_x(x_axis, [y_empr, y_theo], ['Deferrable Server Sim', 'M/D/1 Theoretical'], [gXLIM, 1.0])
