import gmpy2 as mp

if __name__ == '__main__':
	var = mp.mpz('12345679023243546546', 10)
	var1 = mp.mpz(999999991111111111123456776432345679876543)

	print("Var", var, "Var1", var1)

	f1 = mp.mpq("1110001010/100111", 2)

	print("f1", f1)
