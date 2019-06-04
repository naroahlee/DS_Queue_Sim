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

# B/D(XS)/1 D>=1
def get_BD1_V0_iter(B, P, p, d, W, error_cap=0.001):
	Vn = np.zeros((P + 1, W))
	Vn[0][0] = 1.0

	err_1norm = 1.0
	iter_counter = 0
	while(err_1norm > error_cap):
		for n in range(1, P + 1):
			if(n <= (P - B)):
			# Compute Off-slot
				for i in range(0, d):
					Vn[n][i] = Vn[n-1][i] * (1.0-p)
				for i in range(d, W):
					Vn[n][i] = Vn[n-1][i-d] * p + Vn[n-1][i] * (1.0-p)
			else:
			# Compute On-slot
				if(1 == d):
					Vn[n][0] = Vn[n-1][0]             + Vn[n-1][1] * (1.0-p)
					for i in range(1, W - 1):
						Vn[n][i] = Vn[n-1][i] * p     + Vn[n-1][i+1] * (1.0-p)
					Vn[n][W - 1] = p * Vn[n-1][W - 1] 
				else:#(d >= 2)
					Vn[n][0] = Vn[n-1][0] * (1.0-p)   + Vn[n-1][1] * (1.0-p)
					for i in range(1, d - 1):
						Vn[n][i] = Vn[n-1][i+1] * (1.0-p)
					for i in range(d - 1, W - 1):
						Vn[n][i] = Vn[n-1][i-d+1] * p + Vn[n-1][i+1] * (1.0-p)
					Vn[n][W - 1] = p * Vn[n-1][W-d+1] 

		# Normalize Vn[P]
		Vn[P] = (Vn[P] / sum(Vn[P]))
	
		err = Vn[P] - Vn[0]
		err_1norm = np.linalg.norm(err, ord=1)

		Vn[0] = Vn[P]
		iter_counter += 1

	print "Iteration Time: [%d], 1-norm Error [%f]" % (iter_counter, err_1norm)

	return Vn[0]

# B/G(XS)/1 
# exe_dist is a list of tuple (d, q): we got probablity q of having an duration d
def get_BG1_V0_iter(B, P, p, exe_dist, W, error_cap=0.001):

	qsum = 0.0	
	for (d, q) in exe_dist:
		assert(d > 0)
		qsum += q
	assert(abs(1.0 - qsum) <= 0.001)
		
	# Algorithm Start
	Vn = np.zeros((P + 1, W))
	Vn[0][0] = 1.0

	err_1norm = 1.0
	iter_counter = 0
	while(err_1norm > error_cap):
		for n in range(0, P):
			if(n < (P - B)):
			# Compute Off-slot
				for i in range(0, W):
					Vn[n+1][i] += Vn[n][i] * (1.0-p)         # No arrival
					for (d, q) in exe_dist:
						if (i+d < W):
							Vn[n+1][i+d] += Vn[n][i] * p * q # Arrival + Condition
			else:
			# Compute On-slot
				# Process i == 0 
				Vn[n+1][0] += Vn[n][0] * (1.0-p)         # No arrival
				for (d, q) in exe_dist:
					if (d - 1 < W):
						Vn[n+1][d-1] += Vn[n][0] * p * q # Arrival + Condition
				
				# Process i >= 1	
				for i in range(1, W):
					Vn[n+1][i-1] +=  Vn[n][i] * (1.0-p)  # No arrival
					for (d, q) in exe_dist:
						if (i+d-1 < W):
							Vn[n+1][i+d-1] += Vn[n][i] * p * q # Arrival + Condition
		# end for n=0toP-1

		# Normalize Vn[P]
		Vn[P] = (Vn[P] / sum(Vn[P]))
	
		err = Vn[P] - Vn[0]
		err_1norm = np.linalg.norm(err, ord=1)

		temp = Vn[P]
		Vn = np.zeros((P + 1, W))
		Vn[0] = temp
		iter_counter += 1
	# end while(check error)

	print "Iteration Time: [%d], 1-norm Error [%f]" % (iter_counter, err_1norm)

	return Vn[0]

