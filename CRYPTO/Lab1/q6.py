import gmpy2 as mp

if __name__ == '__main__':
	a = mp.mpz(input("Enter 1st number : "), 10)
	b = mp.mpz(input("Enter 2nd number : "), 10)

	while b != 0:
		r = mp.remainder(a, b)
		a, b = b, r

	print("G.C.D. : ", a)
