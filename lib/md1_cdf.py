#!/usr/bin/python
# A Library
# Figure Out the numerical result of CDF
# According to theoretical response time distribution of M/D/1 queue
import numpy as np
import math

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
