import numpy as np 
from copy import copy, deepcopy
import sys 
sys.setrecursionlimit(1000000)
"""
Name = Owais Sarwar

Code Challenge: Implement NeighborJoining.

Input: An integer n, followed by an n x n distance matrix.
Output: An adjacency list for the tree resulting from applying the neighbor-joining algorithm. Edge-weights should be accurate to two decimal places (they are provided to three decimal places in the sample output below).

Note on formatting: The adjacency list must have consecutive integer node labels starting from 0. The n leaves must be labeled 0, 1, ..., n - 1 in order of their appearance in the distance matrix. Labels for internal nodes may be labeled in any order but must start from n and increase consecutively.


Sample Input:

4
0	23	27	20
23	0	30	28
27	30	0	30
20	28	30	0

Sample Output:

0->4:8.000
1->5:13.500
2->5:16.500
3->4:12.000
4->5:2.000
4->0:8.000
4->3:12.000
5->1:13.500
5->2:16.500
5->4:2.000
"""

def NJMatrix(D):
	D_star = deepcopy(D)
	TotalDistance = []
	for leaf in D: 
		TotalDistance.append(sum(leaf))
	n = len(D_star)
	for i in range(n): 
		for j in range(n):
			if i != j: 
				D_star[i][j] = (n-2) * D[i][j] - TotalDistance[i] - TotalDistance[j]
	return D_star, TotalDistance

def minDistance(D_star): 
	min_dist = 1e10
	for i in range(len(D_star)): 
		for j in range(len(D_star)): 
			if D_star[i][j] != 0 and D_star[i][j] < min_dist: 
				min_dist = D_star[i][j]
				leaf1 = i 
				leaf2 = j 
	return leaf1, leaf2

def NeighborhoodJoining(D, leaves, new_leaf): 
	print(D)
	print(leaves)
	n = len(D)
	if n == 2: 
		T = {}
		T[leaves[0]] = [str(leaves[1]) + ':' + str(D[0][1])]; T[leaves[1]] = [str(leaves[0]) + ':' + str(D[0][1])]
		print(T)
		return T 
	D_star, TotalDistance = NJMatrix(D)
	i, j = minDistance(D_star)
	print(i, j)
	delta = (TotalDistance[i] - TotalDistance[j]) / (n-2)
	limbLength_i = (1/2) * (D[i][j] + delta); leaf_i = leaves[i]
	limbLength_j = (1/2) * (D[i][j] - delta); leaf_j = leaves[j]
	print(limbLength_j, limbLength_i)
	new_row_D = []
	for k, row in enumerate(D):
		row.append((1/2) * (D[k][i] + D[k][j] - D[i][j]))
		new_row_D.append(row[-1])
	new_row_D.append(0.00)
	D.append(new_row_D); leaves.append(new_leaf)
	old_D = deepcopy(D); old_leaves = deepcopy(leaves)
	for idx, row in enumerate(D): 
		# print(old_D[idx][i], old_D[idx][j]);
		D[idx].remove(old_D[idx][i]); D[idx].remove(old_D[idx][j])
	old_D = deepcopy(D)
	D.remove(old_D[i]); D.remove(old_D[j]); leaves.remove(old_leaves[i]); leaves.remove(old_leaves[j])
	T = NeighborhoodJoining(D, leaves, new_leaf+1)
	T[new_leaf] += [str(leaf_i) + ':' + str(limbLength_i)]; T[new_leaf] += [str(leaf_j) + ':' + str(limbLength_j)]; 
	T[leaf_i] = [str(new_leaf) + ':' + str(limbLength_i)]; T[leaf_j] = [str(new_leaf) + ':' + str(limbLength_j)]; 
	print(T)
	return T 



file = open(r"NeighborJoining_sample.txt", "r")

file = open(r"NeighborJoining_test.txt", "r")
file = open(r"dataset_397377_7.txt", "r")
file = open(r"NJ_sc.txt", "r")

data = file.readlines()

for idx, line in enumerate(data): 
	data[idx] = line.strip("\n")

n = int(data[0])

distance_matrix = [[0.000 for _ in range(n)] for _ in range(n)]
for idx, line in enumerate(data[1:]): 
	for idx2, val in enumerate(line.split()): 
		distance_matrix[idx][idx2] = float(val)
leaves = [i for i in range(n)]
new_leaf = n
T = NeighborhoodJoining(distance_matrix, leaves, new_leaf)
nodes = list(T.keys())
nodes.sort()
for node in nodes:
	for elem in T[node]: 
		print(node, '->', elem, 0, sep='')