import numpy as np 
import copy as cp 
"""
Code Challenge: Solve the 2-Break Distance Problem.

Input: Genomes P and Q.
Output: The 2-break distance d(P, Q).

Sample Input:

(+1 +2 +3 +4 +5 +6)
(+1 -3 -6 -5)(+2 -4)

Sample Output:

3

"""

def ChromosomeToCycle(Chromosome): 
	"""
	Code Challenge: Implement ChromosomeToCycle.
	Input: A chromosome Chromosome containing n synteny blocks.
	Output: The sequence Nodes of integers between 1 and 2n resulting from applying ChromosomeToCycle to Chromosome.

	Sample Input:

	(+1 -2 -3 +4)

	Sample Output:

	(1 2 4 3 6 5 7 8)
	"""
	Nodes = [0 for i in range(2*len(Chromosome))]
	for j in range(1, len(Chromosome) + 1): 
		i = Chromosome[j-1]
		if i > 0: 
			Nodes[2*j-1 -1] = 2*i - 1 
			Nodes[2*j -1] = 2*i 
		else: 
			Nodes[2*j-1 -1] = -2*i 
			Nodes[2*j -1] = -2*i - 1
	return Nodes


def CycleToChromosome(Nodes): 
	"""
	Code Challenge: Implement CycleToChromosome.

	Input: A sequence Nodes of integers between 1 and 2n.
	Output: The chromosome Chromosome containing n synteny blocks resulting from applying CycleToChromosome to Nodes.

	Sample Input:

	(1 2 4 3 6 5 7 8)

	Sample Output:

	(+1 -2 -3 +4)
	"""
	Chromosome = [0 for i in range(int(len(Nodes) / 2))]
	for j in range(1, int(len(Nodes) / 2 + 1)): 
		if Nodes[2*j-1 -1] < Nodes[2*j -1]: 
			Chromosome[j-1] = int(Nodes[2*j -1] / 2)
		else: 
			Chromosome[j-1] = int(-Nodes[2*j-1 -1] / 2)
	return Chromosome


def ColoredEdges(P):
	"""
	Code Challenge: Implement ColoredEdges.
	Input: A genome P.
	Output: The collection of colored edges in the genome graph of P in the form (x, y).


	Sample Input:

	(+1 -2 -3)(+4 +5 -6)

	Sample Output:

	(2, 4), (3, 6), (5, 1), (8, 9), (10, 12), (11, 7)
	""" 
	Edges = []
	for Chromosome in P: 
		Nodes = ChromosomeToCycle(Chromosome)
		Nodes.append(Nodes[0])
		for j in range(1, len(Chromosome) + 1): 
			Edges.append([Nodes[2*j -1], Nodes[2*j+1 -1]])
	return Edges

def CyclesInGenomeGraph(GenomeGraph): 

	def index_2d(myList, v):
		for i, x in enumerate(myList):
			if v in x:
				return (i, x.index(v))
	Cycles = []
	start_node = np.min(GenomeGraph) 
	while len(GenomeGraph) != 0:
		cycle = []
		node = start_node
		cycle.append(node)
		while True:
			if node == start_node: 
				node = node + 1 
				cycle.append(node)
				node_index = index_2d(GenomeGraph, node)
				edge_index = node_index[0]
				if node_index[1]==1: 
					node = GenomeGraph[edge_index][0]
				else: 
					node = GenomeGraph[edge_index][1]
				GenomeGraph.pop(edge_index)
				cycle.append(node)
			else: 
				if node%2 == 0: 
					node = node - 1 
					cycle.append(node)
					node_index = index_2d(GenomeGraph, node)
					edge_index = node_index[0]
					if node_index[1]==1: 
						node = GenomeGraph[edge_index][0]
					else: 
						node = GenomeGraph[edge_index][1]
					GenomeGraph.pop(edge_index)
					cycle.append(node)
				else: 
					node = node + 1
					cycle.append(node)
					node_index = index_2d(GenomeGraph, node)
					edge_index = node_index[0]
					if node_index[1]==1: 
						node = GenomeGraph[edge_index][0]
					else: 
						node = GenomeGraph[edge_index][1]
					GenomeGraph.pop(edge_index)
					cycle.append(node) 
			
			if node == start_node: 
				cycle.pop(-1)
				Cycles.append(cycle)
				if len(GenomeGraph) > 0: 
					start_node = np.min(GenomeGraph)  
				break 

	return Cycles 

def GraphToGenome(GenomeGraph): 
	"""
	Code Challenge: Implement GraphToGenome.

	Input: The colored edges ColoredEdges of a genome graph.
	Output: The genome P corresponding to this genome graph.

	Sample Input:

	(2, 4), (3, 6), (5, 1), (7, 9), (10, 12), (11, 8)

	Sample Output:

	(+1 -2 -3)(-4 +5 -6)
	"""
	P = []
	Cycles = CyclesInGenomeGraph(GenomeGraph)
	# print("CYCLes:", Cycles)
	for Nodes in Cycles: 
		Chromosome = CycleToChromosome(Nodes)
		P.append(Chromosome)
	return P 


