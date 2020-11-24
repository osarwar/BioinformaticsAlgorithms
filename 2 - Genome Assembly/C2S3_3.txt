import numpy as np 
"""
Name: OWAIS SARWAR

Code Challenge: Solve the String Spelled by a Genome Path Problem.

Sample Input:

ACCGA
CCGAA
CGAAG
GAAGC
AAGCT

Sample Output:

ACCGAAGCT

"""

f = open("dataset_397290_3.txt", "r")
data = f.readlines()

#Patters/k-mers  
Patterns = data

for idx, kmer in enumerate(Patterns): 
	Patterns[idx] = kmer.strip('\n')

# Patterns = ["ACCGA",
# "CCGAA",
# "CGAAG",
# "GAAGC",
# "AAGCT"]

Text = ""

for idx, kmer in enumerate(Patterns): 

	if idx == 0: 
		Text += kmer
	else: 
		Text += kmer[-1]

print(Text)
