import numpy as np 
from copy import copy 
"""
Sequence Alignment with Profile HMM Problem: Align a new sequence to a family of sequences using a profile HMM.

Input: A multiple alignment Alignment, a threshold θ, a pseudocount value σ, and a string Text.
Output: An optimal hidden path emitting Text in HMM(Alignment, θ, σ).

Code Challenge: Solve the Sequence Alignment with Profile HMM Problem.

Input: A string x followed by a threshold θ and a pseudocount σ, followed by an alphabet Σ, followed by a multiple alignment Alignment whose strings are formed from Σ.
Output: An optimal hidden path emitting x in HMM(Alignment, θ, σ).

Sample Input:

AEFDFDC
--------
0.4 0.01
--------
A B C D E F
--------
ACDEFACADF
AFDA---CCF
A--EFD-FDC
ACAEF--A-C
ADDEFAAADF

Sample Output:

M1 D2 D3 M4 M5 I5 M6 M7 M8
"""


file = open("SeqAlignProfileHMM_sample.txt", "r")
file = open("SeqAlignProfileHMM_test.txt", "r")
file = open("dataset_397441_14.txt", "r")
data = file.readlines()
string = data[0].strip('\n')
threshold = float(data[2].strip('\n').split(' ')[0]) 
pseudocount = float(data[2].strip('\n').split(' ')[1]) 

alphabet = data[4].strip('\n').split(' ')

Alignment = []
for d in data[6:]: 
	Alignment.append(d.strip('\n'))
# print(Alignment)

def identify_removed_columns(threshold, Alignment): 
	
	removed_columns = []
	for column in range(len(Alignment[0])): 
		count = 0 
		for sequence in Alignment: 
			if sequence[column] == '-': 
				count += 1 
		if count / len(Alignment) >= threshold: 
			removed_columns.append(column)

	return removed_columns

def construct_transition_matrix_with_pseudocounts(States, Alignment, removed_columns, pseudocount): 

	total_count = np.zeros((len(States), len(States)))
	transition = copy(total_count)
	Paths = []
	for sequence in Alignment: 

		count = np.zeros((len(States), len(States)))
		path = []; State_idx = 0 
		for idx, letter in enumerate(sequence): 
			if idx == 0: 
				path.append(States[State_idx])
			if idx in removed_columns: 
				if letter in alphabet: 
					if State_idx == 0: 
						path.append(States[State_idx+1])
					else: 
						if States[State_idx][0] == "M": 
							path.append(States[State_idx+2])
						elif States[State_idx][0] == "D": 
							path.append(States[State_idx+1])							
						else: 
							path.append(States[State_idx])

			else: 
				if State_idx == 0: 
					State_idx += 2
				else:
					if States[State_idx][0] == "I": 
						State_idx += 1 
					elif States[State_idx][0] == "D": 
						State_idx += 2
					else: #States[State_idx][0] == "M": 
						State_idx += 3 
				if letter == "-": 
					path.append(States[State_idx+1])
				else: 
					path.append(States[State_idx])

		path.append(States[-1])
		Paths.append(path)
		for i in range(len(path)-1): 
			count[States.index(path[i])][States.index(path[i+1])] += 1 
		# print(count)
		total_count += count 
		# print(path)
	# print(total_count)
	for idx, state_trans_counts in enumerate(total_count):
		if np.sum(state_trans_counts) != 0: 
			transition[idx] = np.round(state_trans_counts / np.sum(state_trans_counts),3) 
	# print(transition)

	# Add pseudocounts
	row_start_idx = [0, 2]
	while row_start_idx[-1] + 3 != len(States)-1: 
		row_start_idx.append(row_start_idx[-1]+3)
	col_start_idx = [1]
	while col_start_idx[-1] + 3 != len(States)+1: 
		col_start_idx.append(col_start_idx[-1]+3)
	# print(row_start_idx, col_start_idx)
	for rowidxs, colidxs in zip(row_start_idx, col_start_idx): 
		if rowidxs == 0: 
			numrows = 2
		else: 
			numrows = 3
		if colidxs == len(States) - 2: 
			numcols = 2 
		else: 
			numcols = 3 
		for i in range(rowidxs, rowidxs + numrows): 
			for j in range(colidxs, colidxs + numcols): 
				transition[i][j] += pseudocount

	#normalize transition matrix  
	for idx, trans in enumerate(copy(transition)):
		if np.sum(trans) != 0: 
			transition[idx] = np.round(trans / np.sum(trans),3)
 


	return 	transition, Paths

def construct_emission_matrix_with_pseudocounts(States, alphabet, Alignment, Paths, removed_columns, pseudocount): 

	emission = np.zeros((len(States), len(alphabet)))
	count = copy(emission)
	for idx1, sequence in enumerate(Alignment): 
		idx_str = 0 
		for idx2, letter in enumerate(sequence): 
			if letter in alphabet: 
				count[States.index(Paths[idx1][1:-1][idx2-idx_str])][alphabet.index(letter)] \
				+= 1 
			elif letter == '-' and idx2 in removed_columns: 
				idx_str += 1 
			else: 
				pass
	for idx, state_emiss_counts in enumerate(count):
		if np.sum(state_emiss_counts) != 0: 
			emission[idx] = np.round(state_emiss_counts / np.sum(state_emiss_counts), 3)


	for i in range(len(States)): 
		for j in range(len(alphabet)): 
			if States[i][0] in ["I", "M"]: 
				emission[i][j] += pseudocount

	#normalize emission matrix  
	for idx, emiss in enumerate(copy(emission)):
		if np.sum(emiss) != 0: 
			emission[idx] = np.round(emiss / np.sum(emiss),3)

	return emission

