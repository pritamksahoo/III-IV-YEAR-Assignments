if __name__ == '__main__':
	arr1 = list(map(int, input().split()))
	arr2 = list(map(int, input().split()))

	# f = lambda x, y: list((set(x)).intersection(set(y)))
	arr = list(filter(lambda x: x in arr2, arr1))
	# arr = f(arr1, arr2)
	print(arr)
