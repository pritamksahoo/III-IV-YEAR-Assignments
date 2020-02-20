import gmpy2 as mp

if __name__ == '__main__':
	n = mp.mpz(input("Value of n : "), 10)
	len = mp.mpz(input("Bit length : "), 10)

	state = mp.random_state()
	count = n

	while count != 0:
		rand = mp.mpz_urandomb(state, len)

		if mp.is_prime(rand):
			print(rand)

			count = count - 1
