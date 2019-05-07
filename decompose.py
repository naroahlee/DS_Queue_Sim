#!/usr/bin/python
# Compare Exponential CDF between Theoretical and Emprical
import sys
import math
import numpy as np
import statsmodels.api as sm
from lib.utils           import *
from lib.arrival_process import *
from lib.server_model    import *
import matplotlib.pyplot as plt

runfile = 'redis_sort'

processfile  = './data/input/' + runfile + '.csv'

sep_list = [[], [], [], [], [], [], [], []]

arrival_evt = read_arrival_data(processfile)

for i in range(0, len(arrival_evt)):
	sep_list[i % 8].append(arrival_evt[i])
	

for i in range(0, 8):
	resfile  = './data/input/' + runfile + str(i) + '.csv'
	write_arrival_data(resfile, sep_list[i])

