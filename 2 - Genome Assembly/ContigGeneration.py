import numpy as np 
from copy import copy 

"""
Name: OWAIS SARWAR

Contig Generation Problem: Generate the contigs from a collection of reads (with imperfect coverage).

Input: A collection of k-mers Patterns.
Output: All contigs in DeBruijn(Patterns).

Code Challenge: Solve the Contig Generation Problem.

Sample Input:

ATG
ATG
TGT
TGG
CAT
GGA
GAT
AGA

Sample Output:

AGA ATG ATG CAT GAT TGGA TGT

"""

def deBruijn(Patterns): 

	Prefixes, Suffixes = [], []
	for idx, pattern in enumerate(Patterns): 
		Prefixes.append(pattern[0:-1])
		Suffixes.append(pattern[1:])

	PrefixesAndSuffixes = Prefixes + Suffixes

	uniquePrefixesAndSuffixes = np.unique(PrefixesAndSuffixes)

	num_nodes = len(uniquePrefixesAndSuffixes)

	AdjacencyMatrix = np.zeros((num_nodes, num_nodes))

	for idx1, pref in enumerate(uniquePrefixesAndSuffixes): 
		for idx2, suff in enumerate(uniquePrefixesAndSuffixes): 

			if pref[1:] == suff[:-1]: 
				count_kmer = Patterns.count(pref + suff[-1])
				if count_kmer > 0: 
					AdjacencyMatrix[idx1][idx2] = count_kmer

	# print(uniquePrefixesAndSuffixes)
	return uniquePrefixesAndSuffixes, AdjacencyMatrix

def MaximalNonBranchingPaths(AdjacencyMatrix, uniquePrefixesAndSuffixes): 

	Paths = []

	for node in np.arange(len(uniquePrefixesAndSuffixes)): 
		# print("node:", node)

		if np.sum(AdjacencyMatrix[node]) != 1 or np.sum(AdjacencyMatrix.T[node]) != 1: 

			for connected_node in np.nonzero(AdjacencyMatrix[node])[0]: 
				# print("CN:", connected_node)
				for i in range(int(AdjacencyMatrix[node][connected_node])): 
					NonBranchingPath = [node]
					if connected_node == node:
						Paths.append([node, connected_node])
					else: 
						# print(connected_node)
						NonBranchingPath.append(connected_node)
					while np.sum(AdjacencyMatrix[connected_node]) == 1 and np.sum(AdjacencyMatrix.T[connected_node]) == 1: 
						connected_node = np.argwhere(AdjacencyMatrix[connected_node]==1)[0][0]
						NonBranchingPath.append(connected_node)
					Paths.append(NonBranchingPath)
					# print(Paths)

	return Paths

def PathToGenome(uniquePrefixesAndSuffixes, path): 


	Text = ""

	for idx, node in enumerate(path): 

		if idx == 0: 
			Text += uniquePrefixesAndSuffixes[node]
		else: 
			Text += uniquePrefixesAndSuffixes[node][-1]

	return Text

f = open("dataset_397297_5.txt", "r")
data = f.readlines()

#Patters/k-mers  
Patterns = data

for idx, kmer in enumerate(Patterns): 
	Patterns[idx] = kmer.strip('\n')

# Patterns = ["ATG", 
# "ATG", 
# "TGT", 
# "TGG", 
# "CAT", 
# "GGA", 
# "GAT", 
# "AGA"]

# Patterns = ["AG",
# "GT",
# "GC",
# "TA"]

# Patterns = ["GTT",
# "TTA",
# "TAC",
# "TTT"]

uniquePrefixesAndSuffixes, AdjacencyMatrix = deBruijn(Patterns)

# print(AdjacencyMatrix)
# print(uniquePrefixesAndSuffixes)

Paths = MaximalNonBranchingPaths(AdjacencyMatrix, uniquePrefixesAndSuffixes)

# print(Paths)

results = open("results.txt", "a")
for path in Paths: 
	Text = PathToGenome(uniquePrefixesAndSuffixes, path)
	print(Text, end=" ", file=results)
	# print(Text, end=" ")
results.close()