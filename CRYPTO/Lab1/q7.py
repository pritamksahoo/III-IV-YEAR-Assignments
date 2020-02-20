import gmpy2 as mp

if __name__ == '__main__':
	print("Equation : ax + by = c")
	a = mp.mpz(input("Value of a : "))
	b = mp.mpz(input("Value of b : "))
	c = mp.gcd(a, b)
	print("So, value of c : ", c)

	mod = mp.mpz(input("Modulo : "), 10)

	x1, x2, y1, y2 = mp.mpz(1), mp.mpz(0), mp.mpz(0), mp.mpz(1)

	while b != 0:
		q = mp.div(a, b)
		r = a - b*q

		x = x1 - q*x2
		y = y1 - q*y2

		a, b = b, r
		x1, x2 = x2, x
		y1, y2 = y2, y

	x1, y1 = mp.remainder(x1, mod), mp.remainder(y1, mod)

	if x1 < 0:
		x1 = x1 + mod

	if y1 < 0:
		y1 = y1 + mod

	print("x : ", mp.mpz(x1), " | y : ", mp.mpz(y1))
