from collections import defaultdict
import re
import numpy as np
import time
from matplotlib import pyplot as plt


methods = ['SEQUENTIAL', 'GALLOPING', 'BINARY']
colors = ['red', 'green', 'blue']
cache = dict()


def binary_search(term, l, left, right, current):
	global cache

	while right-left > 1:
		mid = (left + right)//2

		if l[mid] <= current:
			left = mid
		else:
			right = mid

	cache[term] = right

	return right


def galloping_search(term, l, left, max_index, current):
	global cache

	jump = 1
	right = left + jump

	while right <= max_index and l[right] <= current:
		left, jump = right, 2*jump
		right = left + jump

	right = min(max_index, right)

	ret_index = binary_search(term, l, left, right, current)
	cache[term] = ret_index

	return ret_index 


def sequential_search(term, l, left, right, current):
	'''
	Linear Search
	'''
	global cache

	while l[left] <= current and left <= right:
		left = left + 1

	cache[term] = left

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
			cache[term] = 0
			return posting_list[0]

		if cache[term] > 0 and cache[term] < len(posting_list) and posting_list[cache[term]-1] <= position:
			low = cache[term]-1
		else:
			low = 0

		if flag == 'BINARY':
			return posting_list[binary_search(term, posting_list, low, len(posting_list)-1, position)]
		elif flag == 'GALLOPING':
			return posting_list[galloping_search(term, posting_list, low, len(posting_list)-1, position)]
		elif flag == 'SEQUENTIAL':
			return posting_list[sequential_search(term, posting_list, low, len(posting_list)-1, position)]


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
		return list(map(lambda x: x.lower(), tokens))


def plot_avg_response_against_phrase_length(inverted_index):
	'''
	Plotting avg_response of 'next_phrase_occurrance' against
	length of phrase, for three different type of 'next_occurrance'
	method
	'''
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
				temp = next_phrase_occurrance(inverted_index, token, i, 0, method)
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
			avg_response[length][method] = avg_response[length].get(method, 0) + time_taken[method]

	for key in avg_response.keys():
		for method in methods:
			avg_response[key][method] = avg_response[key][method]/avg_response[key]['count']

	# print(avg_response)

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

	'''END of plot_avg_response_against_phrase_length'''


def length_of_posting_list(inv_adt, term):
	'''
	Returns length of a posting list of a term
	'''
	return len(inv_adt.get(term, []))


def plot_avg_response_against_length_of_posting_list(inverted_index):
	'''
	Plotting avg_response of 'next_phrase_occurrance' against
	length of phrase, for three different type of 'next_occurrance'
	method
	'''
	avg_response = defaultdict(dict)

	phrases = []

	with open("phrase_len_2.txt", "r") as f:
		for line in f:
			phrases.append(line)

	for phrase in phrases:
		token = tokenize(phrase)
		length = max([length_of_posting_list(inverted_index, term) for term in token])

		time_taken = dict()

		for i in range(1,no_files_in_corpus+1):

			for method in methods:
				start = time.time()
				temp = next_phrase_occurrance(inverted_index, token, i, 0, method)
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
			avg_response[length][method] = avg_response[length].get(method, 0) + time_taken[method]

	for key in avg_response.keys():
		for method in methods:
			avg_response[key][method] = avg_response[key][method]/avg_response[key]['count']

	# print(avg_response)

	'''
	Plotting
	'''

	x = sorted(list(avg_response.keys()))

	for index, method in enumerate(methods):
		y = []
		for key in x:
			y.append((avg_response[key][method])*(10**6))

		plt.plot(x, y, color=colors[index], label=method)

	plt.xlabel("Length of longest posting list")
	plt.ylabel("Avg. respose (microsecond)")
	plt.legend()
	plt.show()

	'''END of plot_avg_response_against_length_of_posting_list'''



if __name__ == '__main__':
	inverted_index = defaultdict(list)
	text = ""
	no_files_in_corpus = 4
	corpus = []

	print('\nCreating Inverted index......', end='')

	for i in range(1,no_files_in_corpus+1):
		with open('input' + str(i) + '.txt', 'r') as f:
			text = f.read()

			tokenize(text, i, corpus)

	corpus = sorted(corpus, key=lambda x: (x[0], x[1], x[2]))

	for term, doc_id, index in corpus:
		inverted_index[term].append((doc_id, index))

		if cache.get(term, None) is None:
			cache[term] = 0

	print("Done")

	try:
		while True:

			print('\n---------------------\nChoose your option :- ')
			print('1) Next occurrance search')
			print('2) Next phrase occurrance search')
			print('3) Plot_avg_response_against_phrase_length')
			print('4) Plot_avg_response_against_length_of_posting_list')
			print('5) EXIT')

			print('\nEnter : ', end='')
			option = int(input())

			if option == 1:
				word = input('\nEnter term (word) : ')
				pos = int(input('Current position : '))

				for i in range(1, no_files_in_corpus+1):
					print("\nNext occurrance of \'", word, "\' in doc", '#'+str(i), ":-", next_occurrance(inverted_index, word, i, pos))

			elif option == 2:

				phrases = input('\nEnter phrase (word) : ')
				pos = int(input('Current position : '))

				phrase = tokenize(phrases)

				for i in range(1, no_files_in_corpus+1):
					print("\nNext occurrance of \'", phrases, "\' in doc", '#'+str(i), ":-", next_phrase_occurrance(inverted_index, phrase, i, pos))
				
			elif option == 3:

				print("\nPlotting avg. resonse time against phrase length......", end='')
				plot_avg_response_against_phrase_length(inverted_index)
				print("Done")

			elif option == 4:
				
				print('\nPlotting avg. response time against length of the longest posting list......', end='')
				plot_avg_response_against_length_of_posting_list(inverted_index)
				print("Done\n")

			elif option == 5:
				break
			else:
				print('\nCHOOSE A VALID OPTION')

			# print(inverted_index)
			# print(next_phrase_occurrance(inverted_index, ['the', 'indian', 'team'], 1, 250))

			'''
			Saving the cache for later use
			'''
			np.save("cache", cache)

		print('\n----------------------END OF PROGRAM----------------------\n')

	except KeyboardInterrupt:
		print('\n----------------------END OF PROGRAM----------------------\n')