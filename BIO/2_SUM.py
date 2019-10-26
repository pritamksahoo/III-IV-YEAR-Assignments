if __name__ == '__main__':
	k, n = tuple(map(int, input().split()))

	for i in range(k):
		arr = list(map(int, input().split()))

		arr = [(val, index) for index, val in enumerate(arr)]
		arr = sorted(arr, key=lambda x: x[0])

		start, end, found = 0, n-1, False

		while found == False and start < end:
			if arr[start][0]+arr[end][0] == 0:
				found = True

			else:
				abs_start, abs_end = abs(arr[start][0]), abs(arr[end][0])

				if abs_start < abs_end:
					end = end - 1

				else:
					start = start + 1

		if found == True:
			if arr[start][1] < arr[end][1]:
				print(arr[start][1]+1, arr[end][1]+1)
			else:
				print(arr[end][1]+1, arr[start][1]+1)
		else:
			print("-1")