#!/usr/bin/python
import numpy as np
import copy
from scipy.special import comb
from fractions import gcd

def int_frac_ceil(N, D):
	assert(int(N) == N)
	assert(int(D) == D)

	if(0 == N % D):
		return (N / D)
	else:
		return ((N / D) + 1)

# A optimized version of getting roots
# Will use gcd(B, P) to simplify the computation
def get_roots(B, P, prob):
	assert(int(B) == B)
	assert(int(P) == P)
	assert(prob <= 1.0 and prob >= 0)
	assert(prob * float(P) <= B)

	g = gcd(B, P)
	q = B / g
	r = P / g

	eq_list = []

	# Degenerate the order of the polynominal function
	alpha_r = []
	for i in range(0, r + 1):
		f1  = np.power(      prob, r - i)
		f2  = np.power(1.0 - prob,     i)
		a_i = comb(r, i) * f1 * f2
		alpha_r.append(a_i)

	# We will have g functions, each is a r-order
	# And we still get g x r = P roots
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

	# Step 2. Group the roots
	# We will discard the z=1 roots, since it's trivial
	# We will use in_root to determin pi_0 ... pi_{B-1}
	# We will use ex_root to determin pi_B ... pi_{\infty}
	# Discard the root whose has the minimal distance to z=1
	ex_roots = []
	in_roots = []

	for i_root in eq_list:
		if (np.abs(i_root) > (1.00)):
			ex_roots.append(i_root)
		else:
			in_roots.append(i_root)

	assert((P - B) == len(ex_roots))
	assert((B - 1) == len(in_roots))

	eq_roots = np.concatenate((ex_roots, [1.0], in_roots))

	return eq_roots

# This is for analytical solution
# Can hardly be stable, just for reference
def get_BD1_V0(B, P, prob, J=4):
	assert(int(B) == B)
	assert(int(P) == P)
	assert(int(J) == J)
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

	# Step 2. Get the roots
	# Get roots: use the optimized method
	eq_roots = get_roots(B, P, prob)
	ex_roots = eq_roots[0 : P - B]
	in_roots = eq_roots[P - B + 1: P]

	print eq_roots
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
		print xi
		for j in range(0, B):
			A[i][j] = 0.0
			for h in range(0, B - j):
				A[i][j] += ((np.power(xi, B) - np.power(xi, h + j)) * alpha_h[h])

#	print A

	b = np.zeros(B)
	b[0] = B - prob * P 
	pi_j = np.linalg.solve(A, b)

	print pi_j

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

	# Step 4.1 Compute pi_{B+1} to pi_{P-B-1}
	for j in range(1, P - B):
		term1 = 0.0
		for h in range(0, B + j):
			term1 += pi_j[h] * alpha_h[B + j - h]
		pi_jpB = (pi_j[j] - term1) / alpha_h[0]
		pi_j   = np.concatenate((pi_j, [pi_jpB]))
		

	for j in range(P - B, 20):
		term1 = 0.0
		for h in range(0, P):
			term1 += pi_j[j - P + B + h] * alpha_h[P - h]
		pi_jpB = (pi_j[j] - term1) / alpha_h[0]
		pi_j   = np.concatenate((pi_j, [pi_jpB]))


	pi_j = np.abs(pi_j)

	# Step 4.3 Using GT method to correct the tail
	# Adopt the tail method:
	
	# Get the dominate root:
	q = 1.0 / np.min(np.abs(ex_roots))
	pi_0toJm1 = sum(pi_j[0:J])

	#print "q= %f" % (q)
	#print "sum pi[0 to J-1] = %f" % (pi_0toJm1)

	# Truncate Pi, then figure out Pi_J
	pi_j = pi_j[0:J]
	pi_J = (1.0 - q) * (1.0 - pi_0toJm1)	
	pi_j = np.concatenate((pi_j, [pi_J]))

	# Using Geometric Tail
	for i in range(J + 1, 20):
		new_item = pi_j[i - 1] * q
		pi_j = np.concatenate((pi_j, [new_item]))
		
	return pi_j

def get_BD1_V0_iter(B, P, p, W, time=100):
	Vn = np.zeros((P + 1, W))
	Vn[0][0] = 1.0

	for k in range(0, time):
		#print "Iter[%2d]" % (k)
		for n in range(1, P + 1):
			# Compute Off-slot
			if(n <= (P - B)):
				Vn[n][0] = Vn[n-1][0] * (1.0 - p)
				for i in range(1, W):
					Vn[n][i] = Vn[n-1][i-1] * p + Vn[n-1][i] * (1.0-p)
			else:
			# Compute On-slot
				Vn[n][0] = Vn[n-1][0] + Vn[n-1][1] * (1.0 - p)
				for i in range(1, W - 1):
					Vn[n][i] = Vn[n - 1][i] * p + Vn[n-1][i + 1] * (1.0-p)
				Vn[n][W - 1] = p * Vn[n-1][W - 1] 

		# Normalize Vn[P]
		Vn[P] = (Vn[P] / sum(Vn[P]))
	
		# Compute the 1-norm Distance
		#err = Vn[P] - Vn[0]
		#err_1norm = np.linalg.norm(err, ord=1)
		#print err_1norm

		Vn[0] = Vn[P]

	return Vn[0]

