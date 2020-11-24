import numpy as np 
from copy import copy 
import sys
# print(sys.getrecursionlimit())
sys.setrecursionlimit(2000)

"""
Name: OWAIS SARWAR

Code Challenge: Solve the Longest Path in a DAG Problem.

Input: An integer representing the starting node to consider in a graph, followed by an integer representing the ending node to consider, followed by a list of edges in the graph. The edge notation "0->1:7" indicates that an edge connects node 0 to node 1 with weight 7.  You may assume a given topological order corresponding to nodes in increasing order.
Output: The length of a longest path in the graph, followed by a longest path. (If multiple longest paths exist, you may return any one.)

Sample Input:

0
4
0->1:7
0->2:4
2->3:2
1->4:1
3->4:3

Sample Output:

9
0->2->3->4

"""

f = open("dataset_397340_7.txt", "r")
data = f.readlines()

# data = ["0", 
# "4",
# "0->1:7",
# "0->2:4",
# "2->3:2",
# "1->4:1",
# "3->4:3"]

# data = ["0", 
# "4",
# "0->1:1",
# "1->2:1",
# "3->1:2",
# "4->2:1"]

#start node 
source = int(data[0].strip('\n'))

#end node 
sink = int(data[1].strip('\n'))

origins = []
destinations = []
weights = []

for i in range(2, len(data)): 
	origins.append(int(data[i].strip('\n').replace("->", ":").split(":")[0]))
	destinations.append(int(data[i].strip('\n').replace("->", ":").split(":")[1]))
	weights.append(float(data[i].strip('\n').replace("->", ":").split(":")[2]))

Nodes = np.union1d(origins, destinations)
# print(Nodes)
GraphAdjacencyMatrix = np.zeros((sink+1, sink+1))
for idx, o in enumerate(origins): 
	GraphAdjacencyMatrix[o][destinations[idx]] = weights[idx]

# print(origins, destinations, weights)
# print(GraphAdjacencyMatrix)


def TopologicalOrdering(GraphAdjacencyMatrix): 

	List = []
	Candidates = np.setdiff1d(origins, destinations).tolist()

	while len(Candidates) > 0: 
		a = Candidates[np.random.choice(np.arange(len(Candidates)))]
		Candidates.remove(a)
		List.append(a)
		for b, edge in enumerate(GraphAdjacencyMatrix[a]):
			if edge != 0: 
				GraphAdjacencyMatrix[a][b] = 0
				if np.count_nonzero(GraphAdjacencyMatrix.T[b]) == 0: 
					Candidates.append(b)

	if np.count_nonzero(GraphAdjacencyMatrix) > 0: 
		return "the input graph is not a DAG"
	else: 
		return List 

# print(TopologicalOrdering(GraphAdjacencyMatrix))

def LongestPathLength(GraphAdjacencyMatrix, source, sink): 
	backtrack = np.ones(len(GraphAdjacencyMatrix))*0.5
	s = np.zeros(len(GraphAdjacencyMatrix))
	for node_b in range(len(GraphAdjacencyMatrix)): 
		s[node_b] = -1e10 
	s[source] = 0 
	TopologicalOrder = TopologicalOrdering(GraphAdjacencyMatrix.copy())
	# print(GraphAdjacencyMatrix)
	# print(TopologicalOrder)
	for node_b in TopologicalOrder: 
		# print(node_b)
		nodes_a = np.nonzero(GraphAdjacencyMatrix.T[node_b])[0]
		# print(nodes_a)
		score_path_a_to_b = [s[a] + GraphAdjacencyMatrix[a][node_b] for a in nodes_a]
		if len(score_path_a_to_b) > 0: 
			s[node_b] = max(score_path_a_to_b)
			previous_node = nodes_a[np.argmax(score_path_a_to_b)]
			backtrack[node_b] = previous_node

	# print(backtrack)
	return int(s[sink]), backtrack

def LongestPath(backtrack, source, sink):

	original_sink = copy(sink)

	BackwardsList = [sink]
	while sink != source: 
		# print(sink, source)
		# print(str(sink))
		sink = int(backtrack[sink])
		BackwardsList.append(sink)

	for i in BackwardsList[::-1]:
		if i != original_sink: 
			print(str(i) + "->", end="")
		else: 
			print(str(i))

length_longestpath, backtrack = LongestPathLength(GraphAdjacencyMatrix, source, sink)

print(length_longestpath)
LongestPath(backtrack, source, sink)