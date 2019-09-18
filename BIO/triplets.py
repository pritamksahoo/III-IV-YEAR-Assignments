no_char, pair = 4, 3
dict_char = {'a':0, 'c':1, 'g':2, 't':3}


class Triplet(object):
	'''
	Trie data structure to store triplets and their frequencies
	'''
	def __init__(self):
		super(Triplet, self).__init__()
		self.freq = 0
		self.children = [None for i in range(no_char)]
		

def add_to_suffix_tree(triplet, part):
	'''
	Function to add a triplet to Trie data structure
	Parameters:
		triplet : Pointer to the root od Trie
		part    : The actual triplet to enter into the Trie
	'''
	trip = triplet
	ret = 0

	for i in range(pair):
		val = dict_char[part[i]]

		if trip.children[val] is None:
			trip.children[val] = Triplet()
			trip = trip.children[val]

		else:
			trip = trip.children[val]
			trip.freq = trip.freq + 1

			if i == pair-1:
				ret = trip.freq

	return ret


if __name__ == '__main__':
	string = input()
	triplet = Triplet()
	max_freq, ans = 0, list()

	for i in range(0,len(string)-pair+1):
		part = string[i:i+pair]
		freq = add_to_suffix_tree(triplet, part)

		if freq > max_freq:
			ans = [part]
			max_freq = freq

		elif freq == max_freq:
			ans.append(part)

	print("Triplets :-", ans, "|| Frequency :-", max_freq)