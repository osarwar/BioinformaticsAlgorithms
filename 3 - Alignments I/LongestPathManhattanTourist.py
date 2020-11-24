import numpy as np 
from copy import copy 
"""
Name: OWAIS SARWAR

Code Challenge: Find the length of a longest path in the Manhattan Tourist Problem.

Input: Integers n and m, followed by an n × (m + 1) matrix Down and an (n + 1) × m matrix Right. The two matrices are separated by the "-" symbol.
Output: The length of a longest path from source (0, 0) to sink (n, m) in the rectangular grid whose edges are defined by the matrices Down and Right.

Sample Input:

4 4
1 0 2 4 3
4 6 5 2 1
4 4 5 2 1
5 6 8 5 3
-
3 2 4 0
3 2 4 2
0 7 3 3
3 3 0 2
1 3 2 2

Sample Output:

34

"""

f = open("dataset_397338_10.txt", "r")
data = f.readlines()

#N
N = int(data[0].strip('\n').split(" ")[0])

#M
M = int(data[0].strip('\n').split(" ")[1])

Down, Right = [], []
right_hit = False

for line in data[1:]: 
	if right_hit == True: 
		Right.append([int(i) for i in line.strip('\n').split(" ")])
	if right_hit == False and "-" not in line.strip('\n').split(" "): 
		Down.append([int(i) for i in line.strip('\n').split(" ")])
	if "-" in line.strip('\n'): 
		right_hit = True 

Down = np.array(Down)
Right = np.array(Right)

# N, M = 4, 4 
# Down = np.array([[1, 0, 2, 4, 3], [4, 6, 5, 2, 1], [4, 4, 5, 2, 1], [5, 6, 8, 5, 3]])
# Right = np.array([[3, 2, 4, 0], [3, 2, 4, 2], [0 ,7, 3, 3], [3, 3, 0, 2], [1, 3, 2, 2]])

def ManhattanTourist(n, m, down, right): 
	s = np.zeros((n+1, m+1))

	for i in range(1,n+1): 
		s[i][0] = s[i-1][0] + down[i-1][0]
	for j in range(1, m+1): 
		s[0][j] = s[0][j-1] + right[0][j-1]
	for i in range(1, n+1): 
		for j in range(1, m+1): 
			s[i][j] = max(s[i-1][j] + down[i-1][j], s[i][j-1] + right[i][j-1])

	return int(s[n][m])

print(ManhattanTourist(N,M,Down,Right))