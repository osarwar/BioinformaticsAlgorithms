import numpy as np 
from copy import copy 
import sys 
sys.setrecursionlimit(50)
"""
Name = Owais Sarwar

Code Challenge: Solve the Limb Length Problem.

Input: An integer n, followed by an integer j between 0 and n - 1, followed by a space-separated additive distance matrix D (whose elements are integers).
Output: The limb length of the leaf in Tree(D) corresponding to row j of this distance matrix (use 0-based indexing).

Sample Input:

4
1
0	13	21	22
13	0	12	13
21	12	0	13
22	13	13	0

Sample Output:

2
"""

def LimbLength(n, leaf, distance_matrix): 

	min_value = 1000
	min_i = 0 
	min_k = 0 

	for i in range(n): 
		for k in range(n): 
			value = (distance_matrix[i,leaf] + distance_matrix[leaf,k] - distance_matrix[i, k]) / 2 
			if value < min_value and i != leaf and k != leaf: 
				min_value = copy(value)
				min_i = copy(i)
				min_k = copy(k)

	LimbLength_leaf = int(min_value)
	return LimbLength_leaf

file = open(r"LimbLength_sample.txt", "r")

file = open(r"LimbLength_test.txt", "r")
file = open(r"dataset_397373_11.txt", "r")
file = open(r"LimbLength_quiz.txt", "r")

data = file.readlines()

for idx, line in enumerate(data): 
	data[idx] = line.strip("\n")

n = int(data[0])
leaf = int(data[1])

distance_matrix = np.zeros((n,n))
for idx, line in enumerate(data[2:]): 
	for idx2, val in enumerate(line.split()): 
		distance_matrix[idx, idx2] = int(val)


print(LimbLength(n, leaf, distance_matrix))