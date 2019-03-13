181126: Build the first Exponential CDF comparison
181127: 
	Add M/D/1 theoretical control parameter experiment in ./src
	M/D(DS)/1 implementation finished. Recursive Sanity Check Passed
181128:
	Reconstruct the code base

	Executables:
	run_MD1.py:    Run MD1   system once; compare the response time distribution with the theoretical result
	run_MDDS1.py:  Run MDDS1 system once; compare the response time distribution with the theoretical result

	run_P2_Bwvar.py : Run MDDS1 system multiple times, with a constant P,  while varying Bw
	run_Bw60_Pvar.py: Run MDDS1 system multiple times, with a constant Bw, while varying P
181130:
	Implement the Periodic Server, for DS_worst simluation

190108:
	Adding a Saving Server, means a DS can potentially overrun.

190306:
    Adding a Simplified the model:
    Using Discrete time simulation, say, changing the model from M/D/1 to
    Bernoulli / D / 1, and where D = 1

    Goal: Prove the Queuing Length (and effectivly the Virtual Waiting time) at statistical equilibrim
        of a DS server at every start of the Period
        has the same distribution 
        of a related PS server (off-period first) at every start of the Period.

	For a discrete process:
	The arrival   @ n-th slot means the arrival time is actually n+;
    The departure @ n-th slot means the arrival time is actually n-;
	E.g. A customer arrivals at 7th slot, and service time is 2:
         The customer arrives at time 7+, and leaves at time 9-. 

190313:
	B/D/1 (DS) analytical solution finished
               response time distribution can be found with analytical method.
               and that meets our expectation


