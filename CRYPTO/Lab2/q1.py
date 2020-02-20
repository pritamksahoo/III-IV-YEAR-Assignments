import gmpy2 as mp

if __name__ == '__main__':
	print("Equation : ax = b (mod m)")

	a = mp.mpz(input("Value of a : "), 10)
	b = mp.mpz(input("Value of b : "), 10)
	m = mp.mpz(input("Value of m : "), 10)

	gcd = mp.gcd(a, m)

	if mp.remainder(b, gcd) == 0:
		a, b, m = mp.div(a, gcd), mp.div(b, gcd), mp.div(m, gcd)
		inv_a = mp.invert(a, m)
		b = mp.remainder(b*inv_a, m)

		print("Solution space : ")

		for i in range(gcd):
			print(mp.mpz(b + i*m))
	else:
		print("Solution does not exist")
