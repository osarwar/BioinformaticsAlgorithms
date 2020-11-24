import numpy as np 
from copy import copy 
"""
Suffix Array Construction Problem: Construct the suffix array of a string.

Input: A string Text.
Output: SuffixArray(Text).

Code Challenge: Solve the Suffix Array Construction Problem.

Sample Input:

AACGATAGCGGTAGA$

Sample Output:

15, 14, 0, 1, 12, 6, 4, 2, 8, 13, 3, 7, 9, 10, 11, 5
"""

def SuffixArrayConstruction(Text): 
	SuffixArray = []
	suffixes = [Text[i:] for i in range(len(Text))]
	old_suffixes = copy(suffixes)
	suffixes.sort()
	for i in suffixes: 
		SuffixArray.append(old_suffixes.index(i))
	return SuffixArray


file = open(r"SuffixArrayConstruction_sample.txt", "r")
# file = open(r"LongestSharedSubstring_test.txt", "r")
file = open(r"dataset_397416_2.txt", "r")
data = file.readlines()
Text = data[0].strip('\n')

SuffixArray  = SuffixArrayConstruction(Text)
# results = open(r"stresults.txt", "a")

for index in SuffixArray:
	print(index, end=", ")

