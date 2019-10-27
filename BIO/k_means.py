dim = 5

def eucledian_dst(p1, p2):
	dst = 0
	# print(p1, p2, end=' ')
	for index, val in enumerate(p1):
		dst = dst + (val - p2[index])**2

	return dst


def k_mean(no_points, points_in_5D, no_clusters, origins):
	change = True
	clusters = [0]*no_points

	while change == True:
		# Finding clusters in which points will fit into
		for index_point, point in enumerate(points_in_5D):
			min_dst, closest_org = 1000000000, 0 
			for index_org, org in enumerate(origins):
				dst = eucledian_dst(point, org)

				if min_dst > dst:
					min_dst = dst
					closest_org = index_org

			# No cange
			if clusters[index_point] == closest_org:
				change = False
			else:
				# Change
				clusters[index_point] = closest_org
				change = True

		# Updating origins
		# origins = [[0]*dim]*no_clusters
		origins = [[0 for i in range(dim)] for j in range(no_clusters)]

		for index_cluster, cluster in enumerate(clusters):
			for i in range(dim):
				origins[cluster][i] = origins[cluster][i] + points_in_5D[index_cluster][i]

		# print("origins", origins, "clusters", clusters)

		for cluster in range(no_clusters):
			cnt = clusters.count(cluster)
			if cnt != 0:
				for i in range(dim):
					origins[cluster][i] = origins[cluster][i]/cnt

		print(clusters, origins, '\n')

	return clusters, origins


if __name__ == '__main__':
	no_points = int(input())
	points_in_5D = []

	for i in range(no_points):
		points_in_5D.append(list(map(int, input().split())))

	no_clusters = int(input())
	origins = []

	for i in range(no_clusters):
		origins.append(list(map(int, input().split())))

	clusters, origins = k_mean(no_points, points_in_5D, no_clusters, origins)

	print(clusters, origins)