# ===================== For Periodic Server ===========================
# to determine response time
#     the Virtual Waiting Time : l
#     the arriving slot offset : n
#     the deterministic servie : d
def f_PS(l, n, B, P, d):
	if(n < P-B):
		t = int_frac_ceil((l+d), B) * (P - B) + l + d - n
	else:
		t = int_frac_ceil( (l+d)-(P-n) , B) * (P - B) + l + d

	return t

# B/D(PS)/1 D>=1
def get_BD1_PS_Vn(B, P, p, d, V0):
	W = len(V0)
	Vn = np.zeros((P, W))
	# Iteration Initial State has been computed
	Vn[0] = V0

	for n in range(1, P):
		if(n <= (P - B)):
		# Compute Off-slot
			for i in range(0, d):
				Vn[n][i] = Vn[n-1][i] * (1.0-p)
			for i in range(d, W):
				Vn[n][i] = Vn[n-1][i-d] * p + Vn[n-1][i] * (1.0-p)
		else:
		# Compute On-slot
			if(1 == d):
				Vn[n][0] = Vn[n-1][0]             + Vn[n-1][1] * (1.0-p)
				for i in range(1, W - 1):
					Vn[n][i] = Vn[n-1][i] * p     + Vn[n-1][i+1] * (1.0-p)
				Vn[n][W - 1] = p * Vn[n-1][W - 1] 
			else:#(d >= 2)
				Vn[n][0] = Vn[n-1][0] * (1.0-p)   + Vn[n-1][1] * (1.0-p)
				for i in range(1, d - 1):
					Vn[n][i] = Vn[n-1][i+1] * (1.0-p)
				for i in range(d - 1, W - 1):
					Vn[n][i] = Vn[n-1][i-d+1] * p + Vn[n-1][i+1] * (1.0-p)
				Vn[n][W - 1] = p * Vn[n-1][W-d+1] 

	return Vn

def get_BD1_PS_R(B, P, d, Vn):
	(P1, W) = Vn.shape
	R = np.zeros(((W + d) / B + 1) * P + 1)
	for n in range(0, P):
		for l in range(0, W):
			k = f_PS(l, n, B, P, d)
			R[k] += (1.0 / P) * Vn[n][l]
	return R

	
# ===================== For Deferrable Server ===========================
# to determine response time
#     the Virtual Waiting Time : l
#     the Remaining Budget     : m
#     the arriving slot offset : n
#     the deterministic servie : d
def f_DS(l, m, n, B, P, d):
	assert(int(B) == B and (B >  0))
	assert(int(P) == P and (P >= B))
	assert(int(l) == l and (l >= 0))
	assert(int(d) == d and (d >= 1))
	assert(int(m) == m and (m >= 0) and (m <= B))
	assert(int(n) == n and (n >= B - m) and (n < P))

	r = min(m, P - n)
	v = P - n - r 

	if (l + d <= r):
		t = l + d
	elif (l + d <= r + B):
		t = l + d + v
	else:
		t = int_frac_ceil(((l+d)-(r+B)), B)
		t = t * (P - B)
		t = t + l + d + v

	return t

