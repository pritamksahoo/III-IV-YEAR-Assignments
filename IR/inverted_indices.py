from collections import defaultdict
import re
import numpy as np
import time
from matplotlib import pyplot as plt


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
	'''
	Finding the next occurrance of a word in a document
	flag : search method used in next_occurrance method
	'''
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
	Finding the next occurrance of a phrase in a particular document
	flag : search method used in next_occurrance method
	'''
	pos1 = next_occurrance(inv_adt, phrase[0], doc_id, position, flag)

	pos2 = pos1

	if pos2 == 'INF' or pos2 is None:
		return ['INF', 'INF']
	else:

		for i in range(1,len(phrase)):
			pos2 = next_occurrance(inv_adt, phrase[i], doc_id, pos2, flag)

			if pos2 == 'INF' or pos2 is None:
				break

		if pos2 == 'INF' or pos2 is None:
			return ['INF', 'INF']
		else:
			if pos2 - pos1 == len(phrase)-1:
				return [pos1, pos2]
			else:
				return next_phrase_occurrance(inv_adt, phrase, doc_id, pos2-len(phrase), flag)


def tokenize(text, doc_id=0, corpus = None):
	'''
	Splitting the text aginst some pre-defined delimiter
	'''
	split_chars = [" ", "\n", "\-", ",", "\.", "\"", "\(", "\)", "\?", "\[", "\]", "\*", ";", "\\", "/"]

	delimiter = '|'.join(split_chars)

	tokens = re.split(delimiter, text)

	try:
		while True:
			tokens.remove("")
	except Exception as e:
		pass

	if corpus is not None:
		for index, t in enumerate(tokens):
			corpus.append((t.lower(), doc_id, index))

	else:
		return tokens


if __name__ == '__main__':
	inverted_index = defaultdict(list)
	text = ""
	no_files_in_corpus = 4

	methods = ['BINARY', 'GALLOPING', 'SEQUENTIAL']
	colors = ['r', 'g', 'b']

	corpus = []

	for i in range(1,no_files_in_corpus+1):
		with open('input' + str(i) + '.txt', 'r') as f:
			text = f.read()

			tokenize(text, i, corpus)

	corpus = sorted(corpus, key=lambda x: (x[0], x[1], x[2]))

	for term, doc_id, index in corpus:
		inverted_index[term].append((doc_id, index))

	# print(inverted_index)

	# print(next_phrase_occurrance(inverted_index, ['the', 'indian', 'team'], 1, 250))

	avg_response = defaultdict(dict)

	phrases = []

	with open("phrase.txt", "r") as f:
		for line in f:
			phrases.append(line)


	for phrase in phrases:
		token = tokenize(phrase)
		length = len(token)

		time_taken = dict()

		for i in range(1,no_files_in_corpus+1):

			for method in methods:
				start = time.time()
				next_phrase_occurrance(inverted_index, token, i, 0, method)
				end = time.time()

				time_taken[method] = time_taken.get(method, 0) + (end - start)

		for key in time_taken.keys():
			time_taken[key] = time_taken[key]/no_files_in_corpus

		if avg_response.get(length, None) is not None:
			count = avg_response[length]['count'] + 1
		else:
			count = 1

		avg_response[length]['count'] = count
		for method in methods:
			avg_response[length][method] = (avg_response[length].get(method, 0)*(count-1) + time_taken[method])/count

	print(avg_response)

	'''
	Plotting
	'''

	x = sorted(list(avg_response.keys()))

	for index, method in enumerate(methods):
		y = []
		for key in x:
			y.append((avg_response[key][method])*(10**6))

		plt.plot(x, y, color=colors[index], label=method)

	plt.xlabel("Phrase length")
	plt.ylabel("Avg. respose (microsecond)")
	plt.legend()
	plt.show()