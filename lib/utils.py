#!/usr/bin/python
import matplotlib.pyplot as plt
import csv

def plot_curves_with_same_x(x_axis, y_curves, legends, xy_lim, fig_title):
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
	plt.subplots_adjust(left=0.18,top=0.90, bottom=0.2)

	index = 0
	for y_curve in y_curves:
		if(0 == index):
			plt.plot(x_axis, y_curve, linestyle='-', color='black', drawstyle='steps', clip_on=False, linewidth=2.8)
		elif(1 == index):
			plt.plot(x_axis, y_curve, linestyle='-', color='grey', drawstyle='steps', clip_on=False, linewidth=2.8)
		elif(2 == index):
			plt.plot(x_axis, y_curve, linestyle='-', color='sienna', drawstyle='steps', clip_on=False, linewidth=2.8)
		elif(3 == index):
			plt.plot(x_axis, y_curve, linestyle='--', color='orange', drawstyle='steps', clip_on=False, linewidth=2.0)
		elif(4 == index):
			plt.plot(x_axis, y_curve, linestyle='--', color='blue', drawstyle='steps', clip_on=False, linewidth=2.0)
		elif(5 == index):
			plt.plot(x_axis, y_curve, linestyle='--', color='green', drawstyle='steps', clip_on=False, linewidth=2.0)
		else:
			plt.plot(x_axis, y_curve, linestyle='--', drawstyle='steps', clip_on=False, linewidth=2.0)
		index += 1

	plt.xlabel('Response Time (s)', fontsize = 12)
	plt.ylabel('Proportion', fontsize = 12)
	plt.title(fig_title, fontsize = 12)

	(x_lim, y_lim) = xy_lim
	plt.xlim([0, x_lim])
	plt.ylim([0, y_lim])
	plt.legend(legends)
	plt.show()
	return

def write_arrival_data(outfile, arrival_evt):
	with open(outfile, 'w') as outfile:
		for item in arrival_evt:
			outfile.write('%f\n' % (item))
	return

def write_trace_data(outfile, arrival_evt, atserver_evt, leave_evt):
	with open(outfile, 'w') as outfile:
		for index in range(0, len(arrival_evt)):
			outfile.write('%f,%f,%f\n' % (arrival_evt[index], atserver_evt[index], leave_evt[index]))
	return

def read_arrival_data(infile):
	arrival_evt = []
	with open(infile, 'rb') as csvfile:
		myreader = csv.reader(csvfile, delimiter=',', quotechar='|')
		for row in myreader:
			for item in row:
				arrival_evt.append(float(item));
	return arrival_evt


def read_trace_data(infile):
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