def Cycles(P, Q): 

	def index_2d(myList, v):
		for i, x in enumerate(myList):
			if v in x:
				return (i, x.index(v))

	Edges_P = ColoredEdges(P)
	Edges_Q = ColoredEdges(Q)
	# print(Edges_P, Edges_Q)
	Cycles = []

	while len(Edges_P) != 0 and len(Edges_Q) != 0: 
		cycle = []
		first_edge_in_cycle = Edges_P[0]
		first_node = first_edge_in_cycle[0]
		first_edge_in_cycle = Edges_P[0]
		first_node = np.min(Edges_P)
		P_or_Q = 0 
		node = first_node
		cycle.append(node)
		while True: 
			if P_or_Q == 0: 
				node_index = index_2d(Edges_P, node) 
				edge = Edges_P[node_index[0]]
				if node_index[1] == 1: 
					node = edge[0]
					cycle.append(node)
				else: 
					node = edge[1]
					cycle.append(node)
				P_or_Q = 1 
				Edges_P.pop(node_index[0])
			else:
				node_index = index_2d(Edges_Q, node) 
				edge = Edges_Q[node_index[0]]
				if node_index[1] == 1: 
					node = edge[0]
					cycle.append(node)
				else: 
					node = edge[1]
					cycle.append(node)
				P_or_Q = 0 
				Edges_Q.pop(node_index[0])

			
			if P_or_Q == 0: 
				node_index = index_2d(Edges_P, node) 
				edge = Edges_P[node_index[0]]
				if node_index[1] == 1: 
					node = edge[0]
					cycle.append(node)
				else: 
					node = edge[1]
					cycle.append(node)
				P_or_Q = 1
				Edges_P.pop(node_index[0])

			else:
				node_index = index_2d(Edges_Q, node) 
				edge = Edges_Q[node_index[0]]
				if node_index[1] == 1: 
					node = edge[0]
					cycle.append(node)
				else: 
					node = edge[1]
					cycle.append(node)
				P_or_Q = 0
				Edges_Q.pop(node_index[0])
			

			if node == first_node: 
				cycle.pop(-1)
				Cycles.append(cycle)
				break 

	return Cycles 

def TwoBreakOnGenomeGraph(GenomeGraph, i1, i2, i3, i4): 
	#remove colored edges (i1, i2) and (i3, i4) from GenomeGraph
	if [i1, i2] in GenomeGraph: 
		GenomeGraph.pop(GenomeGraph.index([i1, i2])) 
	else: 
		GenomeGraph.pop(GenomeGraph.index([i2, i1])) 
	if [i3, i4] in GenomeGraph: 
		GenomeGraph.pop(GenomeGraph.index([i3, i4])) 
	else: 
		GenomeGraph.pop(GenomeGraph.index([i4, i3])) 
	#add colored edges (i1, i3) and (i2, i4) to GenomeGraph
	GenomeGraph.append([i1, i3]) 
	GenomeGraph.append([i2, i4])
	return GenomeGraph

def TwoBreakOnGenome(P, i1, i2, i3, i4): 
	GenomeGraph = ColoredEdges(P)
	GenomeGraph = TwoBreakOnGenomeGraph(GenomeGraph, i1, i2, i3, i4)
	# print("genome graph after break", GenomeGraph)
	P = GraphToGenome(GenomeGraph)
	return P 

def TwoBreakDistance(P, Q): 

	Blocks_PQ = sum(len(i) for i in P)

	cycles = Cycles(P, Q)

	Cycles_PQ = len(cycles)

	TwoBreakDist = Blocks_PQ - Cycles_PQ

	return TwoBreakDist 

def TwoBreakSorting(P, Q): 
	def OutputP(P): 
		for idx, C in enumerate(P): 
			print("(", end='')
			for idx2, c in enumerate(C): 
				if c > 0: 
					print("+", c, sep='', end='')
				else: 
					print(c, end='')
				if idx2 == len(C)-1: 
					if idx != len(P) - 1: 
						print(")", end="")
					else: 
						print(")")

	OutputP(P)
	while TwoBreakDistance(P, Q) > 0: 
		cycles = Cycles(P, Q) 
		for cycle in cycles: 
			if len(cycle) > 3:  
				i1 = cycle[1]; i2 = cycle[0]; i3 = cycle[2]; i4 = cycle[3]
				P = TwoBreakOnGenome(P, i1, i2, i3, i4)
				OutputP(P)
				break 
			else: 
				pass


file = open(r"2BreakSort_sample.txt", "r")
file = open(r"dataset_397361_5.txt", "r")
# file = open(r"2BreakSorting_test.txt", "r"))
data = file.readlines()
for idx, line in enumerate(data): 
	line = line.strip('\n').strip(')')[1:].split(")(")
	if idx == 0: 
		P = []
		for chromosome in line: 
			chromosome = chromosome.split()
			for idx, elem in enumerate(chromosome): 
				chromosome[idx] = int(elem)
			P.append(chromosome)
	elif idx == 1: 
		Q = []
		for chromosome in line: 
			chromosome = chromosome.split()
			for idx, elem in enumerate(chromosome): 
				chromosome[idx] = int(elem)
			Q.append(chromosome)
	else: 
		pass 
# print(ChromosomeToCycle([1, -2, -3, 4]))
# print(CycleToChromosome([1,2,4,3,6,5,7,8]))
# # print(Cycles(P, Q))
# # print(GraphToGenome([[2,4], [3,6], [5,1], [7,9], [10,12],[11,8]]))
# print("two break genome graph")
# print(TwoBreakOnGenomeGraph(ColoredEdges([[1, -2, -4, 3]]), 1, 6, 3, 8))
# print("two break genome")
# print(TwoBreakOnGenome([[1, -2, -4, 3]], 1, 6, 3, 8))
# print("two break sorting")
TwoBreakSorting(P, Q)
