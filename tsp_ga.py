'''
Solving Traveling Salesman Problem using Genetic Algorithm
## Pritam Kumar Sahoo ##
'''

from collections import defaultdict
import numpy as np


def add_new_edge(graph, node1, node2, cost):
	'''
	Adding a new edge to the graph
	Parameters:
		graph : The actual graph :: {'node11' : [(node2, cost2), (node3, cost3), ... ], 'node12' : [ ... ], ...}
		node1 : Source node of the edge
		node2 : Destination node of the edge
		cost  : Cost to travel from node1 to node2
	'''

	graph[node1][node2] = cost
	graph[node2][node1] = cost


def initialize_population(arr, state, size):
	'''
	Initialize the population of size 'size', which each chromosome is basically one permutation of all the nodes
	Parameters:
		arr   : List of graph nodes
		state : To store the chromosomes
		size  : Size of the population
	'''
	for i in range(size):
		permutation = np.random.permutation(arr)

		while permutation in state:
			permutation = np.random.permutation(arr)

		state.append(list(permutation))


def fitness_value(graph, chromosome):
	'''
	Calculates fitness value of one chromosome
	Parameters:
		graph      : The actual graph
		chromosome : One particular chromosome from the population
	Returns:
		The fitness value
	'''
	ret, length = 0, len(chromosome)
	for i in range(length-1):
		ret = ret + graph[chromosome[i]][chromosome[i+1]]

	ret = ret + graph[chromosome[-1]][chromosome[0]]

	return ret


def find_optimal_tsp_path(graph):
	'''
	Tries to finds the optimal tour (min-cost tour) given the consition that each node has to visited only once
	Parameters:
		graph : The actual graph
	Prints optimal path accounted so far
	'''
	pop_size = int(input("Enter the population size : "))
	ga_state = list()

	initialize_population(list(graph.keys()), ga_state, pop_size)





if __name__ == '__main__':
	'''
	Main Function
	'''

	'''
	Prerequisites
	'''
	# print("\nInstalling Some prerequisites (Make sure pip3 is installed) - \n\n")
	# subprocess.call(['pip3', 'install', 'treelib'])

	graph = defaultdict(dict)
	graph_input = None
	# graph_input = [('A', 'B', 20), ('B', 'D', 34), ('C', 'D', 12), ('A', 'C', 42), ('A', 'D', 35), ('B', 'C', 30)]

	# Creating the graph
	if graph_input is not None:
		for n1, n2, c in graph_input:
			add_new_edge(graph, n1, n2, c)

	else:
		print("\nEnter source node, destination node, cost (Space seperated. One record in each line. And put a '/' as EOF) : ")
		line = input()
		while line != '/':
			elem = line.split()
			add_new_edge(graph, elem[0], elem[1], int(elem[2]))
			line = input()

	if len(graph) != 0:
		# Solving the TSP Problem via genetic algorithm
		find_optimal_tsp_path(graph)

	else:
		print("Graph is empty")