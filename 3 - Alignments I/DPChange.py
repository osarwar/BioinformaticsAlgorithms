import numpy as np 
from copy import copy 
"""
Name: OWAIS SARWAR

Code Challenge: Solve the Change Problem. The DPChange pseudocode is reproduced below for your convenience.

Input: An integer money and an array Coins = (coin1, ..., coind).
Output: The minimum number of coins with denominations Coins that changes money.

Sample Input:

40
50,25,20,10,5,1

Sample Output:

2

"""

f = open("dataset_397337_10.txt", "r")
data = f.readlines()

#Money 
money = int(data[0].strip('\n'))

#Coins  
Coins = data[1].strip('\n')

Coins = Coins.split(",")

for idx, coin in enumerate(Coins): 
	Coins[idx] = int(coin)

# Coins = [50, 25, 20, 10, 5, 1]
# money = 40 

def DPChange(money, Coins): 

	MinNumCoins = np.zeros(money+1)

	for m in range(1, money+1): 
		MinNumCoins[m] = 1e10
		for i in range(0, len(Coins) - 1): 
			if m >= Coins[i]: 
				if MinNumCoins[m - Coins[i]] + 1 < MinNumCoins[m]: 
					MinNumCoins[m] = MinNumCoins[m - Coins[i]] + 1 

	return int(MinNumCoins[money])

print(DPChange(money, Coins))
