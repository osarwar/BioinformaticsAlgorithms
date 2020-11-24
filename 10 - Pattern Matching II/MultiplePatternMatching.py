import numpy as np 
from copy import copy 
"""
Name = Owais Sarwar

Code Challenge: Solve the Multiple Pattern Matching Problem.

Input: A string Text followed by a collection of strings Patterns.
Output: All starting positions in Text where a string from Patterns appears as a substring.

Sample Input:

AATCGGGTTCAATCGGGGT
ATCG
GGGT

Sample Output:

1 4 11 15
"""
def BurrowsWheelerTransform(Text):
	Rotations = []
	n_chars = len(Text)
	for i in range(n_chars): 
		Rotations.append(Text[n_chars-1-i:n_chars] + Text[0:n_chars-1-i])

	Rotations.sort()
	BWT = ""
	for r in Rotations: 
		BWT += r[-1]
	return BWT  

def SuffixArrayConstruction(Text): 
	SuffixArray = []
	suffixes = [Text[i:] for i in range(len(Text))]
	old_suffixes = copy(suffixes)
	suffixes.sort()
	for i in suffixes: 
		SuffixArray.append(old_suffixes.index(i))
	return SuffixArray

def BWMatching(LastColumn, Pattern, LastToFirst): 
	top = 0 
	bottom = len(LastColumn) - 1 
	# print(LastColumn)
	while top <= bottom: 
		if len(Pattern) > 0: 
			symbol = Pattern[-1]
			# print(symbol)
			Pattern.pop(-1)
			if symbol in LastColumn[top:bottom+1]: 
				positions = [idx for idx in range(top,bottom+1) if LastColumn[idx]==symbol]
				topIndex = positions[0]
				bottomIndex = positions[-1]
				top = LastToFirst[topIndex]
				bottom = LastToFirst[bottomIndex]
			else: 
				return 0
		else: 
			return bottom - top + 1


file = open(r"MultiplePatternMatching_sample.txt", "r")
# file = open(r"MultiplePatternMatching_test.txt", "r")
file = open(r"dataset_397423_4.txt", "r")
data = file.readlines()
Text = data[0].strip('\n')
SuffixArray  = SuffixArrayConstruction(Text)
BWT = BurrowsWheelerTransform(Text)
Patterns = []
for line in data[1:]: 
	Patterns.append(line.strip('\n'))
BWT = [char for char in BWT]
num_for_each_char = {}
count_char = {}
for char in BWT:
	if char in num_for_each_char: 
		num_for_each_char[char] += 1 
	else: 
		num_for_each_char[char] = 1 
		count_char[char] = 1 
Characters = []
LastColumn = copy(BWT)
FirstColumn = sorted(BWT)
for idx, char in enumerate(LastColumn): 
	LastColumn[idx] = char + str(count_char[char])
	count_char[char] += 1
for char in count_char.keys():
	count_char[char] = 1
for idx, char in enumerate(FirstColumn): 
	FirstColumn[idx] = char + str(count_char[char])
	count_char[char] += 1
results = open(r"results_mpm.txt", "a")
LastToFirst = [FirstColumn.index(char) for char in LastColumn]
LastColumn = copy(BWT)
for Pattern in Patterns: 
	num = BWMatching(LastColumn, list(Pattern), LastToFirst)
	count = 0 
	sa_idx = 0 
	while count != num: 
		while True: 
			if Text[SuffixArray[sa_idx]:SuffixArray[sa_idx]+len(Pattern)] == Pattern: 
				print(SuffixArray[sa_idx], end=" ")
				sa_idx += 1 
				count += 1
				break 
			else: 
				sa_idx += 1 
