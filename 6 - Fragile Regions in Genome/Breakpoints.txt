import numpy as np 
from copy import copy 
"""
Name = Owais Sarwar

Number of Breakpoints Problem: Find the number of breakpoints in a permutation.

Input: A permutation.
Output: The number of breakpoints in this permutation.

Code Challenge: Solve the Number of Breakpoints Problem.

Extra Dataset

Sample Input:

+3 +4 +5 -12 -8 -7 -6 +1 +2 +10 +9 -11 +13 +14

Sample Output:

8
"""

file = open(r"Breakpoints_sample.txt", "r")
file = open(r"dataset_397357_6.txt", "r")
# file = open(r"Breakpoints_test.txt", "r"))
data = file.readlines()

permutation = data[0].strip('\n').split(" ")

for idx, p in enumerate(permutation): 
	permutation[idx] = int(p)
permutation = [20, 8, 9, 10, 11, 12, 18, -7, -6, -14, 2, -17, -16, -15, 1, 4, 13, -5, 3, -19]
# print(permutation)

def NumberOfBreakpoints(permutation): 

	n = len(permutation)+1
	permutation.append(n)
	permutation.insert(0, 0)

	num_breakpoints = 0 
	for idx, p in enumerate(permutation): 
		if idx != len(permutation) -1: 
			if abs(permutation[idx+1]) not in [abs(p) + 1, abs(p) -1]: 
				num_breakpoints += 1 
			elif abs(permutation[idx+1]) > abs(p): 
				if np.sign(permutation[idx+1]) != np.sign(p) and np.sign(p) != 0: 
					num_breakpoints += 1 
			else: 
				if np.sign(permutation[idx+1]) == 1 or np.sign(p) == 1: 
					num_breakpoints += 1 

	return num_breakpoints

NB = NumberOfBreakpoints(permutation)

print(NB)