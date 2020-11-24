import numpy as np 
from copy import copy 
"""
Name = Owais Sarwar

Code Challenge: Solve the Multiple Approximate Pattern Matching Problem.

Input: A string Text, followed by a collection of strings Patterns, and an integer d.
Output: All positions where one of the strings in Patterns appears as a substring of Text with at most d mismatches.

Sample Input:

ACATGCTACTTT
ATT GCC GCTA TATT
1

Sample Output:

2 4 4 6 7 8 9
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
def GenSeeds(k, d, Pattern): 
	seeds = []
	for s in range(d+1): 
		if s != d: 
			seeds.append(Pattern[s*k:(s+1)*k])
		else: 
			seeds.append(Pattern[s*k:len(Pattern)])
	return seeds 

file = open(r"MultipleApproximatePatternMatching_sample.txt", "r")
file = open(r"MultipleApproximatePatternMatching_test.txt", "r")
file = open(r"dataset_397424_6.txt", "r")
data = file.readlines()

Text = data[0].strip('\n')
print(Text)
SuffixArray  = SuffixArrayConstruction(Text)
BWT = BurrowsWheelerTransform(Text)
Patterns = data[1].strip('\n').split()
d = int(data[2].strip('\n'))

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
# results = open(r"results_mapm.txt", "a")
LastToFirst = [FirstColumn.index(char) for char in LastColumn]
LastColumn = copy(BWT)
Matches = {}
results = open(r"results_mapm.txt", "a")
for Pattern in Patterns: 
	k = int(np.floor(len(Pattern) / (d+1)))
	seeds = GenSeeds(k, d, Pattern)
	for seed_num, seed in enumerate(seeds): 
		num = BWMatching(LastColumn, list(seed), LastToFirst)
		if num != 0: 
			match = copy(seed)
			# print()
			# print(match, num)
			match_index_in_pattern = seed_num*k 
			count = 0 
			sa_idx = 0 
			# print("num", num)
			skip = False 
			while count != num: 
				discrepancies = 0 
				#Find location of match 
				if sa_idx < len(SuffixArray):
					while True:  
						# print(Pattern, count, match, SuffixArray[sa_idx])
						if sa_idx < len(SuffixArray):
							if Text[SuffixArray[sa_idx]:SuffixArray[sa_idx]+len(match)] == match: 
								# print(SuffixArray[sa_idx], end=" ")
								match_index_in_text = SuffixArray[sa_idx]
								# print(SuffixArray[sa_idx], end=" ", file=results)
								sa_idx += 1 
								count += 1
								break 
							else: 
								sa_idx += 1 
						else: 
							skip = True 
							count += 1 
							break 
					if not skip: 
						#Expand and compare pattern to the right 
						match_index_in_text_right = match_index_in_text + len(match)
						match_index_in_pattern_right = match_index_in_pattern + len(match)
						while discrepancies <= d and match_index_in_pattern_right < len(Pattern): 
							if Text[match_index_in_text_right] != Pattern[match_index_in_pattern_right]: 
								discrepancies+= 1 
							match_index_in_text_right += 1 
							match_index_in_pattern_right += 1 

						#Expand and compare pattern to the left
						match_index_in_text_left = copy(match_index_in_text)
						match_index_in_pattern_left = copy(match_index_in_pattern)   
						while discrepancies <= d and match_index_in_pattern_left-1 >= 0:
							match_index_in_text_left -= 1 
							match_index_in_pattern_left -= 1 
							if Text[match_index_in_text_left] != Pattern[match_index_in_pattern_left]: 
								discrepancies+= 1 
						if discrepancies <= d: 
							# print(Pattern)
							if Pattern not in Matches.keys():
								Matches[Pattern] = [match_index_in_text_left]
								print(match_index_in_text_left, end=" ", file=results)
							if match_index_in_text_left not in Matches[Pattern]: 
								Matches[Pattern] += [match_index_in_text_left]
								print(match_index_in_text_left, end=" ", file=results)

				else: 
					count += 1 