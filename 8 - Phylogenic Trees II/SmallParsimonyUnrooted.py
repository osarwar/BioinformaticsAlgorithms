import numpy as np 
from copy import copy, deepcopy
import sys 
sys.setrecursionlimit(1000000)
"""
Name = Owais Sarwar

Code Challenge: Solve the Small Parsimony in an Unrooted Tree Problem.

Input: An integer n followed by an adjacency list for an unrooted binary tree with n leaves labeled by DNA strings.
Output: The minimum parsimony score of this tree, followed by the adjacency list of the tree corresponding to labeling internal nodes by DNA strings in order to minimize the parsimony score of the tree.

Sample Input:

4
TCGGCCAA->4
4->TCGGCCAA
CCTGGCTG->4
4->CCTGGCTG
CACAGGAT->5
5->CACAGGAT
TGAGTACC->5
5->TGAGTACC
4->5
5->4

Sample Output:

17
TCGGCCAA->CCAGGCAC:4
CCTGGCTG->CCAGGCAC:3
TGAGTACC->CAAGGAAC:4
CCAGGCAC->CCTGGCTG:3
CCAGGCAC->CAAGGAAC:2
CCAGGCAC->TCGGCCAA:4
CACAGGAT->CAAGGAAC:4
CAAGGAAC->CACAGGAT:4
CAAGGAAC->TGAGTACC:4
CAAGGAAC->CCAGGCAC:2
"""

def SmallParsimony(T, character):
	def SkVcalc(): 
		Daughter_v = T[node_v][0]; Son_v = Tree[node_v][1]
		min_score_d = np.Inf
		min_score_s = np.Inf
		for i_idx, i in enumerate(alphabet): 
			if i == k: 
				alpha = 0 
			else: 
				alpha = 1
			score_d = s[Daughter_v][i_idx] + alpha
			score_s = s[Son_v][i_idx] + alpha
			if score_d < min_score_d: 
				min_score_d = copy(score_d)
				min_char_d = copy(i)
			if score_s < min_score_s: 
				min_score_s = copy(score_s)
				min_char_s = copy(i)
		return min_score_s + min_score_d, min_char_d, min_char_s
	def backtrack(parent, parent_label, daughter, son):
		if daughter in leaves or son in leaves:  
			pass 
		else: 
			character[daughter] = MinCharacters[parent][parent_label][0]
			character[son] = MinCharacters[parent][parent_label][1]
			backtrack(daughter, character[daughter], Tree[daughter][0], Tree[daughter][1])
			backtrack(son, character[son], Tree[son][0], Tree[son][1])
	def ripe_node(): 
		for node_v in range(n, root_node+1): 
			if Tag[Tree[node_v][0]] == 1 and Tag[Tree[node_v][1]]==1 and Tag[node_v] == 0: 
				Tag[node_v] = 1 
				return node_v

	weights ={}
	leaves = [i for i in range(len(character))]
	alphabet = ["A", "C", "G", "T"]
	root_node = max(list(T.keys()))
	Tag = [0 for _ in range(root_node+1)]
	s = [[0 for k in alphabet] for node_v in range(root_node+1)]
	for node_v in range(root_node+1): 
		if node_v in leaves: 
			Tag[node_v] = 1 
			for k_idx, k in enumerate(alphabet): 
				if character[node_v] == k: 
					s[node_v][k_idx] = 0 
				else: 
					s[node_v][k_idx] = np.Inf
	MinCharacters = {node:{k:[0,0] for k in alphabet} for node in range(len(character), root_node+1)}
	# for node_v in range(len(character), root_node+1):
	while 0 in Tag:  
		node_v = ripe_node()
		for k_idx, k in enumerate(alphabet): 
			s[node_v][k_idx], min_char_d, min_char_s = SkVcalc()
			MinCharacters[node_v][k][0] = min_char_d; MinCharacters[node_v][k][1] = min_char_s
	ParsimonyScore = min(s[root_node])
	weights = {}
	character = character + ["" for _ in range(n, root_node+1)]
	character[root_node] = alphabet[s[root_node].index(min(s[root_node]))]
	backtrack(root_node, character[root_node], T[root_node][0], T[root_node][1])
	for node in range(n, root_node+1): 
		if character[node] == character[Tree[node][0]]: 
			weights[node] = [0]
		else: 
			weights[node] = [1]
		if character[node] == character[Tree[node][1]]: 
			weights[node] += [0]
		else: 
			weights[node] += [1]
	character_all_nodes = character

	return ParsimonyScore, character_all_nodes, weights