# The new method for getting the VU_T when d >= 2
# Return:
# A list contains P lists to identify which joint probabality is no zero
# For Each of the P lists:
#     Contains a tuple of (V=l, U=m) to identify the one with no zero probablity
def get_BD1_DS_VU_T_list(B, P, p, d, V0):
	nz_list = []

	# initalization
	W = len(V0)
	VU_T = np.zeros((W, B + 1, P))


	templist = []
	# fill the initial number V0
	for l in range(0, W):
		VU_T[l][B][0] = V0[l]
		templist.append( (l, B) )

	nz_list.append(templist)
	
	for n in range(0, P - 1):
		templist = []
		# For each Iteration, reset the checkmark
		checkchart = np.zeros((W, B + 1))

		for (l, m) in nz_list[n]:
			if(m > 0):
				if(l > 0):
					# We have budget and we have things pending
					# If nothing incoming, use budget for already pending task
					VU_T[l-1  ][m-1][n+1] += VU_T[l][m][n] * (1 - p)
					if(0 == checkchart[l-1  ][m-1]):
						checkchart[l-1  ][m-1] = 1
						templist.append( (l-1  ,m-1) )

					# Sacrifice some tail proportion
					if(l+d-1 >= W):
						continue

					# If something incoming, use budget for already pending task
					VU_T[l+d-1][m-1][n+1] += VU_T[l][m][n] * p
					if(0 == checkchart[l+d-1][m-1]):
						checkchart[l+d-1][m-1] = 1
						templist.append( (l+d-1,m-1) )

				else: #(l == 0)
					# If nothing is incoming, system idle
					VU_T[l    ][m  ][n+1] += VU_T[l][m][n] * (1 - p)
					if(0 == checkchart[l    ][m  ]):
						checkchart[l    ][m  ] = 1
						templist.append( (l    ,m  ) )

					# Sacrifice some tail proportion
					if(l+d-1 >= W):
						continue

					# If something incoming, use budget for current incoming task 
					VU_T[l+d-1][m-1][n+1] += VU_T[l][m][n] * p
					if(0 == checkchart[l+d-1][m-1]):
						checkchart[l+d-1][m-1] = 1
						templist.append( (l+d-1,m-1) )
			
			else: #(m = 0)
			# Regardless l == 0 or l > 0, we can only accumulate the thing
				VU_T[l    ][m  ][n+1] += VU_T[l][m][n] * (1 - p)
				if(0 == checkchart[l    ][m  ]):
					checkchart[l    ][m  ] = 1
					templist.append( (l    ,m  ) )

				# Sacrifice some tail proportion
				if(l+d >= W):
					continue

				# If something incoming, we can only accumulate
				VU_T[l+d  ][m  ][n+1] += VU_T[l][m][n] * p
				if(0 == checkchart[l+d  ][m  ]):
					checkchart[l+d  ][m  ] = 1
					templist.append( (l+d,m  ) )
			# End of * for (l ,m) *
		
		nz_list.append(templist)
		# End of  * for n *

	return (nz_list, VU_T) 

# The new method for getting the VU_T with a general distribution G
# Return:
# A list contains P lists to identify which joint probabality is no zero
# For Each of the P lists:
#     Contains a tuple of (V=l, U=m) to identify the one with no zero probablity
def get_BG1_DS_VU_T_list(B, P, p, exe_dist, V0):
	nz_list = []

	# initalization
	W = len(V0)
	VU_T = np.zeros((W, B + 1, P))


	templist = []
	# fill the initial number V0
	for l in range(0, W):
		VU_T[l][B][0] = V0[l]
		templist.append( (l, B) )

	nz_list.append(templist)
	
	for n in range(0, P - 1):
		templist = []
		# For each Iteration, reset the checkmark
		checkchart = np.zeros((W, B + 1))

		for (l, m) in nz_list[n]:
			#==================== (m > 0) We have no budget =====================
			if(m > 0):
				if(l > 0):
					# We have budget and we have things pending
					# If nothing incoming, use budget for already pending task
					VU_T[l-1  ][m-1][n+1] += VU_T[l][m][n] * (1 - p)
					if(0 == checkchart[l-1  ][m-1]):
						checkchart[l-1  ][m-1] = 1
						templist.append( (l-1  ,m-1) )

					# If something incoming, check all the possible duration 
					# and use budget for already pending task
					for (d, q) in exe_dist:
						if(l+d-1 < W):	 # Sacrifice some tail proportion
							VU_T[l+d-1][m-1][n+1] += VU_T[l][m][n] * p * q
							if(0 == checkchart[l+d-1][m-1]):
								checkchart[l+d-1][m-1] = 1
								templist.append( (l+d-1,m-1) )

				else: #(l == 0)
					# If we have budget and not pending task
					# if nothing is incoming, system idle
					VU_T[l    ][m  ][n+1] += VU_T[l][m][n] * (1 - p)
					if(0 == checkchart[l    ][m  ]):
						checkchart[l    ][m  ] = 1
						templist.append( (l    ,m  ) )

					# If something incoming, use budget for current incoming task 
					for (d, q) in exe_dist:
						if(l+d-1 < W):
							VU_T[l+d-1][m-1][n+1] += VU_T[l][m][n] * p * q
							if(0 == checkchart[l+d-1][m-1]):
								checkchart[l+d-1][m-1] = 1
								templist.append( (l+d-1,m-1) )

			#==================== (m = 0) We have no budget =====================
			else:
				# Regardless l == 0 or l > 0, we can only accumulate the thing
				# Nothing is incoming
				VU_T[l    ][m  ][n+1] += VU_T[l][m][n] * (1 - p)
				if(0 == checkchart[l    ][m  ]):
					checkchart[l    ][m  ] = 1
					templist.append( (l    ,m  ) )

				# If something incoming, we can only accumulate
				for (d, q) in exe_dist:
					if(l+d < W):
						VU_T[l+d  ][m  ][n+1] += VU_T[l][m][n] * p * q
						if(0 == checkchart[l+d  ][m  ]):
							checkchart[l+d  ][m  ] = 1
							templist.append( (l+d,m  ) )
			# End of If m>0
		# End of for(l ,m)
		
		nz_list.append(templist)
	# End of for n

	return (nz_list, VU_T) 

