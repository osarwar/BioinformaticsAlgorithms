import numpy as np 
from copy import copy 
import sys
# print(sys.getrecursionlimit())
sys.setrecursionlimit(3000)
"""
Code Challenge: Solve the Multiple Longest Common Subsequence Problem.

Input: Three DNA strings of length at most 10.
Output: The length of a longest common subsequence of these three strings, followed by a multiple alignment of the three strings corresponding to such an alignment.

Sample Input:

ATATCCG
TCCGA
ATGTACTG

Sample Output:

3
ATATCC-G-
---TCC-GA
ATGTACTG-
"""

f = open("dataset_397346_5.txt", "r")
# f = open("multiple_longest_common_subsequence_test.txt", "r")
data = f.readlines()

#s
s = data[0].strip('\n')

#t
t = data[1].strip('\n')

#u 
u = data[2].strip('\n')

# s, t, u = "ATATCCG", "TCCGA", "ATGTACTG"


def OptMultAlignmentBackTrack(v, w, x): 

	s = np.zeros((len(v)+1, len(w)+1, len(x)+1))
	backtrack = copy(s)

	for i in range(len(v)+1): 
		backtrack[i][0][0] = 1 #deletion 
		for j in range(len(w)+1):
			backtrack[i][j][0] = 4
		for k in range(len(x)+1):
			backtrack[i][0][k] = 5
	for j in range(len(w)+1): 
		backtrack[0][j][0] = 2 #insertion
		for k in range(len(x)+1):
			backtrack[0][j][k] = 6
	for k in range(len(x)+1): 
		backtrack[0][0][k] = 3

	for i in range(1, len(v)+1): 
		for j in range(1, len(w)+1): 
			for k in range(1, len(x)+1):
				step_score = 0 
				if v[i-1] == w[j-1] == x[k-1]: 
					step_score = 1 

				s[i][j][k] = np.max([s[i-1][j][k], s[i][j-1][k], s[i][j][k-1], 
					s[i-1][j-1][k], s[i-1][j][k-1], s[i][j-1][k-1], s[i-1][j-1][k-1] + step_score])
				backtrack_value = np.argmax([s[i-1][j][k], s[i][j-1][k], s[i][j][k-1], 
					s[i-1][j-1][k], s[i-1][j][k-1], s[i][j-1][k-1], s[i-1][j-1][k-1] + step_score])
				backtrack[i][j][k] = backtrack_value+1 

	score = s[-1][-1][-1]
	# print(s)
	return backtrack, int(score)

def OutputOptMultAlignment(backtrack, v, w, x, i, j, k, v_s, w_s, x_s): 

	if i == 0 and j == 0 and k == 0: 
		return ""
	if backtrack[i][j][k] == 1: 
		OutputOptMultAlignment(backtrack, v, w, x, i-1, j, k, v_s, w_s, x_s)
		v_s += v[i-1]
		w_s += "-"
		x_s += "-"
	elif backtrack[i][j][k] == 2: 
		OutputOptMultAlignment(backtrack, v, w, x, i, j-1, k, v_s, w_s, x_s) 
		v_s += "-"
		w_s += w[j-1]
		x_s += "-"
	elif backtrack[i][j][k] == 3: 
		OutputOptMultAlignment(backtrack, v, w, x, i, j, k-1, v_s, w_s, x_s) 
		v_s += "-"
		w_s += "-"
		x_s += x[k-1]
	elif backtrack[i][j][k] == 4: 
		OutputOptMultAlignment(backtrack, v, w, x, i-1, j-1, k, v_s, w_s, x_s) 
		v_s += v[i-1]
		w_s += w[j-1]
		x_s += "-"
	elif backtrack[i][j][k] == 5: 
		OutputOptMultAlignment(backtrack, v, w, x, i-1, j, k-1, v_s, w_s, x_s) 
		v_s += v[i-1]
		w_s += "-"
		x_s += x[k-1]
	elif backtrack[i][j][k] == 6: 
		OutputOptMultAlignment(backtrack, v, w, x, i, j-1, k-1, v_s, w_s, x_s) 
		v_s += "-"
		w_s += w[j-1]
		x_s += x[k-1]
	elif backtrack[i][j][k]  == 7: 
		OutputOptMultAlignment(backtrack, v, w, x, i-1, j-1, k-1, v_s, w_s, x_s)
		v_s += v[i-1]
		w_s += w[j-1]
		x_s += x[k-1]
	else: 
		pass 

backtrack, score = OptMultAlignmentBackTrack(s, t, u)

print(score)
# print(backtrack)
v_s = []
w_s = []
x_s = []
OutputOptMultAlignment(backtrack, s, t, u, len(s), len(t), len(u), v_s, w_s, x_s)
for v in v_s: 
	print(v, end="")
print()
for w in w_s: 
	print(w, end="")
print()
for x in x_s: 
	print(x, end="")