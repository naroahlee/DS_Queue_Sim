#!/usr/bin/python
import copy
from fractions import gcd
import numpy as np
import matplotlib.pyplot as plt
from scipy.special import comb

def get_roots(B, P, prob):
	assert(int(B) == B)
	assert(int(P) == P)
	assert(prob <= 1.0 and prob >= 0)
	assert(prob * float(P) <= B)

	g = gcd(B, P)
	q = B / g
	r = P / g

	eq_list = []

	alpha_r = []
	for i in range(0, r + 1):
		f1  = np.power(      prob, r - i)
		f2  = np.power(1.0 - prob,     i)
		a_i = comb(r, i) * f1 * f2
		alpha_r.append(a_i)

	for k in range(0, g):
		coeff = copy.deepcopy(alpha_r)
		coeff = np.array(coeff)
		coeff = coeff * np.exp(2 * np.pi * 1.0j * k / g)
		coeff[r-q] -= 1
		eq_roots     = np.roots(coeff)
		eq_list = eq_list + list(eq_roots)

	# Eliminate z=1
	eq_list = np.array(eq_list)
	min_index = np.argmin(np.abs(np.add(eq_list, -1.0)))
	eq_list  = np.delete(eq_list, min_index)

	ex_roots = []
	in_roots = []

	for i_root in eq_list:
		if (np.abs(i_root) > (1.00)):
			ex_roots.append(i_root)
		else:
			in_roots.append(i_root)

	# reconstruct eq_roots
	# 0     ~ P-B-1 item:  roots outside unit circle
	#         P-B   item:  z=1
	# P-B+1 ~ P-1   item:  roots inside unit circle
	eq_roots = np.concatenate((ex_roots, [1.0], in_roots))

	return eq_roots

# Compute areas and colors
B = 2
P = 3
p = 0.50

roots = get_roots(B, P, p)

r = np.abs(roots)
theta = np.angle(roots)

print r
#r = 2 * np.random.rand(N)
#theta = 2 * np.pi * np.random.rand(N)
#area = 200 * r**2
colors = theta

fig = plt.figure()
ax = fig.add_subplot(111, projection='polar')
c = ax.scatter(theta, r, s=20, c='blue', alpha=1)
ax.fill_between(np.linspace(0, 2*np.pi, 100), 0.995, 1.005, color='black', zorder=10)
ax.set_rticks([0, 0.25, 0.5, 0.75, 1, 2, 5, 10])  # less radial ticks
ax.set_xticks(np.pi * np.linspace(0,  2, 8, endpoint=False))
ax.set_xticklabels([u'0', u'0.25\u03C0', u'0.5\u03C0' ,u'0.75\u03C0',u'\u03C0',u'1.25\u03C0', u'1.5\u03C0', u'1.75\u03C0'])
mytitle = 'P=%d, B=%d, %c=%3.2f' % (P, B, u'\u03B7', p)
ax.set_rmax(1)
#ax.set_rorigin(0)
ax.grid(True)
ax.set_title(mytitle)
plt.show()
