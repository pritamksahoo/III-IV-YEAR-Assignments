import spacy
from collections import defaultdict, Counter
import re
import numpy as np
import math


no_files_in_corpus = 4
STOP_WORDS = ['in', 'and', 'or', 'be', 'the', 'a', 'an', "-PRON-"]

def tokenize(text, vectors = None):
	'''
	Splitting the text aginst some pre-defined delimiter
	'''
	# nlp model of SpaCy
	nlp = spacy.load('en', disable=['parser', 'ner'])

	'''Tokenization'''
	split_chars = [" ", "\n", "\-", ",", "\.", "\"", "\(", "\)", "\?", "\[", "\]", "\*", ";", "\\", "/"]
	delimiter = '|'.join(split_chars)
	tokens = re.split(delimiter, text)

	try:
		while True:
			tokens.remove("")
	except Exception as e:
		pass

	tokens = list(map(lambda x: x.lower(), tokens))

	'''Lemmatization'''
	sentence = " ".join(tokens)
	doc = nlp(sentence)
	tokens = [token.lemma_ for token in doc]

	'''Removing stop-words'''
	for sw in STOP_WORDS:
		try:
			while True:
				tokens.remove(sw)
		except Exception as e:
			e = 0
	# for ind, t in enumerate(tokens):
	# 	w = Word(t)
	# 	w.lemmatize()
	# 	tokens[ind] = str(w)

	if vectors is not None:
		for t in tokens:
			vectors.append(t)

		return tokens

	else:
		return tokens

	'''END'''

def build_vectors():
	'''
	Building corpus as vectors
	'''
	vectors, all_tokens = [], []

	'''
	Representing all terms as dimentions of a vector-space
	'''
	print("\nProcessing the documents in corpus (Collecting terms as vector space dimensions) . . . ", end = '')
	for i in range(1,no_files_in_corpus+1):
		with open('input' + str(i) + '.txt', 'r') as f:
			text = f.read()
			'''Storing document-wise and in-total at one time'''
			all_tokens.append(tokenize(text, vectors))

	vectors = sorted(list(set(vectors)))
	vector = {}

	for dim, term in enumerate(vectors):
		vector[term] = {}
		vector[term]['dim'] = dim
		'''
		Calculating idf
		'''
		doc_freq = 0
		for doc in all_tokens:
			if term in doc:
				doc_freq = doc_freq + 1

		vector[term]['df'] = doc_freq

	print("Done")

	'''
	Representing all documents as vector
	'''
	print("\nRepresenting documents in term of vectors . . . ", end = '')
	corpus = {}

	for i in range(no_files_in_corpus):
		corpus[i] = {}

		record = all_tokens[i]
		counter = Counter(record)

		'''
		Calculating tf-idf weight
		'''
		tf_idf = 0.0
		for c in counter:
			term_vector, tf, idf = vector[c]['dim'], counter[c], vector[c]['df']

			if idf == no_files_in_corpus:
				idf = idf - 1

			tf_idf = tf_idf + (tf * math.log10(idf))**2

		tf_idf = tf_idf**(0.5)

		'''
		Normalized tf-idf
		'''
		for c in counter:
			term_vector, tf, idf = vector[c]['dim'], counter[c], vector[c]['df']

			if idf == no_files_in_corpus:
				idf = idf - 1

			weight = tf * math.log10(no_files_in_corpus/idf)
			corpus[i][term_vector] = weight/tf_idf
	'''
	END
	'''
	print("Done")

	return corpus, vector


def find_doc_accord_to_query(query, corpus, vector):
	'''
	Rank docs according to query
	'''
	token = tokenize(query)
	token = sorted(list(token))

	score = [0.0]*no_files_in_corpus

	for t in token:
		vec_t = vector.get(t, None)
		# print(t, vec_t)
		if vec_t is not None:
			for doc in range(no_files_in_corpus):
				weight = corpus[doc].get(vec_t['dim'], 0.0)
				# print("weight", weight)
				score[doc] = score[doc] + weight

	return score


if __name__ == '__main__':
	'''
	Start
	'''
	corpus, vector = build_vectors()
	# print(corpus, vector)

	print('\nEnter a query : ')
	query = input()
	ranked_docs = find_doc_accord_to_query(query, corpus, vector)
	# print(ranked_docs)

	ranked_docs = [[val, ind] for ind, val in enumerate(ranked_docs)]
	ranked_docs = sorted(ranked_docs, key=lambda x: x[0], reverse=True)

	print('\nRanked Documents - ')
	for ind, docs in enumerate(ranked_docs):
		print("\n" + str(ind) + ")", "Doc", docs[1], '( Score -', docs[0], ')', end=' ')

	print('\n')