file = open(r"SmallParsimonyUnrooted_sample.txt", "r")

# file = open(r"SmallParsimonyUnrooted_test.txt", "r")
file = open(r"dataset_397379_12.txt", "r")


data = file.readlines()

for idx, line in enumerate(data): 
	data[idx] = line.strip("\n")

n = int(data[0])

Tree = {}
characters =[]
for idx, line in enumerate(data[2::2]): 
	d = line.split('->')
	if idx < n: 
		if int(d[0]) in Tree.keys(): 
			Tree[int(d[0])] += [idx]
		else: 
			Tree[int(d[0])] = [idx]
		characters.append(d[1])
	else: 
		if idx != len(data[2::2]) - 1: 
			if int(d[0]) in Tree.keys(): 
				Tree[int(d[0])] += [int(d[1])]
			else: 
				Tree[int(d[0])] = [int(d[1])]
		else: 
			broke_node1, broke_node2 = int(d[0]), int(d[1])
			Tree[int(d[0])+1] = [int(d[0]), int(d[1])]
character_list = [[characters[leaf][position] for leaf in range(n)] for position in range(len(characters[0]))]

Total_PS = 0 
total_weights = {key:[0 for node in Tree[key]] for key in Tree.keys()}
total_characters = ['' for i in range(len(Tree.keys())+n)]
for character in character_list: 
	ParsimonyScore, characters, weights = SmallParsimony(Tree, character)
	# print(ParsimonyScore, weights, characters)
	Total_PS += ParsimonyScore
	# print(weights)
	for parent in total_weights.keys():
		for idx, node in enumerate(total_weights[parent]): 
			total_weights[parent][idx] += weights[parent][idx]
	for idx, char in enumerate(characters): 
		total_characters[idx] += char

root_node = max(Tree.keys())
print(Total_PS)
for node in Tree.keys():
	if node != root_node: 
		for idx, node2 in enumerate(Tree[node]):
			print(total_characters[node], '->', total_characters[node2], ":", int(total_weights[node][idx]), sep='')
			print(total_characters[node2], '->', total_characters[node], ":", int(total_weights[node][idx]), sep='')
			sums+= total_weights[node][idx]
	else: 
		node = broke_node1
		node2 = broke_node2
		print(total_characters[node], '->', total_characters[node2], ":", int(total_weights[root_node][0]) + int(total_weights[root_node][1]), sep='')
		print(total_characters[node2], '->', total_characters[node], ":", int(total_weights[root_node][0]) + int(total_weights[root_node][1]), sep='')
file = open(r"resultsSPUnrooted.txt", "a")
print(Total_PS, file=file)
for node in Tree.keys():
	if node != root_node: 
		for idx, node2 in enumerate(Tree[node]):
			print(total_characters[node], '->', total_characters[node2], ":", int(total_weights[node][idx]), sep='', file=file)
			print(total_characters[node2], '->', total_characters[node], ":", int(total_weights[node][idx]), sep='', file=file)
	else: 
		node = broke_node1
		node2 = broke_node2
		print(total_characters[node], '->', total_characters[node2], ":", int(total_weights[root_node][0]) + int(total_weights[root_node][1]), sep='', file=file)
		print(total_characters[node2], '->', total_characters[node], ":", int(total_weights[root_node][0]) + int(total_weights[root_node][1]), sep='', file=file)
file.close()