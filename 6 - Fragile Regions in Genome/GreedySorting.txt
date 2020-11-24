import numpy as np 
from copy import copy 
"""
Name = Owais Sarwar

Code Challenge: Implement GreedySorting.

Input: A permutation P.
Output: The sequence of permutations corresponding to applying GreedySorting to P, ending with the identity permutation.

Sample Input:

-3 +4 +1 +5 -2

Sample Output:

-1 -4 +3 +5 -2
+1 -4 +3 +5 -2
+1 +2 -5 -3 +4
+1 +2 +3 +5 +4
+1 +2 +3 -4 -5
+1 +2 +3 +4 -5
+1 +2 +3 +4 +5
"""

file = open(r"GreedySorting_sample.txt", "r")
file = open(r"dataset_397356_4.txt", "r")
data = file.readlines()
output = open("greedyresults.txt", "w")
permutation = data[0].strip('\n').split(" ")

for idx, p in enumerate(permutation): 
	permutation[idx] = int(p)
permutation = [+6, -12, -9, +17, +18, -4, +5, -3, +11, +19, +14, +10, +8, +15, -13, +20, +2, +7, -16, -1]
print(permutation)

def GreedySorting(permutation, output): 

	approxReversalDistance = 0 
	for k in range(1, len(permutation) + 1): 
		if permutation[k-1] != k: 
			end_idx = list(map(abs, permutation)).index(k)
			reverse = permutation.copy()[k-1:end_idx+1][::-1]
			for i in range(len(reverse)): 
				permutation[k-1+i] = -1*reverse[i]
			for idx, p in enumerate(permutation): 
				if idx != len(permutation)-1:
					if p > 0: 
						print("+",p, sep='', end=" ", file=output)
					else: 
						print(p, end=" ", file=output)
				else:
					if p > 0: 
						print("+",p, sep='', file=output)
					else: 
						print(p, file=output) 

			approxReversalDistance += 1 
		if permutation[k-1] == -k: 
			permutation[k-1] = k 
			for idx, p in enumerate(permutation): 
				if idx != len(permutation)-1:
					if p > 0: 
						print("+",p, sep='', end=" ", file=output)
					else: 
						print(p, end=" ", file=output)
				else:
					if p > 0: 
						print("+",p, sep='', file=output)
					else: 
						print(p, file=output) 
			approxReversalDistance += 1 

	return approxReversalDistance

dist = GreedySorting(permutation, output)

print(dist)