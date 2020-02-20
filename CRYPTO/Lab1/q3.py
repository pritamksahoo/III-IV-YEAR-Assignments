import gmpy2 as mp

if __name__ == '__main__':
	num = mp.mpz(input("Enter the number : "), 10)

	fac = mp.fac(num)

	print("Factorial : ", fac)
