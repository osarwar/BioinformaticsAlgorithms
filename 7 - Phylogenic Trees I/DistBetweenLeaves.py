import numpy as np 
from copy import copy 
import sys 
sys.setrecursionlimit(50)
"""
Name = Owais Sarwar

Distances Between Leaves Problem: Compute the distances between leaves in a weighted tree.

Input:  An integer n followed by the adjacency list of a weighted tree with n leaves.
Output: An n x n matrix (di,j), where di,j is the length of the path between leaves i and j.

Code Challenge: Solve the Distances Between Leaves Problem. The tree is given as an adjacency list of a graph whose leaves are integers between 0 and n - 1; the notation a->b:c means that node a is connected to node b by an edge of weight c. The matrix you return should be space-separated.

Sample Input:

4
0->4:11
1->4:2
2->5:6
3->5:7
4->0:11
4->1:2
4->5:4
5->4:4
5->3:7
5->2:6

Sample Output:

0	13	21	22
13	0	12	13
21	12	0	13
22	13	13	0
"""
def Distance(root, node, distance, adjacency_matrix, n, visited, dist_matrix): 
	if node != root and node < n: 
		# print(root, node, int(distance))
		dist_matrix[root, node] = int(distance)
		return 
	children = np.nonzero(adjacency_matrix[node])[0]
	visited.append(node)
	for x in visited: 
		if x in children: 
			children = np.delete(children, np.where(children==x))
	# print("children:", children)
	for child in children: 
		# print("child", child) 
		Distance(root, child, distance+adjacency_matrix[node, child], adjacency_matrix, n, visited, dist_matrix)
	


def DistanceBetweenLeaves(n, adjacency_matrix): 

	dist_matrix=np.zeros((n, n))

	for start in range(n): 
		Distance(start, start, 0, adjacency_matrix, n, [], dist_matrix)

	for i in range(n): 
		for j in range(n): 
			if j != n-1: 
				print(int(dist_matrix[i, j]), end=" ")
			else: 
				print(int(dist_matrix[i, j]))

file = open(r"DistBetweenLeaves_sample.txt", "r")

file = open(r"DistBetweenLeaves_test.txt", "r")
file = open(r"dataset_397372_12.txt", "r")

data = file.readlines()

for idx, line in enumerate(data): 
	data[idx] = line.strip("\n")

n = int(data[0])

starts = []
ends = []
lens = []
for idx, line in enumerate(data[1:]): 
	first_split = line.split("->")
	starts.append(int(first_split[0]))
	second_split = first_split[1].split(":")
	ends.append(int(second_split[0]))
	lens.append(int(second_split[1]))

adjacency_matrix = np.zeros((max(starts + ends) +1, max(starts+ends)+1))

for idx, s in enumerate(starts): 
	adjacency_matrix[s, ends[idx]] = lens[idx]
# print(adjacency_matrix)


DistanceBetweenLeaves(n, adjacency_matrix)


