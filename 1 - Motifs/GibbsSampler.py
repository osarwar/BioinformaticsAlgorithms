"""
Code Challenge: Implement GibbsSampler.

Input: Integers k, t, and N, followed by a collection of strings Dna.
Output: The strings BestMotifs resulting from running GibbsSampler(Dna, k, t, N) with 20 random starts. Remember to use pseudocounts!

Sample Input:

8 5 100
CGCCCCTCTCGGGGGTGTTCAGTAACCGGCCA
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

def MotifGenerator(Profile, dna): 

	k = len(Profile[0])
	number_kmers = len(dna) - k + 1 
	kmer_prob = np.zeros(number_kmers)

	#Generate Profile-randomly generated k-mer
	for kmer_start in range(number_kmers): 
		prob = 1 
		for kmer_position in range(k): 
			Base = dna[kmer_start + kmer_position]
			if Base == "A": 
				prob *= Profile[0][kmer_position]
			elif Base == "C": 
				prob *= Profile[1][kmer_position]
			elif Base == "G": 
				prob *= Profile[2][kmer_position]
			else:
				prob *= Profile[3][kmer_position] 
		kmer_prob[kmer_start] = prob 

	kmer_prob = kmer_prob / np.sum(kmer_prob)
	random_kmer_number = np.random.choice(number_kmers, p=kmer_prob)
	motif = copy(dna[random_kmer_number:random_kmer_number+k])

	return motif 

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

f = open("dataset_397052_11.txt", "r")
data = f.readlines()

#DNA 
DNA = data[1:]

for idx, dna in enumerate(DNA): 
	DNA[idx] = dna.strip('\n')


# # Testing 

# DNA = ["CGCCCCTCTCGGGGGTGTTCAGTAACCGGCCA", \
# "GGGCGAGGTATGTGTAAGTGCCAAGGTGCCAG", \
# "TAGTACCGAGACCGAAAGAAGTATACAGGCGT", \
# "TAGATCAAGTTTCAGGTGCACGTCGGTGAACC", \
# "AATCCACCAGCTCCACGTGCAATGTTGGCCTA"]

t = len(DNA)
k = 15
N = 2000

#Number of kmers in DNA 
number_kmers = len(DNA[0]) - k + 1 

#Number of runs 
num_runs = 20

#RandomizedMotifSearch
best_score_all = 1e5 
BestMotifs_all = ["" for i in range(t)]

for run in range(num_runs): 
	improvement = True 
	Motifs = []
	# Generate random motifs 
	for string in DNA: 
		kmer_number = np.random.choice(number_kmers, 1)[0]
		Motifs.append(string[kmer_number:kmer_number+k])
	BestMotifs = copy(Motifs)
	best_score = Score(BestMotifs)
	for j in range(N): 
		rand_motif_num = np.random.choice(t) 
		Profile = ProfileGenerator(np.delete(np.array(Motifs), rand_motif_num))
		# print(Motifs)
		random_motif = MotifGenerator(Profile, DNA[rand_motif_num])
		Motifs[rand_motif_num] = random_motif
		# print(Motifs)
		if Score(Motifs) < best_score: 
			best_score = copy(Score(Motifs))
			BestMotifs = copy(Motifs)
			# print(best_score, BestMotifs)

	if best_score < best_score_all: 
		best_score_all = copy(best_score)
		BestMotifs_all = copy(BestMotifs)

for motif in BestMotifs_all: 
	print(motif)
# print(best_score_all)

# TM = ["TCTCGGGG", \
# "CCAAGGTG", \
# "TACAGGCG", \
# "TTCAGGTG", \
# "TCCACGTG",\
# ]

# print(Score(TM))