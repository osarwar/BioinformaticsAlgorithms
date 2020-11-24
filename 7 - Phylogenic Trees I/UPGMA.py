import numpy as np 
from copy import copy 
import sys 
sys.setrecursionlimit(1000000)
"""
Name = Owais Sarwar

Code Challenge: Implement UPGMA.

Input: An integer n followed by a space separated n x n distance matrix.
Output: An adjacency list for the ultrametric tree returned by UPGMA. Edge weights should be accurate to two decimal places (answers in the sample dataset below are provided to three decimal places).

Note on formatting: The adjacency list must have consecutive integer node labels starting from 0. The n leaves must be labeled 0, 1, ..., n - 1 in order of their appearance in the distance matrix. Labels for internal nodes may be labeled in any order but must start from n and increase consecutively.

Sample Input:

4
0	20	17	11
20	0	20	13
17	20	0	10
11	13	10	0

Sample Output:

0->5:7.000
1->6:8.833
2->4:5.000
3->4:5.000
4->2:5.000
4->3:5.000
4->5:2.000
5->0:7.000
5->4:2.000
5->6:1.833
6->5:1.833
6->1:8.833
"""

def UPGMA(n, distance_matrix): 

	def ClosestClusters():
		min_dist = 1e10
		for i in range(len(distance_matrix)): 
			for j in range(len(distance_matrix)): 
				if distance_matrix[i][j] != 0 and distance_matrix[i][j] < min_dist and i in Clusters and j in Clusters: 
					min_dist = distance_matrix[i][j]
					cluster1 = i 
					cluster2 = j 
		return cluster1, cluster2, min_dist

	def Dist(Clusters, c_new, c, distance_matrix): 
		
		leaves_c = len(Clusters[c]); leaves_c_new = len(Clusters[c_new])

		sum_dist = 0 
		for i in Clusters[c_new]: 
			for j in Clusters[c]: 
				sum_dist += distance_matrix[i][j]

		return sum_dist / (leaves_c * leaves_c_new)


	Clusters, Age, T = {}, {}, {}
	for i in range(n): 
		Clusters[i] = [i] 
		Age[i] = 0 

	c_new = n 
	while len(Clusters) > 1: 
		clust1, clust2, dist = ClosestClusters()
		# print(clust1, clust2)
		if c_new in T.keys():
			T[c_new] += [clust1]; T[c_new] += [clust2]; 
		else: 
			T[c_new] = [clust1]; T[c_new] += [clust2]; 

		if clust1 in T.keys(): 
			T[clust1] += [c_new]
		else: 
			T[clust1] = [c_new]

		if clust2 in T.keys(): 
			T[clust2] += [c_new]
		else: 
			T[clust2] = [c_new]


		Age[c_new] = distance_matrix[clust1][clust2] / 2 
		# distance_matrix[clust1] = [0 for _ in range(len(distance_matrix))]
		# distance_matrix[clust2] = [0 for _ in range(len(distance_matrix))]
		for idx, d in enumerate(distance_matrix): 
			# distance_matrix[idx][clust1] = 0; distance_matrix[idx][clust2] = 0 
			distance_matrix[idx].append(0.000)
		distance_matrix.append([0 for _ in range(len(distance_matrix)+1)])
		Clusters[c_new] = Clusters[clust1] + Clusters[clust2]
		del Clusters[clust1]; del Clusters[clust2]
		for c in range(len(distance_matrix)-1): 
			if c in Clusters: 
				distance_matrix[c_new][c] = Dist(Clusters, c_new, c, distance_matrix)
				distance_matrix[c][c_new] = Dist(Clusters, c_new, c, distance_matrix)
		c_new += 1 
	root = Clusters[c_new-1]
	weights = {}
	for node in range(len(distance_matrix)): 
		for w in T[node]:  
			weights[node, w] = abs(Age[node] - Age[w])
			print(node, "->", w, ":", np.around(np.array([weights[node, w]])[0],3), "00", sep='')




file = open(r"UPGMA_sample.txt", "r")

# file = open(r"UPGMA_test.txt", "r")
file = open(r"dataset_397376_8.txt", "r")


data = file.readlines()

for idx, line in enumerate(data): 
	data[idx] = line.strip("\n")

n = int(data[0])

distance_matrix = np.zeros((n,n))
distance_matrix = [[0.000 for _ in range(n)] for _ in range(n)]
for idx, line in enumerate(data[1:]): 
	for idx2, val in enumerate(line.split()): 
		distance_matrix[idx][idx2] = float(val)

UPGMA(n, distance_matrix)