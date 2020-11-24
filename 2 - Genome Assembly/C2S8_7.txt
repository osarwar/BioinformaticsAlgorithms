import numpy as np 
from copy import copy 
"""
Name: OWAIS SARWAR

You now have a method to assemble a genome, since the String Reconstruction Problem reduces to finding an Eulerian path in the de Bruijn graph generated from reads.

We can therefore summarize this solution using the following pseudocode, which relies on three problems that we have already solved:

The de Bruijn Graph Construction Problem;
The Eulerian Path Problem;
The String Spelled by a Genome Path Problem.

Code Challenge: Solve the String Reconstruction Problem.

Input: An integer k followed by a list of k-mers Patterns.
Output: A string Text with k-mer composition equal to Patterns. (If multiple answers exist, you may return any one.)

Sample Input:

4
CTTA
ACCA
TACC
GGCT
GCTT
TTAC

Sample Output:

GGCTTACCA

"""

def PathToGenome(uniquePrefixesAndSuffixes, path): 


	Text = ""

	for idx, node in enumerate(path): 

		if idx == 0: 
			Text += uniquePrefixesAndSuffixes[node]
		else: 
			Text += uniquePrefixesAndSuffixes[node][-1]

	return Text

def EulerianPath(AdjacencyMatrix): 

	#Starting Node & Ending Node 
	for idx, node in enumerate(AdjacencyMatrix):
		in_degree = np.sum(AdjacencyMatrix.T[idx])
		out_degree = np.sum(node)
		if in_degree > out_degree: # Ending node 
			EndingNode = copy(idx) 
		elif out_degree > in_degree: 
			StartingNode = copy(idx)
		else: 
			pass 

	# print(StartingNode, EndingNode)

	AdjacencyMatrix_EulerianCycle = copy(AdjacencyMatrix)
	AdjacencyMatrix_EulerianCycle[EndingNode, StartingNode] = 1 #Add Edge to ensure Eulerian Path 


	#Generate Random Cycle 
	Cycle = []
	Nodes_with_unexplored_edges_in_Cycle = []
	StartNode = np.random.choice(np.arange(AdjacencyMatrix_EulerianCycle.shape[0])) #Starting Node 
	NewNode = np.random.choice(np.argwhere(AdjacencyMatrix_EulerianCycle[StartNode] > 0)[0])#Next Node 
	Cycle.append(NewNode) #Add Node to Cycle 
	AdjacencyMatrix_EulerianCycle[StartNode][NewNode] -= 1 #Remove Edge 
	if np.count_nonzero(AdjacencyMatrix_EulerianCycle[StartNode]) > 0: 
		Nodes_with_unexplored_edges_in_Cycle.append(StartNode)
	while NewNode != StartNode: 
		OldNode = copy(NewNode)
		NewNode = np.random.choice(np.argwhere(AdjacencyMatrix_EulerianCycle[OldNode] > 0)[0]) #Next Node 
		Cycle.append(NewNode) #Add Node to Cycle 
		AdjacencyMatrix_EulerianCycle[OldNode][NewNode] -= 1 #Remove Edge
		if np.count_nonzero(AdjacencyMatrix_EulerianCycle[OldNode]) > 0: 
			Nodes_with_unexplored_edges_in_Cycle.append(OldNode)

	#Using Intial Cycle, Generate new Cycles until all edges explored 

	while np.count_nonzero(AdjacencyMatrix_EulerianCycle) != 0: 
		StartNode = np.random.choice(Nodes_with_unexplored_edges_in_Cycle)[0] #Select Start Node from List of Nodes with unexplored edges from cycle
		Cycle = Cycle[StartNode:] + Cycle[:StartNode]
		NewNode = np.random.choice(np.argwhere(AdjacencyMatrix_EulerianCycle[StartNode] > 0)[0]) #Next Node 
		Cycle.append(NewNode) #Add Node to Cycle 
		AdjacencyMatrix_EulerianCycle[StartNode][NewNode] -= 1 #Remove Edge 
		if np.count_nonzero(AdjacencyMatrix_EulerianCycle[StartNode]) > 0: 
			Nodes_with_unexplored_edges_in_Cycle.append(StartNode)
		else: 
			Nodes_with_unexplored_edges_in_Cycle.remove(StatNode)
		while NewNode != StartNode: 
			OldNode = copy(NewNode)
			NewNode = np.random.choice(np.argwhere(AdjacencyMatrix_EulerianCycle[OldNode] > 0)[0]) #Next Node 
			Cycle.append(NewNode) #Add Node to Cycle 
			AdjacencyMatrix_EulerianCycle[OldNode][NewNode] -= 1 #Remove Edge
			if np.count_nonzero(AdjacencyMatrix_EulerianCycle[OldNode]) > 0: 
				Nodes_with_unexplored_edges_in_Cycle.append(OldNode)


	#Remove added edge to get Eulerian Path 
	# print(Cycle)
	idx_of_StartingNode_in_Cycle = Cycle.index(StartingNode)
	# print(idx_of_StartingNode_in_Cycle)
	path = Cycle[idx_of_StartingNode_in_Cycle:] + Cycle[:idx_of_StartingNode_in_Cycle]
	# print(path)
		
	return path 

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

f = open("dataset_397295_7.txt", "r")
data = f.readlines()

#k for length of kmer
k = int(data[0].strip('\n'))

#Patters/k-mers  
Patterns = data[1:]

for idx, kmer in enumerate(Patterns): 
	Patterns[idx] = kmer.strip('\n')

# Patterns = ["CTTA",
# "ACCA",
# "TACC",
# "GGCT",
# "GCTT",
# "TTAC"]

uniquePrefixesAndSuffixes, AdjacencyMatrix = deBruijn(Patterns)

path = EulerianPath(AdjacencyMatrix)

print(PathToGenome(uniquePrefixesAndSuffixes, path))