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
from lib.analytics import get_BD1_V0_iter
from lib.analytics import get_BD1_PS_Vn
from lib.analytics import get_BD1_PS_R
import matplotlib.pyplot as plt

# ================Parameters ===============
# For Bernoulli Process
p = 0.90

# For imbedded queue server, service_time = 1
service_dur = 1

# Server:
budget = 19
period = 20

# Step 1. Get Virtual Waiting time distribution @ Start of a period (P + 0)

V_0 = get_BD1_V0_iter(budget, period, p, 20, 100)
print V_0

print sum(V_0)

