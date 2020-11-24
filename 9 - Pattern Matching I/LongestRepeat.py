import numpy as np 
from copy import copy 
import sys 
sys.setrecursionlimit(10000000)
"""
Name = Owais Sarwar


Longest Repeat Problem: Find the longest repeat in a string.

Input: A string Text.
Output: A longest substring of Text that appears in Text more than once.

Code Challenge: Solve the Longest Repeat Problem. (Multiple solutions may exist, in which case you may return any one.)

Sample Input:

ATATCGTTTTATCGTT

Sample Output:

TATCGTT
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
					SuffixTree[child]=[edge, origin]
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

def LongestRepeat(Text): 

	SuffixTree = SuffixTreeConstruct(Text)

	LR = ""

	Potential_LRs = []
	# print(SuffixTree)

	for edge_origin in SuffixTree.values(): 
		pot_LR = ""; 
		if "$" not in edge_origin[0]: 
			origin = edge_origin[1]
			pot_LR = edge_origin[0] + pot_LR
			while origin != 0:
				edge_origin = SuffixTree[edge_origin[1]]
				origin = edge_origin[1]
				pot_LR = edge_origin[0] + pot_LR
		if len(pot_LR) > len(LR): 
			LR = copy(pot_LR)  

	return LR 



file = open(r"LongestRepeat_sample.txt", "r")
file = open(r"dataset_397415_5.txt", "r")

Text = file.readlines()[0].strip('\n') + "$"
# Text = "AATTTCCGACTTGCATGACGAGTCAGCGTTCCATCTGATCGAGTCTCCGAAGAACAAATACCCCTACTCAGTTGTGAGCCCCTTTACCGTGAGGACAGGGTCCTTGATGTCGTCTCCTAATTTGCGTTGCGGCTCAACATGTTGTACATAGTGGGGCCAGCCCCAGGGATTTTGTAATTTCTACACTCCATATACGGGACAAGGGTGAGCATTTCCGGGCTTGGATAGGGGCTGCAAGAAAATATCTGGACGTAAGAACTTAATGCCATTCCTACATCCTCGATACCTCGTCTGTCAGAGCAATGAGCTGGTTAGAGGACAGTATTGGTCGGTCATCCTCAGATTGGGGACACATCCGTCTCTATGTGCGTTCCGTTGCCTTGTGCTGACCTTGTCGAACGTACCCCATCTTCGAGCCGCACGCTCGACCAGCTAGGTCCCAGCAGTGGCCTGATAGAAAAATTACCTACGGGCCTCCCAATCGTCCTCCCAGGGTGTCGAACTCTCAAAATTCCCGCATGGTCGTGCTTCCGTACGAATTATGCAAACTCCAGAACCCGGATCTATTCCACGCTCAACGAGTCCTTCACGCTTGGTAGAATTTCATGCTCGTCTTTTGTATCCGTGTAAGTAGGAGGCCGCTGTACGGGTATCCCAGCCTTCGCGCTCTGCTGCAGGGACGTTAACACTCCGAACTTTCCATATACGGGACAAGGGTGAGCATTTCCGGGCTTGGATAGGGGCTGCAAGAAAATATCTGGACGTAAGAAGCTCTGAGGGATCCTCACGGAGTTAGATTTATTTTCCATATACGGGACAAGGGTGAGCATTTCCGGGCTTGGATAGGGGCTGCAAGAAAATATCTGGACGTAAGAAGAGTGATGTTTGGAATGCCAACTTCCATGCACGCCAATTGAGCAATCAGGAGAATCGAGTGCTGTTGACCTAGACCTTGTCAGAAGTATGAATTAACCGCGCGTGTAGGTTTGTCGCTCGACCTGCAAGGGTGCACAATCTGGACTGTCGTCGGCGAACGCTTTCATACGCCTACAAACCGCGTTGCTGGTCGAATCGATCTCACCACCGGCCTTGCAGGATTCTAATTATTCTCTCTCGGTGAGACTGCCGGCGGTCCATGGGTCTGTGTTTCGCTTCAAGCAGTGATATACTGGCGTTTTGTGACACATGGCCACGCACGCCTCTCGTTACTCCCAAT"
LR = LongestRepeat(Text)
# results = open(r"stresults.txt", "a")

print(LR)