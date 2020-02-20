if __name__ == '__main__':
	a = list(map(int, input().split()))
	f = lambda l: ([el for el in l if el%2 == 1]) + ([el for el in l if el%2 == 0])

	new_a = f(a)
	print(new_a)
