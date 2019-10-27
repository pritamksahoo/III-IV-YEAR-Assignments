COMPLETE_LINKAGE = 0
SINGLE_LINKAGE = 1


def eucledian_dst(p1, p2):
	dst = 0
	# print(p1, p2, end=' ')
	for index, val in enumerate(p1):
		dst = dst + (val - p2[index])**2

	return dst**(0.5)


def hierarchical_cluster(points_in_5D, no_points, dist_metric, cluster, cluster_th, flag):
	while len(cluster) > 1:
		# print(cluster)
		min_dst, from_c, to_c, len_c, cluster_list = 1000000000, 0, 1, len(cluster), list(cluster.keys())

		# Minimum distance selection
		for ind1 in range(len_c):
			for ind2 in range(ind1+1, len_c):
				p1, p2 = cluster_list[ind1], cluster_list[ind2]

				dst = dist_metric[p1].get(p2, None)
				if dst is None:
					dst = dist_metric[p2][p1]

				if dst < min_dst:
					min_dst = dst
					from_c, to_c = p1, p2

		if from_c > to_c:
			from_c, to_c = to_c, from_c

		# Threshold acheived, so out of loop
		# print(min_dst)
		if min_dst > cluster_th:
			break

		# Forming New Cluster
		new_pts = cluster[to_c]['points']
		for point in new_pts:
			cluster[from_c]['points'].append(point)

		cluster[from_c]['measure'] = min_dst
		cluster.pop(to_c)

		# Linkage
		for other_cluster in list(cluster.keys()):
			if other_cluster != from_c:

				dst1 = dist_metric[from_c].get(other_cluster, None)
				if dst1 is None:
					dst1 = dist_metric[other_cluster][from_c]

				dst2 = dist_metric[to_c].get(other_cluster, None)
				if dst2 is None:
					dst2 = dist_metric[other_cluster][to_c]

				# New distance metric
				if flag == COMPLETE_LINKAGE:
					dst = max(dst1, dst2)
				else:
					dst = min(dst1, dst2)

				dist_metric[from_c][other_cluster] = dst

		dist_metric.pop(to_c)

	return cluster


if __name__ == '__main__':
	no_points = int(input())
	points_in_5D = []

	for i in range(no_points):
		points_in_5D.append(list(map(int, input().split())))

	dist_metric = {}

	for i in range(no_points):
		dist_metric[i] = {}

	# Calculating and storing distance b/w points
	for i in range(no_points):
		for j in range(i+1, no_points):
			dst = eucledian_dst(points_in_5D[i], points_in_5D[j])

			dist_metric[i][j] = dst

	cluster = {}
	for i in range(no_points):
		cluster[i] = {'points': [i], 'measure': 0}

	cluster_th = int(input())
	# Complete linkage or Single linkage (0 or 1)
	flag = int(input())

	cluster = hierarchical_cluster(points_in_5D, no_points, dist_metric, cluster, cluster_th, flag)

	# print(cluster)
	for key in cluster:
		print()
		print("Cluster", key, ":", end=' ')
		
		for point_ind in cluster[key]['points']:
			print(points_in_5D[point_ind], end = ' ')

		print("| Measure : ", cluster[key]['measure'])

	print()