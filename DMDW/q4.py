if __name__ == '__main__':
	l1 = list(map(int, input().split()))
	l2 = list(map(int, input().split()))

	ret = list(filter(lambda x: x not in l2, l1))

	print(ret)
