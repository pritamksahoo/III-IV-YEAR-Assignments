import numpy as np
from matplotlib import pyplot as plt

if __name__ == '__main__':
	# no_doc : No. of documents retreived
	no_doc = int(input())
	# threshold : Probability of a document being relevant
	threshold = float(input())
	# Non-retreived relevant documents
	not_retreived_r_doc = int(input())
	# Record of relevancy
	doc_r_nr = []

	'''Initializing total no. of relevant documents'''
	r_doc = not_retreived_r_doc

	'''Random relevant and non-relevant judjement'''
	for i in range(no_doc):
		rand = np.random.random()

		if rand <= threshold:
			doc_r_nr.append('R')
			r_doc = r_doc + 1

		else:
			doc_r_nr.append('NR')

	precision, recall = [], []

	relevant_so_far = 0

	# Calculating precision and recall
	for ind, val in enumerate(doc_r_nr):
		if val == 'R':
			relevant_so_far = relevant_so_far + 1

		precision.append(relevant_so_far / (ind+1))
		recall.append(relevant_so_far / r_doc)

	# Plotting precision-recall curve
	plt.plot(recall, precision, color='blue', label='Saw-tooth p-r curve')
	plt.xlabel("Recall")
	plt.ylabel("Precision")
	plt.legend()
	plt.show()