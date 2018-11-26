#!/usr/bin/python
# Compare Exponential CDF between Theoretical and Emprical
import matplotlib.pyplot as plt
import numpy as np
import statsmodels.api as sm
import csv
import sys


# \lambda
arrival_rate = 0.5
sample_num   = 500

# Plot Global Parameter
gXLIM = 20

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
	plt.xlabel('Inter-Arrival Time (s)', fontsize = 12)
	plt.ylabel('Proportion', fontsize = 12)
	plt.xlim([0, gXLIM])
	plt.ylim([0, 1.0])
	plt.legend(['Emprical', 'Theoretical'])
	plt.show()
	return


# Generate Emprical Samples
beta = 1.0 / arrival_rate
alldata = np.random.exponential(beta, sample_num)

# Sample ==> CDF
x = np.linspace(0, gXLIM, 10000)
ecdf = sm.distributions.ECDF(alldata);
y_empr = ecdf(x);

# Theoretical: F(t) = P{X <= t} = 1 - exp(-lambda * t),   t > 0
y_theo = list(map(lambda x: (1.0 - np.exp(-1.0 * arrival_rate * x)) , x)) 

# Generate Theoretical Curve
plot_curves((x, y_empr), (x, y_theo))