def get_BD1_PS_Vn(B, P, p, V0):
	m = len(V0)
	Vn = np.zeros((P, m))
	Vn[0] = V0

	for n in range(1, P):
		# Compute Off-slot
		if(n <= (P - B)):
			Vn[n][0] = Vn[n-1][0] * (1.0 - p)
			for i in range(1, m):
				Vn[n][i] = Vn[n-1][i-1] * p + Vn[n-1][i] * (1.0-p)
		else:
		# Compute On-slot
			Vn[n][0] = Vn[n-1][0] + Vn[n-1][1] * (1.0 - p)
			for i in range(1, m - 1):
				Vn[n][i] = Vn[n - 1][i] * p + Vn[n-1][i + 1] * (1.0-p)
			Vn[n][m-1] = p * Vn[n-1][m-1]
	return Vn

def get_BD1_PS_R(B, P, Vn):
	(P1, m) = Vn.shape
	R = np.zeros(100)
	for n in range(0, P):
		for i in range(0, m):
			# Off-slot
			if(n < (P-B)):
				#Replenish Time + Execution Time + First Period Offset
				k = int_frac_ceil(i + 1, B)
				k = k * (P - B)
				k = k + (i + 1) - n
				R[k] += (1.0 / P) * Vn[n][i]
			# On-slot
			else:
				k = int_frac_ceil((i + 1) - (P - n), B)
				k = k * (P - B)
				k = k + (i + 1)
				R[k] += (1.0 / P) * Vn[n][i]
	return R

# ===================== For Deferrable Server ===========================
#     the Virtual Waiting Time : l
#     the Remaining Budget     : m
#     the arriving slot offset : n
# to determine response time
def f_DS(l, m, n, B, P):
	assert(int(B) == B and (B >  0))
	assert(int(P) == P and (P >= B))
	assert(int(l) == l and (l >= 0))
	assert(int(m) == m and (m >= 0) and (m <= B))
	assert(int(n) == n and (n >= B - m) and (n < P))

	r = min(m, P - n)
	v = P - n - r 

	if (l + 1 <= r):
		t = l + 1
	elif (l + 1 <= r + B):
		t = l + 1 + v
	else:
		t = int_frac_ceil(((l+1)-(r+B)), B)
		t = t * (P - B)
		t = t + l + 1 + v

	return t
	


# ========================================================
def get_DS_VU_T(B, P, p, V0):
	W = len(V0)
	VU_T = np.zeros((W, B + 1, P))

	# fill the initial number V0
	for l in range(0, W):
		VU_T[l][B][0] = V0[l]

	# Compute 1~B line
	for n in range(1, B + 1):
		VU_T[0][B][n] = (1-p) * VU_T[0][B][n-1] 
		# Triangle
		for m in range(1, n):
			VU_T[0][B-m][n] = p * VU_T[0][B-m+1][n-1] + (1-p) * VU_T[0][B-m][n-1]
		for l in range(0, W - 1):
			VU_T[l][B-n][n] = p * VU_T[l][B-n+1][n-1] + (1-p) * VU_T[l+1][B-n+1][n-1]
		VU_T[W-1][B-n][n] = p * VU_T[l][B-n+1][n-1] 

	# Compute 1~B line
	for n in range(B + 1, P):
		VU_T[0][B][n] = (1-p) * VU_T[0][B][n-1] 
		# No longer Triangle
		for m in range(1, B):
			VU_T[0][B-m][n] = p * VU_T[0][B-m+1][n-1] + (1-p) * VU_T[0][B-m][n-1]

		VU_T[0][0][n] = p * VU_T[0][1][n-1] + (1-p) * VU_T[0][0][n-1] 
		for l in range(1, W):
			VU_T[l][0][n] = p * VU_T[l-1][0][n-1] + (1-p) * VU_T[l][0][n-1]

	return VU_T

def get_BD1_DS_R(B, P, p, VU_T):
	(W, B1, P1) = VU_T.shape
	R = np.zeros(100)
	for n in range(0, B + 1):
		for m in range(0, n):
			k = f_DS(0, B - m, n, B, P)
			#R[k] += (1.0 / P) * U_T[B - m][n] * V_UT[0][B - m][n]
			R[k] += (1.0 / P) * VU_T[0][B - m][n]
		for l in range(0, W):
			k = f_DS(l, B - n, n, B, P)
			#R[k] += (1.0 / P) * U_T[B - n][n] * V_UT[l][B - n][n]
			R[k] += (1.0 / P) * VU_T[l][B - n][n]

	for n in range(B + 1, P):
		for m in range(0, B):
			k = f_DS(0, B - m, n, B, P)
			#R[k] += (1.0 / P) * U_T[B - m][n] * V_UT[0][B - m][n]
			R[k] += (1.0 / P) * VU_T[0][B - m][n]
		for l in range(0, W):
			k = f_DS(l, 0, n, B, P)
			#R[k] += (1.0 / P) * U_T[0][n]     * V_UT[l][0][n]
			R[k] += (1.0 / P) * VU_T[l][0][n]

	return R
