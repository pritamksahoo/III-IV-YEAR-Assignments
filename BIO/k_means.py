def eucledian_dst(p1, p2):
	dst = 0

	for index, val in enumerate(p1):
		dst = dst + (val - p2[index])**2

	return dst


def k_mean(no_points, points_in_5D, no_clusters, origins):
	change = True
	clusters = [0]*no_points

	while change == True:
		for index_point, point in enumerate(points_in_5D):
			min_dst, closest_org = 1000000000, 0 
			for index_org, org in enumerate(origins):
				dst = eucledian_dst(point, org)

				if min_dst > dst:
					min_dst = dst
					closest_org = index_org

			if clusters[index_point] == closest_org:
				change = False
			else:
				clusters[index_point] = closest_org
				change = True

	origins = [[0, 0]]*no_clusters

	for index_cluster, cluster in enumerate(clusters):
		origins[cluster] = [origins[cluster][0]+points_in_5D[index_cluster][0], origins[cluster][1]+points_in_5D[index_cluster][1]]

	# print("origins", origins, "clusters", clusters)

	for cluster in range(no_clusters):
		cnt = clusters.count(cluster)
		origins[cluster] = [origins[cluster][0]/cnt, origins[cluster][1]/cnt]

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