import gmpy2 as mp

def factorize(n):
	factors = []

	num, start = n, 2
	while num != 1:
		count = 0
		while mp.remainder(num, start) == 0:
			count = count + 1
			num = mp.div(num, start)

		if count != 0:
			factors.append([start, count])
		start = start + 1

	return factors

if __name__ == '__main__':
	m = mp.mpz(input("Value of m : "), 10)

	'''Finding phi(m)'''
	factors = factorize(m)
	print(factors)

	phi = mp.mpz(1)
	for base, exp in factors:
		phi = phi * (base**exp - base**(exp-1))

	phi = mp.mpz(phi)
	print("Phi value : ", phi)

	factors = factorize(phi)
	print(factors)

	print("All primitive roots : ")

	for root in range(2, m):
		ispre = True

		for base, _ in factors:
			if mp.powmod(root, mp.div(phi, root), m) == 1:
				ispre = False
				break

		if ispre and mp.powmod(root, phi, m) == 1:
			print(root)
