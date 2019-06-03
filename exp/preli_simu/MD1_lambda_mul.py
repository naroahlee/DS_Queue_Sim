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

def plot_curves(x_axis, y_theos):
	#figwidth  = 3.5
	#figheight = 2.8
	figwidth  = 4
	figheight = 3
	plt.figure(figsize=(figwidth, figheight))


	# Disable The Frame
	spinelist = plt.gca().spines.values()
	spinelist[1].set_visible(False)
	spinelist[3].set_visible(False)

	# Don't Clip_on
	plt.subplots_adjust(left=0.18,top=0.9, bottom=0.2)

	for y_item in y_theos:
		plt.plot(x_axis, y_item, linestyle='-', drawstyle='steps', clip_on=False, linewidth=2.0)
	plt.xlabel('Response Time (s)', fontsize = 12)
	plt.ylabel('Proportion', fontsize = 12)
	plt.title('M/D/1 Response Time CDF,' + u'\u03BC' + ' = 1.0')
	plt.xlim([0, gXLIM])
	plt.ylim([0, 1.0])

	legend_sym = []
	for value in np.linspace(0.1, 0.9, 5):
		item = u'\u03BB' + ' = %.1f' % (value) 	
		legend_sym.append(item)

	plt.legend(legend_sym)
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

# Generate Theoretical Curve
x_axis  = np.linspace(0, gXLIM, 10000)
y_theos = []

service_rate = 1.0
for arrival_rate in np.linspace(0.1, 0.9, 5):
	y_temp = []
	for item in x_axis:
		value = MD1_response_CDF(arrival_rate, service_rate, item)
		y_temp.append(value)
	y_theos.append(y_temp)

plot_curves(x_axis, y_theos)
