from collections import defaultdict
import re

cache = 0


def binary_search(l, left, right, current):
	global cache

	while right-left > 1:
		mid = (left + right)//2

		if l[mid] <= current:
			left = mid
		else:
			right = mid

	cache = right

	return right


def galloping_search(l, left, max_index, current):
	global cache

	jump = 1
	right = left + jump

	while right <= max_index and l[right] <= current:
		left, jump = right, 2*jump
		right = left + jump

	right = min(max_index, right)

	ret_index = binary_search(l, left, right, current)
	cache = ret_index

	return ret_index 


def sequential_search(l, left, right, current):
	'''
	Linear Search
	'''
	global cache

	while l[left] <= current and left <= right:
		left = left + 1

	cache = left

	return left


def next_occurrance(inv_adt, term, doc_id, position, flag='BINARY'):
	global cache

	posting_list = inv_adt.get(term, None)

	if posting_list is None:
		return None

	else:
		posting_list = list(filter(lambda x: x[0] == doc_id, posting_list))
		posting_list = [index for val, index in posting_list]

		# print(posting_list)

		if len(posting_list) == 0 or posting_list[-1] <= position:
			return "INF"

		elif posting_list[0] > position:
			cache = 0
			return posting_list[0]

		if cache > 0 and cache < len(posting_list) and posting_list[cache-1] <= position:
			low = cache-1
		else:
			low = 0

		if flag == 'BINARY':
			return posting_list[binary_search(posting_list, low, len(posting_list)-1, position)]
		elif flag == 'GALLOPING':
			return posting_list[galloping_search(posting_list, low, len(posting_list)-1, position)]
		elif flag == 'SEQUENTIAL':
			return posting_list[sequential_search(posting_list, low, len(posting_list)-1, position)]


def next_phrase_occurrance(inv_adt, phrase, doc_id, position, flag='BINARY'):
	'''
	flag : search method used in next_occurrance method
	'''
	pos1 = next_occurrance(inv_adt, phrase[0], doc_id, position, flag)

	pos2 = pos1

	for i in range(1,len(phrase)):
		pos2 = next_occurrance(inv_adt, phrase[i], doc_id, pos2, flag)

	if pos2 == 'INF':
		return ['INF', 'INF']

	else:
		if pos2 - pos1 == len(phrase)-1:
			return [pos1, pos2]
		else:
			return next_phrase_occurrance(inv_adt, phrase, doc_id, pos2-len(phrase), flag)


def tokenize(text, doc_id, corpus):
	split_chars = [" ", "\n", "\-", ",", "\.", "\(", "\)", "\?", "\[", "\]", "\*", ";"]

	delimiter = '|'.join(split_chars)

	tokens = re.split(delimiter, text)

	try:
		while True:
			tokens.remove("")
	except Exception as e:
		pass

	for index, t in enumerate(tokens):
		corpus.append((t.lower(), doc_id, index))


if __name__ == '__main__':
	inverted_index = defaultdict(list)
	text = ""
	no_files_in_corpus = 2

	corpus = []

	for i in range(1,no_files_in_corpus+1):
		with open('input' + str(i) + '.txt', 'r') as f:
			text = f.read()

			tokenize(text, i, corpus)

	corpus = sorted(corpus, key=lambda x: (x[0], x[1], x[2]))

	for term, doc_id, index in corpus:
		inverted_index[term].append((doc_id, index))

	print(inverted_index)

	# print(next_occurrance(inverted_index, 'the', 2, 108, 'BINARY'))
	# print(next_occurrance(inverted_index, 'the', 2, 108, 'GALLOPING'))
	# print(next_occurrance(inverted_index, 'the', 2, 108, 'SEQUENTIAL'))
	print(next_phrase_occurrance(inverted_index, ['the', 'best'], 1, 10))