# New method for DS, which can handle d >= 2
def get_BD1_DS_R_list(B, P, p, d, VU_T, nz_list):
	(W, B1, P1) = VU_T.shape
	R = np.zeros(((W + d) / B + 1) * P)

	for n in range(0, P):
		for (l, m) in nz_list[n]:

			k = f_DS(l, m, n, B, P, d)
			R[k] += (1.0 / P) * VU_T[l][m][n]

	return R

def get_BG1_DS_R_list(B, P, p, exe_dist, VU_T, nz_list):

	max_d = 0
	for (d, q) in exe_dist:
		if (d > max_d):
			max_d = d	

	(W, B1, P1) = VU_T.shape
	R = np.zeros(((W + max_d) / B + 1) * P)

	for n in range(0, P):
		for (l, m) in nz_list[n]:
			for (d, q) in exe_dist:
				k = f_DS(l, m, n, B, P, d)
				R[k] += (1.0 / P) * VU_T[l][m][n] * q

	return R

# ==================== Finally: The Top-layer API ===================
# ============= Using B/D(XS)/1 to Approximate M/D(XS)/1 ============
def get_MDPS1_from_BDPS1(arrival_rate, service_rate, budget, period, N):
	assert(1.0 == service_rate)
	p = arrival_rate / N
	d = N
	P = int(period * N)
	B = int(budget * N)

	print p,d,P,B

	# Step 1. Get Virtual Waiting time distribution @ Start of a period (P + 0)
	# Naroah: Using the iteration
	VectorWidth = 400
	Error_cap   = 0.0001

	V0 = get_BD1_V0_iter(B, P, p, d, VectorWidth, Error_Cap)
	Vn = get_BD1_PS_Vn  (B, P, p, d, V0)
	R  = get_BD1_PS_R   (B, P, d, Vn)

	y_cdf = []
	y_cdf.append(R[0])
	for i in range(1, len(R)):
		new_item = y_cdf[i - 1] + R[i]
		y_cdf.append(new_item)
	
	x_tick = np.array(range(0, len(R))) * 1.0 / N
		
	return (x_tick, y_cdf)

def get_MDDS1_from_BDDS1(arrival_rate, service_rate, budget, period, N):
	assert(1.0 == service_rate)
	p = arrival_rate / N
	d = N
	P = int(period * N)
	B = int(budget * N)

	print p,d,P,B

	# Step 1. Get Virtual Waiting time distribution @ Start of a period (P + 0)
	# Naroah: Using the iteration
	VectorWidth = 800
	Error_cap   = 0.0001

	V0 = get_BD1_V0_iter(B, P, p, d, VectorWidth, Error_cap)
	(nz_list, VU_T) = get_BD1_DS_VU_T_list(B, P, p, d, V0)
	R  = get_BD1_DS_R_list(B, P, p, d, VU_T, nz_list)

	y_cdf = []
	y_cdf.append(R[0])
	for i in range(1, len(R)):
		new_item = y_cdf[i - 1] + R[i]
		y_cdf.append(new_item)
	
	x_tick = np.array(range(0, len(R))) * 1.0 / N
		
	return (x_tick, y_cdf)

# ================== Deprecated Version of functions ======================
# Only used for explain why pure analytical method is messy
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
# Not recommended for practical solution
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

