"""
Code Challenge: Implement RandomizedMotifSearch.

Input: Integers k and t, followed by a collection of strings Dna.
Output: A collection BestMotifs resulting from running RandomizedMotifSearch(Dna, k, t) 1,000 times. Remember to use pseudocounts!

Sample Input:

8 5
CGCCCCTCTCGGGGGTGTTCAGTAAACGGCCA
GGGCGAGGTATGTGTAAGTGCCAAGGTGCCAG
TAGTACCGAGACCGAAAGAAGTATACAGGCGT
TAGATCAAGTTTCAGGTGCACGTCGGTGAACC
AATCCACCAGCTCCACGTGCAATGTTGGCCTA
Sample Output:

TCTCGGGG
CCAAGGTG
TACAGGCG
TTCAGGTG
TCCACGTG
"""
import numpy as np 
import math 
from copy import copy 


def ProfileGenerator(Motifs): 


	k = len(Motifs[0])
	t = len(Motifs)

	#Count matrix 
	Count = np.zeros((4, k))
	for motif in Motifs: 
		for kmer_position in range(k): 
			Base = motif[kmer_position]
			if Base == "A": 
				Count[0,kmer_position] += 1
			elif Base == "C": 
				Count[1,kmer_position] += 1
			elif Base == "G": 
				Count[2,kmer_position] += 1
			else:
				Count[3,kmer_position] += 1 

	#Add pseudocount 
	Count += 1 

	#Profile matrix 

	Profile = np.zeros((4, k))

	Profile = Count / t

	return Profile 

def MotifsGenerator(Profile, DNA): 

	k = len(Profile[0])
	Motifs = []
	number_kmers = len(DNA[0]) - k + 1 

	for string in DNA: 
		#Find most Profile-most probable k-mer
		best_prob = 0 
		best_kmer = ""
		for kmer_start in range(number_kmers): 
			prob = 1 
			for kmer_position in range(k): 
				Base = string[kmer_start + kmer_position]
				if Base == "A": 
					prob *= Profile[0][kmer_position]
				elif Base == "C": 
					prob *= Profile[1][kmer_position]
				elif Base == "G": 
					prob *= Profile[2][kmer_position]
				else:
					prob *= Profile[3][kmer_position] 
			if prob > best_prob: 
				best_prob = copy(prob)
				best_kmer = copy(string[kmer_start:kmer_start+k])
		Motifs.append(best_kmer)

	return Motifs

# def Score(Motifs): 

# 	#Score with entropy 

# 	k = len(Motifs[0])
# 	t = len(Motifs)

# 	Profile = ProfileGenerator(Motifs)

# 	position_score = np.zeros(k)

# 	for idx, motif in enumerate(Motifs): 

# 		for position in range(k): 
# 			Base = motif[position]
# 			if Base == "A": 
# 				position_score[position] += -Profile[0, position] * math.log(Profile[0, position], 2)
# 			elif Base == "C": 
# 				position_score[position] += -Profile[1, position] * math.log(Profile[1, position], 2)
# 			elif Base == "G": 
# 				position_score[position] += -Profile[2, position] * math.log(Profile[2, position], 2)
# 			else:
# 				position_score[position] += -Profile[3, position] * math.log(Profile[3, position], 2) 

# 	return np.sum(position_score)

def Score(Motifs): 

	#Naive score

	t = len(Motifs)

	Profile = ProfileGenerator(Motifs)

	Count = Profile * t - 1 

	score = 0 

	for col in Count.T: 
		score += np.sum(col) - np.max(col)

	return score 

f = open("dataset_397050_9.txt", "r")
data = f.readlines()

#DNA 
DNA = data[1:]

for idx, dna in enumerate(DNA): 
	DNA[idx] = dna.strip('\n')


# # Testing 

# DNA = ["CGCCCCTCTCGGGGGTGTTCAGTAAACGGCCA", \
# "GGGCGAGGTATGTGTAAGTGCCAAGGTGCCAG", \
# "TAGTACCGAGACCGAAAGAAGTATACAGGCGT",\
# "TAGATCAAGTTTCAGGTGCACGTCGGTGAACC",\
# "AATCCACCAGCTCCACGTGCAATGTTGGCCTA"]

t = len(DNA)
k = 15

#Number of kmers in DNA 
number_kmers = len(DNA[0]) - k + 1 

#Number of runs 
num_runs = 1000

#RandomizedMotifSearch
best_score_all = 1e5 
BestMotifs_all = ["" for i in range(t)]

for run in range(num_runs): 
	best_score = 1e5 
	improvement = True 
	Motifs = []
	# Generate random motifs 
	for string in DNA: 
		kmer_number = np.random.choice(number_kmers, 1)[0]
		Motifs.append(string[kmer_number:kmer_number+k])
	# print(Motifs)
	BestMotifs = copy(Motifs)
	while improvement: 
		Profile = ProfileGenerator(Motifs)
		Motifs = MotifsGenerator(Profile, DNA)
		if Score(Motifs) < best_score: 
			best_score = copy(Score(Motifs))
			BestMotifs = copy(Motifs)
			# print(best_score, BestMotifs)
		else: 
			improvement = False 

	# print(best_score, best_score_all)
	if best_score < best_score_all: 
		best_score_all = copy(best_score)
		BestMotifs_all = copy(BestMotifs)

for motif in BestMotifs_all: 
	print(motif)
