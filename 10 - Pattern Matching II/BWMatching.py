import numpy as np 
from copy import copy 
"""
Name = Owais Sarwar

Code Challenge: Implement BWMatching.

Input: A string BWT(Text), followed by a collection of Patterns.
Output: A list of integers, where the i-th integer corresponds to the number of substring matches of the i-th member of Patterns in Text.

Sample Input:

TCCTCTATGAGATCCTATTCTATGAAACCTTCA$GACCAAAATTCTCCGGC
CCT CAC GAG CAG ATC

Sample Output:

2 1 1 0 1
"""


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


file = open(r"BWMatching_sample.txt", "r")
file = open(r"dataset_397420_8.txt", "r")

data = file.readlines()
BWT = data[0].strip('\n')
Patterns = data[1].strip('\n').split()
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
BWT = BurrowsWheelerTransform("ACATGCTACTTT")
Patterns = ["TA"]
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

LastToFirst = [FirstColumn.index(char) for char in LastColumn]
LastColumn = copy(BWT)
for Pattern in Patterns: 
	print(BWMatching(LastColumn, list(Pattern), LastToFirst), end=" ")