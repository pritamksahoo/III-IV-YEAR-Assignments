import gmpy2 as mp

if __name__ == '__main__':
	num1 = mp.mpz(input("Enter 1st number : "), 10)
	num2 = mp.mpz(input("Enter 2nd number : "), 10)

	num3 = mp.mul(num1, num2)

	print("Mult : ", num3)
