import spacy
from collections import defaultdict, Counter
import re
import numpy as np
import math

no_files_in_corpus = 3
no_topics_in_corpus = 2

STOP_WORDS = ['in', 'and', 'or', 'be', 'the', 'a', 'an', "-PRON-"]

def tokenize(text, term_collection = None):
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
			pass

	if term_collection is not None:
		for t in tokens:
			term_collection.append(t)

		return tokens

	else:
		return tokens

	'''END'''


def build_corpus():
	'''
	Building corpus as term_collection
	'''
	term_collection, all_tokens = [], []

	'''
	Collecting all terms present in the collection
	'''
	print("\nProcessing the documents in corpus (Collecting all terms) . . . ", end = '')
	for i in range(1,no_files_in_corpus+1):
		with open('doc' + str(i) + '.txt', 'r') as f:
			text = f.read()

			'''Storing document-wise and in-total at one time'''
			all_tokens.append(tokenize(text, term_collection))

	# Sorting the terms lexicographically and make it a dictionary
	term_collection = sorted(list(set(term_collection)))
	term_collection = {term : index for index, term in enumerate(term_collection)}

	'''
	Building term-document incedence matrix
	'''
	corpus = [[0 for j in range(no_files_in_corpus)] for i in range(len(term_collection))]

	for doc_index, doc_tokens in enumerate(all_tokens):
		for token in doc_tokens:
			row_index, col_index = term_collection[token], doc_index

			corpus[row_index][col_index] = corpus[row_index][col_index] + 1

	'''
	END
	'''
	print("Done")

	return corpus, term_collection


def rebuild_query(query, U, S):
	'''
	Reform the query according to reduced dimension
	'''
	query = np.dot(query.T, np.dot(U, np.linalg.inv(S)))

	return query


def reduce_rank(corpus, rank):
	'''
	Reduce the rank of matrix into no. of different topics in corpus
	'''
	u, s, vT = np.linalg.svd(corpus, full_matrices=True)
	# print(u.shape, s.shape, vT.shape)
	s = np.diag(s)

	# Slicing all the matrices to reduce rank
	mod_u = u[:, :rank]
	mod_vT = vT[:rank, :]
	mod_s = s[:rank, :rank]

	# Rebuilding the td incedence matrix
	corpus = mod_vT.T

	# cor = np.dot(mod_u, np.dot(mod_s, mod_vT))
	# for c in cor:
	# 	print(c)

	'''END'''
	return corpus, mod_u, mod_s


def find_doc_accord_to_query(query, corpus):
	'''
	Cosine similarity b/w query and document
	'''
	ranked_docs = []

	for i in range(no_files_in_corpus):
		doc = corpus[i]

		mult = np.dot(query, doc)
		norm = sum([comp**2 for comp in doc])**(0.5)

		ranked_docs.append(mult/norm)

	'''END'''

	return ranked_docs


if __name__ == '__main__':
	'''
	START
	'''
	corpus, term_collection = build_corpus()
	# print(term_collection)
	# for c in corpus:
	# 	print(c)

	'''td incedence matrix'''
	corpus = np.array(corpus)

	'''
	SVD of matrix
	'''
	corpus, U, S = reduce_rank(corpus, no_topics_in_corpus)

	# QUERY
	query = "gold silver truck"
	token = tokenize(query)

	query = [0 for i in range(len(term_collection))]
	for t in token:
		index = term_collection.get(t, None)

		if index is not None:
			query[index] = query[index] + 1

	'''
	Rebuild the query
	'''
	query = np.array(query)
	query = rebuild_query(query, U, S)

	# Find ranked documents in corpus according to query
	ranked_docs = find_doc_accord_to_query(query, corpus)

	ranked_docs = [[val, ind] for ind, val in enumerate(ranked_docs)]
	ranked_docs = sorted(ranked_docs, key=lambda x: x[0], reverse=True)

	print('\nRanked Documents - ')
	for ind, docs in enumerate(ranked_docs):
		print("\n" + str(ind+1) + ")", "Doc", str(docs[1]+1), '( Score -', docs[0], ')', end=' ')

	print('\n')


'''
EXAMPLE TAKEN FROM : 
http://www1.se.cuhk.edu.hk/~seem5680/lecture/LSI-Eg.pdf
'''