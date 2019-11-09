graph = {}
delta = 0.85

if __name__ == '__main__':
	line = input()
	all_nodes = set()

	while line != "/":
		f, t = line.split()
		all_nodes.add(f)
		all_nodes.add(t)

		if graph.get(f, None) is None:
			graph[f] = {t : 1}

		else:
			graph[f][t] = 1

		line = input()

	no_nodes = len(all_nodes)

	rank = [1/no_nodes]*no_nodes
	rank2 = [1]*no_nodes

	nodes = sorted(list(all_nodes))
	# print(graph)
	graph_nodes = sorted(list(graph.keys()))

	itr = 10
	while itr != 0:
		temp_rank = []
		temp_rank2 = []

		for key in nodes:
			r = ((1 - delta) / no_nodes)
			r2 = (1 - delta)

			for key2 in graph_nodes:
				if key != key2:
					if graph[key2].get(key, None) is not None:
						r = r + (rank[nodes.index(key2)] / len(graph[key2])) * delta
						r2 = r2 + (rank2[nodes.index(key2)] / len(graph[key2])) * delta

						# print(key, key2, nodes.index(key2), len(graph[key2]))

			temp_rank.append(r)
			temp_rank2.append(r2)

		s = no_nodes
		for i in range(no_nodes):
			s = s - temp_rank2[i]

		# print(s, no_nodes)
		for i in range(no_nodes):
			temp_rank2[i] = temp_rank2[i] + (s / no_nodes)

		rank = temp_rank.copy()
		rank2 = temp_rank2.copy()

		itr = itr - 1

		print("Rank", rank, '\n')
		# print("Rank2", rank2, '\n')
