import numpy as np 
from copy import copy 
import sys
# print(sys.getrecursionlimit())
sys.setrecursionlimit(3000)
"""
Code Challenge: Solve the Global Alignment Problem.

Input: Two protein strings written in the single-letter amino acid alphabet.
Output: The maximum alignment score of these strings followed by an alignment achieving this maximum score. Use the BLOSUM62 scoring matrix for matches and mismatches as well as the indel penalty σ = 5.

Sample Input:

PLEASANTLY
MEANLY

Sample Output:

8
PLEASANTLY
-MEA--N-LY
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

indel_penalty = 5 

f = open("dataset_397342_3.txt", "r")
data = f.readlines()

#s
s = data[0].strip('\n')

#t
t = data[1].strip('\n')

# s = "PLEASANTLY"
# t = "MEANLY"



def OptAlignmentBackTrack(v, w, ScoringMarix, LettertoPositionMap, indel_penalty): 

	s = np.zeros((len(v)+1, len(w)+1))
	backtrack = copy(s)

	for i in range(len(v)+1): 
		if i == 0: 
			s[i][0] = 0 
		else: 
			s[i][0] = s[i-1][0] - indel_penalty
			backtrack[i][0] = -1 #deletion 
	for j in range(len(w)+1): 
		if j == 0: 
			s[0][j] = 0 
		else: 
			s[0][j] = s[0][j-1] - indel_penalty
			backtrack[0][j] = 1 #insertion
	for i in range(1, len(v)+1): 
		for j in range(1, len(w)+1): 
			# step_score = 0 
			# indel_penalty = 0 
			# if v[i-1] == w[j-1]: 
			# 	step_score = 1 
			step_score = ScoringMarix[LettertoPositionMap[v[i-1]]][LettertoPositionMap[w[j-1]]] 
			# print(v[i-1], w[j-1], step_score)
			s[i][j] = max(s[i-1][j] - indel_penalty, s[i][j-1] - indel_penalty, s[i-1][j-1] + step_score)
			if s[i][j] == s[i-1][j] - indel_penalty: 
				backtrack[i][j] = -1 #d
			elif s[i][j] == s[i][j-1] - indel_penalty: 
				backtrack[i][j] = 1 #i
			elif s[i][j] == s[i-1][j-1] + step_score: 
				backtrack[i][j] = 2 #m/mm
			else: 
				pass 

	return backtrack, s 

def OutputOptAlignment(backtrack, v, w, i, j, v_s, w_s): 

	if i == 0 and j == 0: 
		return ""
	if backtrack[i][j] == -1: 
		OutputOptAlignment(backtrack, v, w, i-1, j, v_s, w_s)
		v_s += v[i-1]
		w_s += "-"
	elif backtrack[i][j] == 1: 
		OutputOptAlignment(backtrack, v, w, i, j-1, v_s, w_s) 
		v_s += "-"
		w_s += w[j-1]
	else: #backtrack[i][j] == 2: 
		OutputOptAlignment(backtrack, v, w, i-1, j-1, v_s, w_s)
		v_s += v[i-1]
		w_s += w[j-1]

backtrack, score = OptAlignmentBackTrack(s, t, ScoringMarix, LettertoPositionMap, indel_penalty)

print(score[len(s)][len(t)])

v_s = []
w_s = []
OutputOptAlignment(backtrack, s, t, len(s), len(t), v_s, w_s)
for v in v_s: 
	print(v, end="")
print()
for w in w_s: 
	print(w, end="")
# print(OutputOptAlignment(backtrack, t, len(t), len(s)))