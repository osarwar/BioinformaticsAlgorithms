import numpy as np 
from copy import copy 
"""
Code Challenge: Implement the Viterbi algorithm solving the Decoding Problem.

Input: A string x, followed by the alphabet from which x was constructed, followed by the states States, transition matrix Transition, and emission matrix Emission of an HMM (Σ, States, Transition, Emission).
Output: A path that maximizes the (unconditional) probability Pr(x, π) over all possible paths π

Sample Input:

xyxzzxyxyy
--------
x y z
--------
A B
--------
	A	B
A	0.641	0.359
B	0.729	0.271
--------
	x	y	z
A	0.117	0.691	0.192	
B	0.097	0.42	0.483

Sample Output:

AAABBAAAAA
"""

file = open("ViterbiAlgorithm_test.txt", "r")
file = open("dataset_397438_7.txt", "r")
data = file.readlines()

string = data[0].strip('\n')
# print(string)
alphabet = data[2].strip('\n').split(" ")
# # print(alphabet)
States = data[4].strip('\n').split(' ')
# # print(States)

Transition = np.zeros((len(States), len(States)))
# # print(data)
for i in range(len(States)): 
	data_s = data[7+i].strip('\n').split('\t')
	for j in range(len(States)): 
		Transition[i][j] = float(data_s[1+j])

# print(Transition)
Emission = np.zeros((len(States), len(alphabet)))

for i in range(len(States)): 
	data_s = data[9+len(States)+i].strip('\n').split('\t')
	for j in range(len(alphabet)): 
		Emission[i][j] = float(data_s[1+j])

# print(Emission)

# string = "66661"
# alphabet = ["1", "2", "3", "4", "5", "6"]
# States = ["F", "Lh", "Ll"]
# Transition = np.array([[2/5, 1/10, 1/2],[1/5, 3/5, 1/5],[1, 0, 0]])
# Emission = np.array([[1/6, 1/6, 1/6, 1/6, 1/6, 1/6],[1/12, 1/12, 1/12, 1/12, 1/3, 1/3], [1/3, 1/3, 1/12, 1/12, 1/12, 1/12]])

def ViterbiAlgorithm(string, alphabet, States, Transition): 

	intial_trans_p = 1 / len(States)

	initial_source_score = 1 

	s = np.zeros((len(States), len(string)))

	backtrack = copy(s)

	alphabet_to_index_map = {}
	for idx, letter in enumerate(alphabet): 
		alphabet_to_index_map[letter] = idx 

	for i in range(0, len(string)): 
		for k in range(len(States)): 

			# if k == 0: 
			# 	intial_trans_p = 1 
			# else: 
			# 	intial_trans_p = 0 
			if i == 0: 
				s[k][i] = initial_source_score * intial_trans_p * Emission[k][alphabet_to_index_map[string[i]]]
			else: 
				scores = [s[l][i-1] * Transition[l][k] * Emission[k][alphabet_to_index_map[string[i]]] for l in range(len(States))]
				s[k][i] = max(scores)
				backtrack[k][i-1] = int(scores.index(s[k][i]))

	last_scores = [s[l][len(string)-1] for l in range(len(States))]			
	sink_score = max(last_scores)
	max_last_state = last_scores.index(sink_score)
	OutputStateSequence(backtrack, States, max_last_state, len(string)-1)


def OutputStateSequence(backtrack, States, k, n): 
	# print(k, n)
	if n == -1: 
		return " "
	else: 
		OutputStateSequence(backtrack, States, int(backtrack[k][n]), int(n-1))
		print(States[int(backtrack[k][n])], end='')


ViterbiAlgorithm(string, alphabet, States, Transition)