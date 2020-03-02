def add(*argv):
	'''
	Addition of real numbers
	'''
	ret = 0
	try:
		for arg in argv:
			ret = ret + arg

		return ret

	except Exception as e:
		return e
