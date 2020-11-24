import numpy as np 
from copy import copy 
"""
Profile HMM with Pseudocounts Problem: Construct a profile HMM with pseudocounts from a multiple alignment.

Input: A multiple alignment Alignment, a threshold value θ, and a pseudocount value σ.
Output: HMM(Alignment, θ), in the form of transition and emission matrices.
Code Challenge: Solve the Profile HMM with Pseudocounts Problem.

Input: A threshold θ and a pseudocount σ, followed by an alphabet Σ, followed by a multiple alignment Alignment whose strings are formed from Σ.
Output: The transition and emission matrices of HMM(Alignment, θ, σ).

Note: Your matrices can be either space-separated or tab-separated.

Sample Input:

0.289
--------
A B C D E
--------
EBA
E-D
EB-
EED
EBD
EBE
E-D
E-D

Sample Input:

0.358 0.01
--------
A B C D E
--------
A-A
ADA
ACA
A-C
-EA
D-A

Sample Output:

	S	I0	M1	D1	I1	M2	D2	I2	E
S	0	0.01	0.819	0.172	0	0	0	0	0
I0	0	0.333	0.333	0.333	0	0	0	0	0
M1	0	0	0	0	0.398	0.592	0.01	0	0
D1	0	0	0	0	0.981	0.01	0.01	0	0
I1	0	0	0	0	0.01	0.981	0.01	0	0
M2	0	0	0	0	0	0	0	0.01	0.99
D2	0	0	0	0	0	0	0	0.5	0.5
I2	0	0	0	0	0	0	0	0.5	0.5
E	0	0	0	0	0	0	0	0	0
--------
	A	B	C	D	E
S	0	0	0	0	0
I0	0.2	0.2	0.2	0.2	0.2
M1	0.771	0.01	0.01	0.2	0.01
D1	0	0	0	0	0
I1	0.01	0.01	0.327	0.327	0.327
M2	0.803	0.01	0.168	0.01	0.01
D2	0	0	0	0	0
I2	0.2	0.2	0.2	0.2	0.2
E	0	0	0	0	0
"""

file = open("dataset_397441_5.txt", "r")
# file = open("ProfileHMMwithPseudocounts_sample.txt", "r")
# file = open("ProfileHMM_test.txt", "r")
data = file.readlines()

threshold = float(data[0].strip('\n').split(' ')[0]) 
pseudocount = float(data[0].strip('\n').split(' ')[1]) 

alphabet = data[2].strip('\n').split(' ')

Alignment = []
for d in data[4:]: 
	Alignment.append(d.strip('\n'))
print(Alignment)

def identify_removed_columns(threshold, Alignment): 
	
	removed_columns = []
	for column in range(len(Alignment[0])): 
		count = 0 
		for sequence in Alignment: 
			if sequence[column] == '-': 
				count += 1 
		if count / len(Alignment) > threshold: 
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


removed_columns = identify_removed_columns(threshold, Alignment)
# print(removed_columns)
#Create states list 
States = ['S', 'I0']

for num in range(1, len(Alignment[0]) - len(removed_columns) + 1): 
	States.append('M' + str(num))
	States.append('D' + str(num))
	States.append('I' + str(num))
States.append('E')
# print(States)
transition, Paths = construct_transition_matrix_with_pseudocounts(States, Alignment, removed_columns, pseudocount)
print(Paths)
print(States, alphabet)
emission = construct_emission_matrix_with_pseudocounts(States, alphabet, Alignment, Paths, removed_columns, pseudocount)
# print(emission)
# Output results 
st=[' '+i for i in States]
for idx, s in enumerate(st): 
	if idx != len(st) - 1: 
		print(s, end=' ')
	else: 
		print(s)

for idx, state in enumerate(States): 
	print(state, end=' ')
	for idx2, value in enumerate(transition[idx]): 
		if idx2 != len(transition[idx])-1:
			print(value, end=' ')
		else: 
			print(value)
print('--------')

at=[' '+i for i in alphabet	]
for idx, a in enumerate(at): 
	if idx != len(at) - 1: 
		print(a, end=' ')
	else: 
		print(a)

for idx, state in enumerate(States): 
	print(state, end=' ')
	for idx2, value in enumerate(emission[idx]): 
		if idx2 != len(emission[idx])-1:
			print(value, end=' ')
		else: 
			print(value)