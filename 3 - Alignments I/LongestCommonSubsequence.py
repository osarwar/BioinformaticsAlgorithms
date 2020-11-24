import numpy as np 
from copy import copy 
import sys
# print(sys.getrecursionlimit())
sys.setrecursionlimit(2000)

"""
Name: OWAIS SARWAR

Code Challenge: Use OutputLCS (reproduced below) to solve the Longest Common Subsequence Problem.

Input: Two strings s and t.
Output: A longest common subsequence of s and t. (Note: more than one solution may exist, in which case you may output any one.)

Sample Input:

AACCTTGG
ACACTGTGA

Sample Output:

AACTGG

"""

f = open("dataset_397340_5.txt", "r")
data = f.readlines()

#s
s = data[0].strip('\n')

#t
t = data[1].strip('\n')

# s = "AACCTTGG"
# t = "ACACTGTGA"

# s = "GACT"
# t = "ATG"

# s = "ACTGAG"
# t = "GACTGG"

# s = "AC"
# t= "AC"

# s = "PLEASANTLY"
# t = "MEANLY"

def LCSBackTrack(v, w): 

	s = np.zeros((len(v)+1, len(w)+1))
	backtrack = copy(s)
	# print(s.shape)

	for i in range(len(v)+1): 
		s[i][0] = 0 
	for j in range(len(w)+1): 
		s[0][j] = 0 
	for i in range(1, len(v)+1): 
		for j in range(1, len(w)+1): 
			match = 0 
			if v[i-1] == w[j-1]: 
				match = 1 
			s[i][j] = max(s[i-1][j], s[i][j-1], s[i-1][j-1] + match)
			if s[i][j] == s[i-1][j]: 
				backtrack[i][j] = -1 #d
			elif s[i][j] == s[i][j-1]: 
				backtrack[i][j] = 1 #r
			elif s[i][j] == s[i-1][j-1] + match: 
				backtrack[i][j] = 2 #m 
			else: 
				pass 

	return backtrack

def OutputLCS(backtrack, v, i, j): 

	if i == 0 or j == 0: 
		return ""
	if backtrack[i][j] == -1: 
		return OutputLCS(backtrack, v, i-1, j)
	elif backtrack[i][j] == 1: 
		return OutputLCS(backtrack, v, i, j-1)
	else: #backtrack[i][j] == 2: 
		return OutputLCS(backtrack, v, i-1, j-1) + v[i-1]

# print(s)
# print(t)
backtrack = LCSBackTrack(s, t)
st = OutputLCS(backtrack, s, len(s), len(t))
print(st)