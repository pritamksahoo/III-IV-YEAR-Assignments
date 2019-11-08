import spacy
from collections import defaultdict, Counter
import re
import numpy as np
import math


no_files_in_corpus = 1
STOP_WORDS = ['in', 'and', 'or', 'be', 'the', 'a', 'an', "-PRON-"]
INT_MAX = 2147483647


class BST: 
	def __init__(self, key): 
		self.left = None
		self.right = None
		self.val = key 


def insert_bst(root, node): 
	if root is None: 
		root = node

	elif root.val == "-1":
		root.val = node.val

	else: 
		if root.val < node.val: 
			if root.right is None: 
				root.right = node 
			else: 
				insert_bst(root.right, node) 
		else: 
			if root.left is None: 
				root.left = node 
			else: 
				insert_bst(root.left, node)

	return root


def inorder_trv(root):
	if root: 
		inorder_trv(root.left) 
		print(root.val) 
		inorder_trv(root.right)


def tokenize(text, corpus = None):
	'''
	Splitting the text aginst some pre-defined delimiter
	'''
	# nlp model of SpaCy
	nlp = spacy.load('en', disable=['parser', 'ner'])

	'''Tokenization'''
	split_chars = [" ", "\no_terms", "\-", ",", "\.", "\"", "\(", "\)", "\?", "\[", "\]", "\*", ";", "\\", "/"]
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

	if corpus is not None:
		for t in tokens:
			corpus.append(t)

		return corpus

	else:
		return tokens

	'''END'''


def build_corpus():
	'''
	Building corpus
	'''
	corpus = []

	print("\nProcessing the documents in corpus (Collecting terms) . . . ", end = '')
	for i in range(1,no_files_in_corpus+1):
		with open('input' + str(i) + '.txt', 'r') as f:
			text = f.read()
			'''Storing document-wise and in-total at one time'''
			corpus = tokenize(text, corpus)

	counter = Counter(corpus)
	term_freq = [[c, counter[c]] for c in counter]

	term_freq = sorted(term_freq, key=lambda x: (x[0], x[1]))

	print("Done")
	return term_freq
	'''END'''


def build_bst(cost_metric, terms, start, end, root):
	'''Building the tree'''
	if start == end:
		root = insert_bst(root, BST(terms[start]))

	else:
		parent = cost_metric[start][end][1]
		root = insert_bst(root, BST(terms[parent]))
		# print(terms[parent])
		if start <= parent-1:
			build_bst(cost_metric, terms, start, parent-1, root)

		if end >= parent+1:
			build_bst(cost_metric, terms, parent+1, end, root)


def build_optimal_bst(terms, freq):
	'''Preparing to build optimal bst'''
	no_terms = len(terms)

	cost_metric = [[[0,-1] for j in range(no_terms)] for i in range(no_terms)] 

	for i in range(no_terms): 
		cost_metric[i][i] = [freq[i], i]  

	# Optimal Cost Calculation
	for cur_len in range(2, no_terms + 1): 
		for i in range(no_terms - cur_len + 2):
			j = i + cur_len - 1

			if i >= no_terms or j >= no_terms: 
				break

			cost_metric[i][j] = [INT_MAX, i]
			for r in range(i, j + 1):  
				c = 0

				if (r > i): 
					c += cost_metric[i][r - 1][0]
				if (r < j): 
					c += cost_metric[r + 1][j][0]

				c += sum(freq[i:j+1])  
				if (c < cost_metric[i][j][0]): 
					cost_metric[i][j] = [c, r]

	# Building the structure
	root = BST("-1")
	build_bst(cost_metric, terms, 0, no_terms-1, root)

	return root


if __name__ == '__main__':
	tf = build_corpus()

	terms, freq = [], []

	for t, f in tf:
		terms.append(t)
		freq.append(f)

	root = build_optimal_bst(terms, freq)

	inorder_trv(root)