def score_ProfileHMM_ViterbiGraph(States, transition, emission, string, alphabet): 

	s = np.zeros((len(States), len(string) + 1 + 1))
	backtrack = np.zeros((len(States), len(string) + 1 + 1, 2)) #holds indicies of node to backtrack to 
	s[0,0] = 1 
	for j in range(s.shape[1]): #emissions 
		if j > 0 and j < len(string) + 1: 
			letter_idx = alphabet.index(string[j-1])
		for i in range(s.shape[0]): #states 
			state = States[i]
			if state == 'S': 
				continue
			if j == 0 and state[0] != 'D': 
				continue 
			if j == s.shape[1] - 1 and state != "E":
				continue 
			if j != s.shape[1] - 1 and state == "E":
				continue

			if j == 0: # First column of D's 
				s[i][j] = s[i-3][j]*transition[i-3][i]
				backtrack[i][j] = [i-3, j]
				continue 

			if j == 1: 
				if state[0] == "I": 
					s[i][j] = s[i-1][j-1] * transition[i-1][i]*emission[i][letter_idx]
					backtrack[i][j] = [i-1, j-1]
				elif state[0] == "M": 
					s[i][j] = s[i-2][j-1] * transition[i-2][i]*emission[i][letter_idx]
					backtrack[i][j] = [i-2, j-1]
				else: # Deletion States 
					if state == "D1": 
						s[i][j] = s[i-2][j]*transition[i-2][i]
						backtrack[i][j] = [i-2, j]
					else:
						scores = [s[i-4][j]*transition[i-4][i], s[i-3][j]*transition[i-3][i], \
						s[i-2][j]*transition[i-2][i]]
						s[i][j] = max(scores)
						backtrack[i][j] = [i-(4 - scores.index(max(scores))), j] 
			else:  
				if state[0] == "I": 
					if state == "I0": 
						s[i][j] = s[i][j-1] * transition[i][i]*emission[i][letter_idx]
						backtrack[i][j] = [i, j-1]
					else: 
						scores = [s[i-2][j-1] * transition[i-2][i]*emission[i][letter_idx], s[i-1][j-1] * transition[i-1][i]*emission[i][letter_idx], \
						s[i][j-1] * transition[i][i]*emission[i][letter_idx]]
						s[i][j] = max(scores)
						backtrack[i][j] = [i-(2 - scores.index(max(scores))), j-1]
				elif state[0] == "M": 
					if state == "M1": 
						s[i][j] = s[i-1][j-1] * transition[i-1][i]*emission[i][letter_idx]
						backtrack[i][j] = [i-1, j-1]
					else: 
						scores = [s[i-3][j-1] * transition[i-3][i]*emission[i][letter_idx], s[i-2][j-1] * transition[i-2][i]*emission[i][letter_idx], \
						s[i-1][j-1] * transition[i-1][i]*emission[i][letter_idx]]
						s[i][j] = max(scores)
						backtrack[i][j] = [i-(3 - scores.index(max(scores))), j-1]
				elif state == "E": 
						scores = [s[i-3][j-1], s[i-2][j-1], \
						s[i-1][j-1]]
						s[i][j] = max(scores)
						backtrack[i][j] = [i-(3 - scores.index(max(scores))), j-1]
				else: # Deletion States 
					if state == "D1": 
						s[i][j] = s[i-2][j]*transition[i-2][i]
						backtrack[i][j] = [i-2, j]
					else:
						scores = [s[i-4][j]*transition[i-4][i], s[i-3][j]*transition[i-3][i], \
						s[i-2][j] * transition[i-2][i]]
						s[i][j] = max(scores)
						backtrack[i][j] = [i-(4 - scores.index(max(scores))), j]				
	return s, backtrack

def backtrack_profileHMM_Viterbi(backtrack, States, state, column): 
	# print(state, column, States[state])
	if States[state] != "S": 
		backtrack_profileHMM_Viterbi(backtrack, States, int(backtrack[state][column][0]), int(backtrack[state][column][1]))
		if States[state] != "E": 
			print(States[state], end=' ')
	else: 
		return 


removed_columns = identify_removed_columns(threshold, Alignment)
# print(removed_columns)
# Create states list 
States = ['S', 'I0']
for num in range(1, len(Alignment[0]) - len(removed_columns) + 1): 
	States.append('M' + str(num))
	States.append('D' + str(num))
	States.append('I' + str(num))
States.append('E')
# print(States)
transition, Paths = construct_transition_matrix_with_pseudocounts(States, Alignment, removed_columns, pseudocount)
# print(transition)
# print(Paths)
# print(States, alphabet)
emission = construct_emission_matrix_with_pseudocounts(States, alphabet, Alignment, Paths, removed_columns, pseudocount)
# print(emission)
# Output results 
s, backtrack = score_ProfileHMM_ViterbiGraph(States, transition, emission, string, alphabet)
# print(string)
backtrack_profileHMM_Viterbi(backtrack, States, len(States)-1, s.shape[1]-1)
# print(s[-1][-1])
# print(States)
# print(np.round(s.T, 3))
# Path = ["S", "M1", "D2", "D3", "M4", "M5", "I5", "M6", "M7", "M8", "E"]

# score = 0
# old_state = "S"
# j = -1
# for state in Path[1:-1]: 
# 	if state[0] != "D": 
# 		j += 1
# 	state_idx = Path.index(state)
# 	prev_state_idx = Path.index(old_state)
# 	score += transition[prev_state_idx][state_idx] * emission[state_idx][alphabet.index(string[j])]
# 	old_state = copy(state)
	 
# print(score)