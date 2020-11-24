import numpy as np 
from copy import copy 
import sys
# print(sys.getrecursionlimit())
sys.setrecursionlimit(3000)
"""
Edit Distance Problem: Find the edit distance between two strings.

Input: Two strings.
Output: The edit distance between these strings.

Code Challenge: Solve the Edit Distance Problem.

Sample Input:

PLEASANTLY
MEANLY

Sample Output:

5
"""

f = open("dataset_397343_3.txt", "r")
# f = open("edit_distance_test.txt", "r")
data = f.readlines()

#s
s = data[0].strip('\n')

#t
t = data[1].strip('\n')

# s = "PLEASANTLY"
# t = "MEANLY"



def editDistance(v, w): 

	s = np.zeros((len(v)+1, len(w)+1))

	for i in range(len(v)+1): 
		if i == 0: 
			s[i][0] = 0 
		else: 
			s[i][0] = s[i-1][0] + 1 
	for j in range(len(w)+1): 
		if j == 0: 
			s[0][j] = 0 
		else: 
			s[0][j] = s[0][j-1] + 1 
	for i in range(1, len(v)+1): 
		for j in range(1, len(w)+1): 
			step_penalty = 1
			if v[i-1] == w[j-1]: 
				step_penalty = 0 
			s[i][j] = min(s[i-1][j] + 1, s[i][j-1] + 1 , s[i-1][j-1] + step_penalty)
#			if s[i][j] == s[i-1][j] + 1: 
#				backtrack[i][j] = -1 #d
#			elif s[i][j] == s[i][j-1] + 1 : 
#				backtrack[i][j] = 1 #i
#			elif s[i][j] == s[i-1][j-1] + step_score: 
#				backtrack[i][j] = 2 #m/mm
#			else: 
#				pass 
	return int(s[len(v)][len(w)])

s = editDistance(s, t)
print(s)
# print(OutputOptAlignment(backtrack, t, len(t), len(s)))