#!/usr/bin/python
# A Verification Program
#
#
# Question: X1 X2 are two random variables
#           X1, X2 i.i.d ~ Exp(-lambda)
# Given:    P >= D >= 0
# Pr(X1 <= P-D, X1 + X2 >= P) = ?
# My analytical result:
# lambda * (P - D) * exp{-lambda * P} 

import math
import numpy as np

l = 0.5 #lambda
P = 3.0
D = 1

def compute_via_formula(l, P, D):
	#res = (l * (P - D) * math.exp(-1.0 * l * P) * (1.0 - math.exp(-1.0 * l * (P - D))))
	res = l * (P - D) * math.exp(-1.0 * l * P)
	return res

def compute_via_simulation(l, P, D):
	beta     = 1.0 / l
	samples  = 200000
	truetime = 0
	for i in range(0, samples):
		X1 = np.random.exponential(beta, 1)
		X2 = np.random.exponential(beta, 1)
		if((X1 <= (P - D)) and (X1 + X2 >= P)):
			truetime += 1

	res = float(truetime) / samples
	return res
	


print compute_via_formula(l, P, D)
print compute_via_simulation(l, P, D)
