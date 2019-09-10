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


def roulette_wheel_selection(fitness_arr, max_parent):
	'''
	Select two parents from the population, between which crossover is to be performed to create next generation child
	Parameters:
		fitness_array : An array consisting of fitness value of each chromosome in the population
	Returns:
		Two parents
	'''
	total_fitness = sum(fitness_array)
	roulette_wheel = [0.0]

	for fit in fitness_array:
		new_val = roulette_wheel[-1] + (fit / total_fitness)
		roulette_wheel.append(new_val)

	no_parent, length, parents = 0, len(roulette_wheel), []
	
	while no_parent != max_parent:
		prob = np.random.random()

		for i in range(1, length):
			if prob >= roulette_wheel[i-1] and prob <= roulette_wheel[i]:
				p = i - 1
				if p not in parents:
					parents.append(i-1)
					no_parent = no_parent + 1

				break

	return parents


def crossover(state, parents, pop_size):
	'''
	Performs a crossover operation between parents, and replace the parents with childs in population
	Parameters:
		state    : Population
		parents  : Two parents selected by roulette-wheel-selection process
		pop_size : Size of the population
	'''
	no_nodes, no_parents = len(state[0]), len(parents)

	for i in range(0, no_parents-1, 2):
		cross_point = np.random.randint(1,no_nodes//2)

		offspring1 = state[i].copy()
		for j in range(cross_point):
			c_index = state[i].index(state[i+1][cross_point])
			offspring1[i][cross_point], offspring1[i][c_index] = offspring1[i][c_index], offspring1[i][cross_point]

		offspring2 = state[i+1].copy()
		for j in range(cross_point):
			c_index = state[i+1].index(state[i][cross_point])
			offspring2[i][cross_point], offspring2[i][c_index] = offspring2[i][c_index], offspring2[i][cross_point]

		state[i], state[i+1] = offspring1, offspring2


def mutation(state, parents):
	'''
	Performs mutation on the childs created after crossover
	Parameters:
		state    : Population
		parents  : Two parents selected by roulette-wheel-selection process
	'''
	no_nodes = len(state[0])
	for p in parents:
		index1, index2 = np.random.randint(0, no_nodes-1), np.random.randint(0, no_nodes-1)
		while index2 == index1:
			index2 = np.random.randint(0, no_nodes-1)

		state[p][index1], state[p][index2] = state[p][index2], state[p][index1]


def find_optimal_tsp_path(graph):
	'''
	Tries to finds the optimal tour (min-cost tour) given the consition that each node has to visited only once
	Parameters:
		graph : The actual graph
	Prints optimal path accounted so far
	'''
	pop_size = int(input("Enter the population size : "))
	max_parent = int(input("Enter the no. of parents selected to create child for next generation : "))
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