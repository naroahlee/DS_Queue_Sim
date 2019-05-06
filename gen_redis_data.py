#!/usr/bin/python
# Compare Exponential CDF between Theoretical and Emprical
import sys
import math
import numpy as np
import statsmodels.api as sm
from lib.utils           import *
from lib.arrival_process import *
from lib.server_model    import *
from lib.analytics import get_MDDS1_from_BDDS1
import matplotlib.pyplot as plt

arrival_rate = 0.1
sample_num   = 5000

for runfile in ['redis01', 'redis02', 'redis03', 'redis04']:
	processfile  = './data/input/' + runfile + '.csv'
	arrival_evt = gen_poisson_process(arrival_rate, sample_num)
	write_arrival_data(processfile, arrival_evt)
