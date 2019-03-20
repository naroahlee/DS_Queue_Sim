#!/usr/bin/python
# Compare Exponential CDF between Theoretical and Emprical
import sys
import math
import numpy as np
import statsmodels.api as sm
from lib.utils           import *
from lib.arrival_process import *
from lib.server_model    import *
from lib.analytics import get_BD1_V0
from lib.analytics import get_BD1_PS_Vn
from lib.analytics import get_BD1_PS_R
from lib.analytics import f_DS
from lib.analytics import prDS_U_T
from lib.analytics import get_DS_V_UT
import matplotlib.pyplot as plt

# ================Parameters ===============
# For Bernoulli Process
p = 0.25

# For imbedded queue server, service_time = 1
service_dur = 1

# Server:
budget = 3
period = 5

l = 0
m = 1
n = 1

#print f_DS(l, m, n, budget, period)
print prDS_U_T(m, n, budget, period, p)

mysum = 0.0
start = max(0, budget - n)
for j in range(start, budget + 1):
	pr = prDS_U_T(j, n, budget, period, p)
	print pr
	mysum += pr

print mysum

V0 = get_BD1_V0(budget, period, p)
