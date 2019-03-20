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
import matplotlib.pyplot as plt

# ================Parameters ===============
# For Bernoulli Process
p = 0.5

# For imbedded queue server, service_time = 1
service_dur = 1

# Server:
budget = 2
period = 3

# Step 1. Get Virtual Waiting time distribution @ Start of a period (P + 0)
V0 = get_BD1_V0(budget, period, p)

Vn = get_BD1_PS_Vn(budget, period, p, V0)


#print Vn

R  = get_BD1_PS_R(budget, period, Vn)

response_aly = R[0: 20]


# =========================== Simulation ===============================

sample_num   = 100000

# Logs
processfile  = './data/input/run01.csv'
resultfile   = './data/output/run01.csv'


#=============== Simulation ================
# Generate Emprical Samples
# Bernoulli Process
arrival_evt = gen_bernoulli_process(p, sample_num)
(atserver_evt, leave_evt) = run_D_FIFO_PS_server_DT(budget, period, service_dur, arrival_evt)
response_sim = np.subtract(leave_evt, arrival_evt)

cnt = [0] * len(response_aly)
for item in response_sim:
	if (item < len(response_aly)):
		cnt[item] += 1
	 
cnt = np.array(cnt)
dist = (cnt) / float(len(response_sim))

#print dist



#============================================

y_pos = np.array(range(0, len(response_aly)))


plt.bar(y_pos - 0.2, response_aly, width=0.4, align='center', alpha=0.5)
plt.bar(y_pos + 0.2, dist, width=0.4, align='center', alpha=0.5)
plt.legend(['Analytics', 'Simulation'])
plt.xticks(range(0, 21))
plt.xlabel('Response Time (Time Unit)')
plt.ylabel('Probability (Frequency)')
plt.xlim([0, 20])
mytitle = 'P=%d, B=%d, %c=%3.2f' % (period, budget, u'\u03B7', p)
plt.title(mytitle)
plt.show()