'''
Solving Traveling Salesman Problem using A* algorithm
## Pritam Kumar Sahoo ##
'''

from collections import defaultdict
import heapq
from treelib import Node, Tree
import sys
import subprocess


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


def choose_min_key_for_mst(node_dict):
	'''
	Returns the key with minimum value
	Parameters:
		node_dict : The input dictionary
	'''
	ret_key, min_val = None, sys.maxsize

	for node, val in node_dict.items():
		if min_val > val[1]:
			min_val = val[1]
			ret_key = node

	return ret_key if ret_key is not None else list(node_dict.keys())[0]


def find_MST(graph, nodes=None):
	'''
	Find the minimum spanning tree of a given graph, considering only specific nodes
	Parameters:
		graph : The actual graph
		nodes : List of nodes to be considered in the MST, by default All.
	''' 
	MST = list()
	NOT_MST = None
	INFINITY = sys.maxsize

	# Intializing Non MST dictionary :: {node : (source, cost from source to node), ... }
	if nodes is None:
		NOT_MST = { node : ('#', INFINITY) for node in graph.keys()}
	else:
		NOT_MST = { node : ('#', INFINITY) for node in nodes}

	while len(NOT_MST) != 0:
		# Find the key with manimum value
		min_key = choose_min_key_for_mst(NOT_MST)

		# Adding the node to the MST list and removing from Non MST (ret[0] contains the source)
		ret = NOT_MST.pop(min_key)
		# if ret[0] != '#':
		MST.append((ret[0], min_key))

		# Updating the source and cost from source of neighbour nodes of the returned key
		for neighbour, val in graph[min_key].items():
			if NOT_MST.get(neighbour, None) is not None and val < NOT_MST.get(neighbour)[1]:
				NOT_MST[neighbour] = (min_key, val)

	if len(MST) > 0:
		MST.pop(0)

	return MST


def find_optimal_tsp_path(graph):
	'''
	Finds the optimal tour (min-cost tour) given the consition that each node has to visited only once
	Parameters:
		graph : The actual graph
	Returns:
		The optimal path (In form of a list)
	'''
	fringe_list, expanded_list, tree_node_id, no_nodes_expanded, no_nodes_generated = [], Tree(), 1, 0, 0

	# Fringe List stores nodes generated and not yet expanded (min-heap implementation) :: [(f-value, g-value, node, parent node_id), ... ]
	# Expanded List stores expanded nodes in form of a tree :: (node_data, unique_id, parent_unique_id)
	fringe_list.append((0, 0, list(graph.keys())[0], '#'))
	heapq.heapify(fringe_list)

	# Running the loop until an optimal path is found
	while True:
		# Picking the node with smallest f-value from fringe list
		smallest_f_value = heapq.heappop(fringe_list)
		g_value, node, p_node = smallest_f_value[1], smallest_f_value[2], smallest_f_value[3]

		# Adding the node to the tree
		if p_node == '#':
			temp_node = expanded_list.create_node(identifier=str(tree_node_id), data=node)
			tree_node_id = tree_node_id + 1
		else:
			temp_node = expanded_list.create_node(identifier=str(tree_node_id), data=node, parent=p_node)
			tree_node_id = tree_node_id + 1

		# Storing all the nodes from root to the current node
		parent_nodes = [node]
		while expanded_list.parent(temp_node.identifier) != None:
			temp_node = expanded_list.parent(temp_node.identifier)
			parent_nodes.append(temp_node.data)

		# If number of collected nodes is the actual total number of nodes, then path has been found, returning it
		if len(parent_nodes) == len(graph)+1:
			return (parent_nodes[::-1]), no_nodes_expanded, no_nodes_generated
		else:
			# Otherwise, finding the h-value of the successor nodes via find_MST() unction
			unvisited_nodes = sorted(list(set(graph.keys()).difference(set(parent_nodes))))
			# Call to MST function
			mst_path = find_MST(graph, unvisited_nodes)

			h_value, min_dist_start, min_dist_end = 0, sys.maxsize, sys.maxsize 
			# Calculating the MST weight
			for n1, n2 in mst_path:
				if n1 != '#' and n2 != '#': 
					h_value = h_value + graph[n1][n2]

			# Finding shortest distance from start and end of the already determined path which connect the rest of MST
			for node_el in unvisited_nodes:
				if graph[parent_nodes[0]].get(node_el, None) is not None:
					min_dist_end = min(min_dist_end, graph[parent_nodes[0]][node_el])

				if parent_nodes[0] != parent_nodes[-1]:
					if graph[parent_nodes[-1]].get(node_el, None) is not None:
						min_dist_start = min(min_dist_start, graph[parent_nodes[-1]][node_el])

				else:
					min_dist_start = 0

			if min_dist_start == sys.maxsize:
				min_dist_start = 0

			if min_dist_end == sys.maxsize:
				min_dist_end = 0

			# Calculating Final h-value
			h_value = h_value + min_dist_start + min_dist_end

			# Adding the successor nodes to the fringe list with it's h-value, f-value and, parent_node_id
			for neighbour, true_val in graph[node].items():
				if neighbour not in parent_nodes:
					f_value = h_value + true_val + g_value
					heapq.heappush(fringe_list, (f_value, true_val + g_value, neighbour, str(tree_node_id-1)))
					no_nodes_generated = no_nodes_generated + 1

				elif len(parent_nodes) == len(graph) and neighbour == parent_nodes[-1]:
					heapq.heappush(fringe_list, (f_value, true_val + g_value, neighbour, str(tree_node_id-1)))
					no_nodes_generated = no_nodes_generated + 1

			no_nodes_expanded = no_nodes_expanded + 1
			# print(no_nodes_expanded)



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
		# Solving the TSP Problem
		optimal_tsp, expanded_nodes, generated_nodes = find_optimal_tsp_path(graph)
		print("\nOptimal TSP : \n")
		print(optimal_tsp)

		optimal_cost = 0
		for i in range(1,len(optimal_tsp)):
			optimal_cost = optimal_cost + graph[optimal_tsp[i-1]][optimal_tsp[i]]

		print("\nOptimal Cost :", optimal_cost, '\n')
		print("Expanded Nodes : ", expanded_nodes, '\n')
		print("Generated nodes : ", generated_nodes, '\n')

	else:
		print("Graph is empty")