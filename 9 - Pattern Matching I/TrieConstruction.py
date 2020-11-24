import numpy as np 
from copy import copy 
"""
Name = Owais Sarwar

Code Challenge: Solve the Trie Construction Problem.

Input: A collection of strings Patterns.
Output: The adjacency list corresponding to Trie(Patterns), in the following format. If Trie(Patterns) has n nodes, first label the root with 0 and then label the remaining nodes with the integers 1 through n - 1 in any order you like. 
Each edge of the adjacency list of Trie(Patterns) will be encoded by a triple: the first two members of the triple must be the integers labeling the initial and terminal nodes of the edge, respectively; the third member of the triple must 
be the symbol labeling the edge.

Sample Input:

ATAGA
ATC
GAT

Sample Output:

0->1:A
1->2:T
2->3:A
3->4:G
4->5:A
2->6:C
0->7:G
7->8:A
8->9:T
"""
def TrieConstruction(Patterns): 
	Trie = {}
	newNode = 0 
	for pattern in Patterns: 
		currentNode = 0 
		for i in range(len(pattern)): 
			currentSymbol = pattern[i]
			if currentNode in Trie.keys(): 
				pass 
			else: 
				Trie[currentNode] = []
			if currentSymbol in Trie[currentNode]: 
				currentNode = Trie[currentNode][Trie[currentNode].index(currentSymbol)-1]
			else: 
				newNode += 1 
				Trie[currentNode] += [newNode] 
				Trie[currentNode] += [currentSymbol]
				currentNode = newNode

	return Trie 

file = open(r"TrieConstruction_sample.txt", "r")

# file = open(r"TrieConstruction_test.txt", "r")
file = open(r"dataset_397413_4.txt", "r")


data = file.readlines()

for idx, line in enumerate(data): 
	data[idx] = line.strip("\n")
Patterns = data

Trie = TrieConstruction(Patterns)
print(Trie)
results = open(r"tcresults.txt", "a")
for node in Trie: 
	for idx, end_node in enumerate(Trie[node][::2]): 
		print(node,"->", end_node, ":", Trie[node][2*idx+1],  sep="", file=results)