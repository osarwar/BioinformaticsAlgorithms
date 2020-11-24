import numpy as np 
from copy import copy 
import sys
# print(sys.getrecursionlimit())
sys.setrecursionlimit(3000)
"""
Code Challenge: Solve the Alignment with Affine Gap Penalties Problem.

Input: Two amino acid strings v and w (each of length at most 100).
Output: The maximum alignment score between v and w, followed by an alignment of v and w achieving this maximum score. Use the BLOSUM62 scoring matrix, a gap opening penalty of 11, and a gap extension penalty of 1.

Sample Input:

PRTEINS
PRTWPSEIN

Sample Output:

8
PRT---EINS
PRTWPSEIN-

"""

ScoringFile = open("BLOSUM62.txt", "r")

Score = ScoringFile.readlines()

for s, line in enumerate(Score):
	Score[s] = line.strip('\n').split()

LettertoPositionMap = {}
for a, letter in enumerate(Score[0]): 
	LettertoPositionMap[letter] = a 

ScoringMarix = np.zeros((len(Score[0]), len(Score[0])))

for i in range(1, len(Score[0])+1): 
	for j in range(1, len(Score[0])+1): 
		ScoringMarix[i-1][j-1] = int(Score[i][j])


f = open("dataset_397344_8.txt", "r")
# f = open("alignment_affine_gap_penalties_test.txt", "r")
data = f.readlines()

#s
s = data[0].strip('\n')

#t
t = data[1].strip('\n')

# s, t = "PRTEINS", "PRTWPSEIN"
# s, t = "GA", "GTTA"
# s, t = "TTT", "TT"
# s, t = "GAT", "AT"
# s, t = "CCAT", "GAT"
# s, t = "CAGGT", "TAC"
# s, t = "GTTCCAGGTA", "CAGTAGTCGT"
# s, t = "AGCTAGCCTAG", "GT"
# s, t = "AA", "CAGTGTCAGTA"
# s, t = "ACGTA", "ACT"

def OptGlobalAffinePenaltyAlignmentBackTrack(v, w, ScoringMarix, LettertoPositionMap): 

	match_score = 5
	mismatch_penalty = -2
	gap_opening_penalty = 11
	gap_extension_penalty = 1

	s_l = np.zeros((len(v)+1, len(w)+1))
	s_m = np.zeros((len(v)+1, len(w)+1))
	s_u = np.zeros((len(v)+1, len(w)+1))

	backtrack_l, backtrack_m, backtrack_u = copy(s_m), copy(s_m), copy(s_m)

	s_u[0][0], s_l[0][0] = -gap_opening_penalty, -gap_opening_penalty

	for i in range(1, len(v)+1): 
		if i == 1: 
			s_m[i][0] = -gap_opening_penalty
		else: 
			s_m[i][0] = s_m[i-1][0] - gap_extension_penalty
		s_u[i][0] = -1e5
		backtrack_u[i][0] = 0


	for j in range(1, len(w)+1): 
		if j == 1: 
			s_m[0][j] = -gap_opening_penalty
		else: 
			s_m[0][j] = s_m[0][j-1] - gap_extension_penalty
		s_l[0][j] = -1e5
		backtrack_l[0][j] = 0
					
	for i in range(1, len(v)+1): 
		for j in range(1, len(w)+1): 

			s_l[i][j] = max(s_l[i-1][j] - gap_extension_penalty, s_m[i-1][j] - gap_opening_penalty)

			if s_l[i][j] == s_l[i-1][j] - gap_extension_penalty: 
				backtrack_l[i][j] = -1 #d + ext
			else:# s_l[i][j] == s_m[i-1][j] - gap_opening_penalty: 
				backtrack_l[i][j] = 0 #d 

			s_u[i][j] = max(s_u[i][j-1] - gap_extension_penalty, s_m[i][j-1] - gap_opening_penalty)

			if s_u[i][j] == s_u[i][j-1] - gap_extension_penalty: 
				backtrack_u[i][j] = 1 #i + ext 
			else:# s_m[i][j-1] - gap_opening_penalty: 
				backtrack_u[i][j] = 0 #i

			step_score = ScoringMarix[LettertoPositionMap[v[i-1]]][LettertoPositionMap[w[j-1]]] 

			# if v[i-1] == w[j-1]: 
			# 	step_score = match_score
			# else:
			# 	step_score = mismatch_penalty

			s_m[i][j] = max(s_l[i][j], s_u[i][j], s_m[i-1][j-1] + step_score)

			if s_m[i][j] == s_l[i][j]: 
				backtrack_m[i][j] = -1 #d
			elif s_m[i][j] == s_u[i][j]: 
				backtrack_m[i][j] = 1 #i
			elif s_m[i][j] == s_m[i-1][j-1] + step_score: 
				backtrack_m[i][j] = 2 #m/mm
			else: 
				pass
	# print(s_l)
	# print(s_m)
	# print(s_u)
	return backtrack_l, backtrack_m, backtrack_u, int(s_m[i][j])

