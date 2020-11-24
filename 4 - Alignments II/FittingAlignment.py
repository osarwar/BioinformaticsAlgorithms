import numpy as np 
from copy import copy 
import sys
# print(sys.getrecursionlimit())
sys.setrecursionlimit(3000)
"""
Code Challenge: Solve the Fitting Alignment Problem.

Input: Two nucleotide strings v and w, where v has length at most 1000 and w has length at most 100.
Output: A highest-scoring fitting alignment between v and w. Use the simple scoring method in which matches count +1 and both the mismatch and indel penalties are 1.

Sample Input:

GTAGGCTTAAGGTTA
TAGATA

Sample Output:

2
TAGGCTTA
TAGA--TA
"""

f = open("dataset_397343_5.txt", "r")
# f = open("fitting_alignment_test.txt", "r")
data = f.readlines()

#s
s = data[0].strip('\n')

#t
t = data[1].strip('\n')

# s, t = "GTAGGCTTAAGGTTA", "TAGATA"

# s, t = "CCAT", "AT"
# s, t = "GAGA", "GAT"
# s, t = "CACGTC", "AT"
# s, t = "ATCC", "AT"
# s, t = "ACGACAGAG", "CGAGAGGTT"
# s, t = "CAAGACTACTATTAG", "GG"

def OptFittingAlignmentBackTrack(v, w): 

	indel_penalty = -1
	mismatch_penalty = -1
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
	score = int(max(s[i][len(w)] for i in range(len(w), len(v)+1)))
	v_position = np.argmax(s.T[len(w)][len(w):len(v)+1], axis=None) + len(w)
	w_position = len(w)
	end_index = (v_position, w_position)
	return backtrack, score, end_index

def OutputOptFittingAlignment(backtrack, v, w, i, j, v_s, w_s): 

	if i == 0 or j == 0: 
		return ""
	if backtrack[i][j] == -1: 
		OutputOptFittingAlignment(backtrack, v, w, i-1, j, v_s, w_s)
		v_s += v[i-1]
		w_s += "-"
	elif backtrack[i][j] == 1: 
		OutputOptFittingAlignment(backtrack, v, w, i, j-1, v_s, w_s) 
		v_s += "-"
		w_s += w[j-1]
	else: #backtrack[i][j] == 2: 
		OutputOptFittingAlignment(backtrack, v, w, i-1, j-1, v_s, w_s)
		v_s += v[i-1]
		w_s += w[j-1]

backtrack, score, end_index = OptFittingAlignmentBackTrack(s, t)

print(score)
# print(backtrack)
v_s = []
w_s = []
OutputOptFittingAlignment(backtrack, s, t, end_index[0], end_index[1], v_s, w_s)
# print(v_s, w_s)
for v in v_s: 
	print(v, end="")
print()
for w in w_s: 
	print(w, end="")