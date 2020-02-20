import gmpy2 as mp

if __name__ == '__main__':
	n = int(input("No. of equations : "))
	print("Enter values af ai's and mi's : ")
	d = [list(map(mp.mpz, input().split())) for i in range(n)]

	mod = mp.mpz(1)
	for i in range(n):
		mod = mod * d[i][1]

	for i in range(n):
		d[i].append(mp.div(mod, d[i][1]))

	for i in range(n):
		inv = mp.invert(d[i][2], d[i][1])

		if inv < 0:
			inv = inv + d[i][1]

		d[i].append(inv)

	ans = mp.mpz(0)

	for i in range(n):
		ans = mp.remainder(ans + d[i][0]*d[i][2]*d[i][3], mod)

	print("Solution : ", mp.mpz(ans))