def OutputOptGlobalAffinePenaltyAlignment(backtrack_l, backtrack_m, backtrack_u, which_backtrack, v, w, i, j, v_s, w_s): 

	if i == 0 and j == 0: 
		return ""
	if which_backtrack == "m": 
		if backtrack_m[i][j] == -1: 
			OutputOptGlobalAffinePenaltyAlignment(backtrack_l, backtrack_m, backtrack_u, "l", v, w, i, j, v_s, w_s)
			# v_s += v[i-1]
			# w_s += "-"
		elif backtrack_m[i][j] == 1: 
			OutputOptGlobalAffinePenaltyAlignment(backtrack_l, backtrack_m, backtrack_u, "u", v, w, i, j, v_s, w_s) 
			# v_s += "-"
			# w_s += w[j-1]
		elif backtrack_m[i][j] == 2: 
			OutputOptGlobalAffinePenaltyAlignment(backtrack_l, backtrack_m, backtrack_u, "m", v, w, i-1, j-1, v_s, w_s)
			v_s += v[i-1]
			w_s += w[j-1]
		else:  
			pass

	if which_backtrack == "l": 
		if backtrack_l[i][j] == -1: 
			OutputOptGlobalAffinePenaltyAlignment(backtrack_l, backtrack_m, backtrack_u, "l", v, w, i-1, j, v_s, w_s)
			v_s += v[i-1]
			w_s += "-"
		else: #backtrack_l[i][j] == 1: 
			OutputOptGlobalAffinePenaltyAlignment(backtrack_l, backtrack_m, backtrack_u, "m", v, w, i-1, j, v_s, w_s)
			v_s += v[i-1]
			w_s += "-"
			

	if which_backtrack == "u": 
		if backtrack_u[i][j] == 1: 
			OutputOptGlobalAffinePenaltyAlignment(backtrack_l, backtrack_m, backtrack_u, "u", v, w, i, j-1, v_s, w_s)
			v_s += "-"
			w_s += w[j-1]
		else: #backtrack_u[i][j] == 1: 
			OutputOptGlobalAffinePenaltyAlignment(backtrack_l, backtrack_m, backtrack_u, "m", v, w, i, j-1, v_s, w_s) 
			v_s += "-"
			w_s += w[j-1]


backtrack_l, backtrack_m, backtrack_u, score = OptGlobalAffinePenaltyAlignmentBackTrack(s, t, ScoringMarix, LettertoPositionMap)

# print(backtrack_l)
# print(backtrack_m)
# print(backtrack_u)

print(score)
v_s = []
w_s = []
OutputOptGlobalAffinePenaltyAlignment(backtrack_l, backtrack_m, backtrack_u, "m", s, t, len(s), len(t), v_s, w_s)
for v in v_s: 
	print(v, end="")
print()
for w in w_s: 
	print(w, end="")