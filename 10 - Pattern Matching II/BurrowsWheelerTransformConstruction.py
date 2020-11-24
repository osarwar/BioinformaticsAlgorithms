import numpy as np 
from copy import copy 
import sys 
sys.setrecursionlimit(10000000)
"""
Name = Owais Sarwar

Burrows-Wheeler Transform Construction Problem: Construct the Burrows-Wheeler transform of a string.

Input: A string Text.
Output: BWT(Text).

Code Challenge: Solve the Burrows-Wheeler Transform Construction Problem.


Note: Although it is possible to construct the Burrows-Wheeler transform in O(|Text|) time and space, we do not expect you to implement such a fast algorithm. In other words, it is perfectly fine to produce BWT(Text) by first producing the complete Burrows-Wheeler matrix M(Text).

Sample Input:

GCGTGCCTGGTCA$

Sample Output:

ACTGGCT$TGCGGC
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



file = open(r"BurrowsWheelerTransformConstruction_sample.txt", "r")
# file = open(r"BurrowsWheelerTransformConstruction_test.txt", "r"))
file = open(r"dataset_397417_5.txt", "r")
data = file.readlines()
Text = data[0].strip('\n') 
Text =  "TCAGGGCTTG$"
print(BurrowsWheelerTransform(Text))