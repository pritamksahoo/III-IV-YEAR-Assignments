import gmpy2 as mp

def factorize(n):
	factors = []

	if mp.is_prime(n) == True:
		factors = [[n, 1]]
		return factors

	num, start = n, mp.mpz(2)
	while num != 1:
		count = 0
		while mp.remainder(num, start) == 0:
			count = count + 1
			num = mp.div(num, start)

		if count != 0:
			factors.append([start, count])
		start = start + 1

	return factors

def inverse(x, m):
	if mp.gcd(x, m) == 1:
		a, b, t1, t2 = m, x, 0, 1

		while b != 0:
			q = mp.div(a, b)
			r = mp.sub(a, mp.mul(q, b))
			t = mp.sub(t1, mp.mul(q, t2))

			a, b = b, r
			t1, t2 = t2, t

		ans = t1

		ans = mp.mpz(mp.remainder(ans, m))
		if ans < 0:
			ans = mp.add(ans, m)

	else:
		ans = -1

	return ans

if __name__ == '__main__':
	print()

	n = mp.mpz(input("Value of n : "), 10)

	fact_exp = factorize(n)
	print("\nAll prime factors of", n, "alongwith exponent : ", )

	for base, power in fact_exp:
		print("Prime -", base, ", Exp -", power)

	try:
		elem = fact_exp[2][0]
	except Exception as e:
		elem = fact_exp[-1][0]

	elem = elem + 1
	inv_elem = inverse(elem, n)

	if inv_elem == -1:
		print("\nInverse of", elem, "mod", n, "does not exist")
	else:
		print("\nInverse of", elem, "mod", n, ":", inv_elem)

	print()
