import numpy as np 
from copy import copy 
"""
Name = Owais Sarwar

Inverse Burrows-Wheeler Transform Problem: Reconstruct a string from its Burrows-Wheeler transform.

Input: A string Transform (with a single "$" symbol).
Output: The string Text such that BWT(Text) = Transform.

Code Challenge: Solve the Inverse Burrows-Wheeler Transform Problem.

Sample Input:

TTCCTAACG$A

Sample Output:

TACATCACGT$
"""

def InverseBurrowsWheelerTransform(BWT):
	num_for_each_char = {}
	count_char = {}
	for char in BWT:
		if char in num_for_each_char: 
			num_for_each_char[char] += 1 
		else: 
			num_for_each_char[char] = 1 
			count_char[char] = 1 
	Characters = []
	LastColumn = BWT 
	FirstColumn = sorted(BWT)
	for idx, char in enumerate(LastColumn): 
		LastColumn[idx] = char + str(count_char[char])
		count_char[char] += 1
	for char in count_char.keys():
		count_char[char] = 1
	for idx, char in enumerate(FirstColumn): 
		FirstColumn[idx] = char + str(count_char[char])
		count_char[char] += 1
	# print(FirstColumn)
	n_char= len(BWT)
	char = "$1"
	Characters.append(char[0])
	for i in range(n_char): 
		char = FirstColumn[LastColumn.index(char)]
		Characters.append(char[0])
	Text = ''
	for i in range(n_char-1): 
		Text+=Characters[i+1]
	Text += "$"
	return Text 



file = open(r"InverseBurrowsWheelerTransform_sample.txt", "r")
# file = open(r"BurrowsWheelerTransformConstruction_test.txt", "r"))
file = open(r"dataset_397419_10.txt", "r")
data = file.readlines()
BWT = data[0].strip('\n')
BWT =  "TTACA$AAGTC"
BWT = [char for char in BWT]

print(InverseBurrowsWheelerTransform(BWT))