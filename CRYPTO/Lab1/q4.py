import gmpy2 as mp

if __name__ == '__main__':
	state = mp.random_state()
	bit_len = mp.mpz(input("Enter bit length : "), 10)

	for i in range(10):
		print(mp.mpz_urandomb(state, bit_len))
