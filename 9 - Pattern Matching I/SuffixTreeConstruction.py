import numpy as np 
from copy import copy 
import sys 
sys.setrecursionlimit(10000000)
"""
Name = Owais Sarwar

Code Challenge: Solve the Suffix Tree Construction Problem.

Input: A string Text.
Output: The edge labels of SuffixTree(Text). You may return these strings in any order.

Sample Input:

ATAAATG$

Sample Output:

AAATG$
G$
T
ATG$
TG$
A
A
AAATG$
G$
T
G$
$
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

def SuffixTreeConstruct(Text): 
	SuffixTree = {}

	suffixes = [Text[i:] for i in range(len(Text))]
	SuffixTrie = TrieConstruction(suffixes)

	# print(SuffixTrie)
	def PathInTrie(origin, node, index, edge, SuffixTree, SuffixTrie):
		# print(SuffixTree, node, index, len(SuffixTrie[node]))
		if len(SuffixTrie[node]) > 2: 
			# print(SuffixTrie[node], node, index, "here")
			if edge != "":
				SuffixTree[node]=[edge, origin]
			for idx, child in enumerate(SuffixTrie[node][::2]): 
				edge = ""
				edge+=SuffixTrie[node][2*idx+1]
				if SuffixTrie[node][2*idx+1] != "$": 
					PathInTrie(node, child, 0, edge, SuffixTree, SuffixTrie)
				else: 
					SuffixTree[child]=[edge, node]
					return 
		else: 
			# print(node, edge, index)
			# print(SuffixTrie[node][index+1])
			edge+=SuffixTrie[node][index+1]
			child = SuffixTrie[node][index]
			if SuffixTrie[node][index+1] != "$": 
				PathInTrie(origin, child, 0, edge, SuffixTree, SuffixTrie)
			else: 
				# print(child, edge, origin)
				SuffixTree[child] = [edge, origin] 
				return 

	root = 0 
	edge = ""
	PathInTrie(root, root, 0, edge, SuffixTree, SuffixTrie)

	return SuffixTree

file = open(r"SuffixTreeConstruction_sample.txt", "r")
# file = open(r"dataset_397415_4.txt", "r")

Text = file.readlines()[0].strip('\n')
# Text = "TCGGTAGATTGCGCCCACTC"
SuffixTree = SuffixTreeConstruct(Text)
results = open(r"stresults.txt", "a")
for edge in SuffixTree.keys(): 
	print(edge, SuffixTree[edge])
	# print(edge, file=results)