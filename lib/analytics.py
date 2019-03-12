#!/usr/bin/python
import numpy as np
import copy
from scipy.special import comb

def get_BD1_Vx_at_nP(B, P, prob):
	assert(int(B) == B)
	assert(int(P) == P)
	assert(prob <= 1.0 and prob >= 0)
	assert(prob * float(P) <= B)

	# Step 1. Get the roots from the equation

	# Create an equation's coeffiecent
	# z^B = [pz + (1-p)]^P
	alpha_h = []
	for i in range(0, P + 1):
		f1  = np.power(      prob, P - i)
		f2  = np.power(1.0 - prob,     i)
		a_i = comb(P, i) * f1 * f2
		alpha_h.append(a_i)

	coeff = copy.deepcopy(alpha_h)
	coeff[P-B] -= 1

	# Get roots
	eq_roots     = np.roots(coeff)

	# Step 2. Group the roots
	# We will discard the z=1 roots, since it's trivial
	# We will use in_root to determin pi_0 ... pi_{B-1}
	# We will use ex_root to determin pi_B ... pi_{\infty}
	# Discard the root whose has the minimal distance to z=1
	min_index = np.argmin(np.abs(np.add(eq_roots, -1.0)))
	eq_roots  = np.delete(eq_roots, min_index)

	ex_roots = []
	in_roots = []

	for i_root in eq_roots:
		if (np.abs(i_root) > (1.00)):
			ex_roots.append(i_root)
		else:
			in_roots.append(i_root)

	# reconstruct eq_roots
	# 0     ~ P-B-1 item:  roots outside unit circle
	#         P-B   item:  z=1
	# P-B+1 ~ P-1   item:  roots inside unit circle
	eq_roots = np.concatenate((ex_roots, [1.0], in_roots))

	#print eq_roots

	assert((P - B) == len(ex_roots))
	assert((B - 1) == len(in_roots))


	# Step 3. Using a Linear equation to solve pi_0 ... pi_{B-1}
	# Create Matrix A
	# The Matrix will be BxB order
	# Solve Ax = b
	A = np.zeros((B, B), dtype=np.complex)

	# Fill in first Row
	# a0j = sum_{h = 0}^{B - 1} (B - h) * a_h
	for j in range(0, B):
		A[0][j] = 0.0
		for h in range (0, B - j):
			A[0][j] += ((B - j - h) * alpha_h[h])

	for i in range(1, B):
		xi = in_roots[i - 1]
		for j in range(0, B):
			A[i][j] = 0.0
			for h in range(0, B - j):
				A[i][j] += ((np.power(xi, B) - np.power(xi, h + j)) * alpha_h[h])

	#print A

	b = np.zeros(B)
	b[0] = B - prob * P 
	pi_j = np.linalg.solve(A, b)

	assert(B == len(pi_j))

	# Step 4. Compute pi_B, remember, this is special
	term1 = 0.0
	for j in range(0, B):
		coef = 0.0
		for h in range(0, B - j + 1):
			coef += alpha_h[h]
		term1 += coef * pi_j[j]

	pi_B = (pi_j[0] - term1) / alpha_h[0]
	pi_j = np.concatenate((pi_j, [pi_B]))

	# Step4.1 Compute pi_{B+1} to pi_{P-B-1}
	for j in range(1, P - B):
		term1 = 0.0
		for h in range(0, B + j):
			term1 += pi_j[h] * alpha_h[B + j - h]
		pi_jpB = (pi_j[j] - term1) / alpha_h[0]
		pi_j   = np.concatenate((pi_j, [pi_jpB]))
		

	for j in range(P - B, 10):
		term1 = 0.0
		for h in range(0, P):
			term1 += pi_j[j - P + B + h] * alpha_h[P - h]
		pi_jpB = (pi_j[j] - term1) / alpha_h[0]
		pi_j   = np.concatenate((pi_j, [pi_jpB]))


	#print eq_roots
	#print np.abs(pi_j) 
	return np.abs(pi_j)

