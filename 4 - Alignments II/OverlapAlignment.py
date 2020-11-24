import numpy as np 
from copy import copy 
import sys
# print(sys.getrecursionlimit())
sys.setrecursionlimit(3000)
"""
Code Challenge: Solve the Overlap Alignment Problem.

Input: Two strings v and w, each of length at most 1000.
Output: The score of an optimal overlap alignment of v and w, followed by an alignment of a suffix v' of v and a prefix w' of w achieving this maximum score. Use an alignment score in which matches count +1 and both the mismatch and indel penalties are 2.

Sample Input:

PAWHEAE
HEAGAWGHEE

Sample Output:

1
HEAE
HEAG
"""

f = open("dataset_397343_7.txt", "r")
# f = open("overlap_alignment_test.txt", "r")
data = f.readlines()

#s
s = data[0].strip('\n')

#t
t = data[1].strip('\n')

# s, t = "PAWHEAE", "HEAGAWGHEE"
# s, t = "GAGA", "GAT"
# s, t = "ATCACT", "AT"
# s, t = "CAGAGATGGCCG", "ACG"


def OptOverlapAlignmentBackTrack(v, w): 

	indel_penalty = -2
	mismatch_penalty = -2
	match_reward = 1

	s = np.zeros((len(v)+1, len(w)+1))
	backtrack = copy(s)

	for i in range(len(v)+1): 
		if i == 0: 
			s[i][0] = 0 
		else: 
			s[i][0] = s[i-1][0] 
			backtrack[i][0] = -1 #deletion 
	for j in range(len(w)+1): 
		if j == 0: 
			s[0][j] = 0 
		else: 
			s[0][j] = s[0][j-1]
			backtrack[0][j] = 1 #insertion
	for i in range(1, len(v)+1): 
		for j in range(1, len(w)+1): 

			if v[i-1] == w[j-1]: 
				step_score = match_reward 
			else: 
				step_score = mismatch_penalty

			s[i][j] = max(s[i-1][j] + indel_penalty, s[i][j-1] + indel_penalty, s[i-1][j-1] + step_score)
			
			if s[i][j] == s[i-1][j] + indel_penalty: 
				backtrack[i][j] = -1 #d
			elif s[i][j] == s[i][j-1] + indel_penalty: 
				backtrack[i][j] = 1 #i
			elif s[i][j] == s[i-1][j-1] + step_score: 
				backtrack[i][j] = 2 #m/mm
			else: 
				pass 

	# print(s)
	# score = int(max(np.max(s[-1]), np.max(s.T[-1])))
	# if np.max(s[-1]) > np.max(s.T[-1]): 
	# 	v_position = len(v)
	# 	w_position = np.argmax(s[len(v)]) 
	# else: 
	# 	v_position = np.argmax(s[len(w)]) 
	# 	w_position = len(w)

	score = int(np.max(s[-1]))
	v_position = len(v)
	w_position = np.argmax(s[len(v)])

	end_index = (v_position, w_position)
	return backtrack, score, end_index

def OutputOptOverlapAlignment(backtrack, v, w, i, j, v_s, w_s): 

	if i == 0 or j == 0: 
		return ""
	if backtrack[i][j] == -1: 
		OutputOptOverlapAlignment(backtrack, v, w, i-1, j, v_s, w_s)
		v_s += v[i-1]
		w_s += "-"
	elif backtrack[i][j] == 1: 
		OutputOptOverlapAlignment(backtrack, v, w, i, j-1, v_s, w_s) 
		v_s += "-"
		w_s += w[j-1]
	else: #backtrack[i][j] == 2: 
		OutputOptOverlapAlignment(backtrack, v, w, i-1, j-1, v_s, w_s)
		v_s += v[i-1]
		w_s += w[j-1]

backtrack, score, end_index = OptOverlapAlignmentBackTrack(s, t)

print(score)
# print(backtrack)
v_s = []
w_s = []
OutputOptOverlapAlignment(backtrack, s, t, end_index[0], end_index[1], v_s, w_s)
# print(v_s, w_s)
for v in v_s: 
	print(v, end="")
print()
for w in w_s: 
	print(w, end="")