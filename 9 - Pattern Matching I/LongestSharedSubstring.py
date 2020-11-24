import numpy as np 
from copy import copy 
import sys 
sys.setrecursionlimit(10000000)
"""
Name = Owais Sarwar


Longest Shared Substring Problem: Find the longest substring shared by two strings.

Input: Strings Text1 and Text2.
Output: The longest substring that occurs in both Text1 and Text2.

Code Challenge: Solve the Longest Shared Substring Problem. (Multiple solutions may exist, in which case you may return any one.)

Sample Input:

TCGGTAGATTGCGCCCACTC
AGGGGCTCGCAGTGTAAGAA

Sample Output:

AGA
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
	# print(Text)
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

def LongestSharedSubstring2(Text1, Text2): 

	SuffixTree = SuffixTreeConstruct(Text1[:-1]+"#"+Text2)
	# for edge in SuffixTree.keys(): 
	# 	print(edge, SuffixTree[edge])

	print("--------")

	Colored_ST = {}
	for node in SuffixTree.keys():
		if SuffixTree[node][1] not in Colored_ST.keys():
			Colored_ST[SuffixTree[node][1]] = {'children':{}, 'color':'g'}
			if "$" in SuffixTree[node][0] and "#" not in SuffixTree[node][0]:
				color = "r"
			elif "#" in SuffixTree[node][0]:
				color = "b"
			else: 
				color = "g"
			Colored_ST[SuffixTree[node][1]]['children'][node] = SuffixTree[node][0]
			if color != "g": 
				Colored_ST[node] = {'children':{}, 'color':color}
		else: 
			if "$" in SuffixTree[node][0] and "#" not in SuffixTree[node][0]:
				color = "r"
			elif "#" in SuffixTree[node][0]:
				color = "b"
			else: 
				color = "g"
			Colored_ST[SuffixTree[node][1]]['children'][node] = SuffixTree[node][0]
			if color != "g": 
				Colored_ST[node] = {'children':{}, 'color':color}

	# print(Colored_ST, end="\n")

	def colorTree(Colored_ST, node): 
		if len(Colored_ST[node]['children']) == 0: 
			return 
		for child in Colored_ST[node]['children']: 
			colorTree(Colored_ST, child)
		colors_of_children = [Colored_ST[child]['color'] for child in Colored_ST[node]['children'].keys()] 
		if all(colors_of_children) == 'r': 
			color_node = 'r'
		elif all(colors_of_children) == 'b': 
			color_node = 'b'
		else: 
			color_node = 'p'
		Colored_ST[node]['color'] = color_node
		return 

	def possible_substrings(candidates, string, node, Colored_ST): 

		for child in Colored_ST[node]['children'].keys(): 
			edge = Colored_ST[node]['children'][child]
			color_child = Colored_ST[child]['color']
			if node == 0: 
				string = ""
			if "$" not in edge and "#" not in edge and color_child == 'p': 
				string += edge
				candidates.append(string)
				possible_substrings(candidates, string, child, Colored_ST)
				# candidates.append(string)
			else: 
				if string != "":
					candidates.append(string)

	colorTree(Colored_ST, 0)

	# print(Colored_ST, end="\n")
	# print(Colored_ST[0])
	# print(Colored_ST[199])
	# print(Colored_ST[200])
	# print(Colored_ST[201])

	candidates = []; string = ""
	possible_substrings(candidates, string, 0, Colored_ST)
	print(candidates)
	print("AACAGAAG" in candidates)
	LSS = ""
	for string in candidates: 
		if string in Text1 and string in Text2 and len(string) > len(LSS): 
			LSS = copy(string)
	return LSS



file = open(r"LongestSharedSubstring_sample.txt", "r")
(?# file = open(r"LongestSharedSubstring_test.txt", "r"))
# file = open(r"dataset_397415_6.txt", "r")
data = file.readlines()
Text1 = data[0].strip('\n') + "$"
Text2 = data[1].strip('\n') + "$"
# Text1 = "panama$"
# Text2 = "bananas$"
# Text1 = "nonsense$"; Text2 = "offense$"
LSS  = LongestSharedSubstring2(Text1, Text2)
# results = open(r"stresults.txt", "a")

print(LSS)

