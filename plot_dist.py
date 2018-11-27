#!/usr/bin/python
# Compare Exponential CDF between Theoretical and Emprical
import matplotlib.pyplot as plt
import numpy as np
import statsmodels.api as sm
import math
import csv
import sys

# Plot Global Parameter
gXLIM = 20

def usage():
	print "plot_dist.py [Arrival_Rate] [Service_Rate] [Result File]"
	return

def read_data(infile):
	arrival_evt  = []
	atserver_evt = []
	leave_evt    = []

	with open(infile, 'rb') as csvfile:
		myreader = csv.reader(csvfile, delimiter=',', quotechar='|')
		for row in myreader:
			arrival_evt.append(float(row[0]))
			atserver_evt.append(float(row[1]))
			leave_evt.append(float(row[2]))
	return (arrival_evt, atserver_evt, leave_evt)

def plot_curves(empr_curve, theo_curve):
	#figwidth  = 3.5
	#figheight = 2.8
	figwidth  = 8
	figheight = 6
	plt.figure(figsize=(figwidth, figheight))


	(x_empr, y_empr) = empr_curve
	(x_theo, y_theo) = theo_curve


	# Disable The Frame
	spinelist = plt.gca().spines.values()
	spinelist[1].set_visible(False)
	spinelist[3].set_visible(False)

	# Don't Clip_on
	plt.subplots_adjust(left=0.18,top=0.95, bottom=0.18)
	plt.plot(x_empr, y_empr, linestyle='-',  color='blue',  drawstyle='steps', clip_on=False, linewidth=2.0)
	plt.plot(x_theo, y_theo, linestyle='--', color='black', drawstyle='steps', clip_on=False, linewidth=2.0)
	plt.xlabel('Response Time (s)', fontsize = 12)
	plt.ylabel('Proportion', fontsize = 12)
	plt.xlim([0, gXLIM])
#	plt.ylim([0, 1.0])
	plt.legend(['Emprical', 'Theoretical'])
	plt.show()
	return

def MD1_waiting_CDF(arrival_rate, service_rate, t):
	rau = arrival_rate / service_rate
	sum = 0.0
	for n in range(0, int(math.floor(service_rate * t)) + 1):
		q = rau * (n - service_rate * t)
		f1 = 1.0 / math.factorial(n)
		f2 = math.pow(q, n)
		f3 = math.exp(-1.0 * q)
		sum += (f1 * f2 * f3)
		
	res = (1 - rau) * sum
	return res

def MD1_response_CDF(arrival_rate, service_rate, t):
	if(t < (1.0 / service_rate)):
		return 0
	else:
		return MD1_waiting_CDF(arrival_rate, service_rate, t - (1.0 / service_rate))
	


# ==================== Main ==============================
if (len(sys.argv) != 4):
	usage()
	sys.exit(-1)

arrival_rate = float(sys.argv[1])
service_rate = float(sys.argv[2])
infile       = sys.argv[3]

# Read Data
(arrival_evt, atserver_evt, leave_evt) = read_data(infile)

# Figure out Response Time
response_time = []
for index in range(0, len(arrival_evt)):
	delta = leave_evt[index] - arrival_evt[index]
	response_time.append(delta)

# Draw

# Generate Empirical Curve
x_axis = np.linspace(0, gXLIM, 10000)
ecdf = sm.distributions.ECDF(response_time);
y_empr = ecdf(x_axis);
# Generate Theoretical Curve
y_theo = []
for item in x_axis:
	value = MD1_response_CDF(arrival_rate, service_rate, item)
	y_theo.append(value)

plot_curves((x_axis, y_empr), (x_axis, y_theo))
