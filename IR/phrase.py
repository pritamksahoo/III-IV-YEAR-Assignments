import numpy as np
import re

text = None

with open('phrase_len_2.txt', 'r') as f:
	text = f.read()

split_chars = [" ", "\n", "\-", ",", "\.", "\"", "\(", "\)", "\?", "\[", "\]", "\*", ";", "\\", "/"]

delimiter = '|'.join(split_chars)

tokens = re.split(delimiter, text)

try:
	while True:
		tokens.remove("")
except Exception as e:
	pass

while len(tokens) != 0:
	length = np.random.randint(2,7)

	if length < len(tokens):
		phrase = ' '.join(tokens[:length])

		with open("phrase_len_2.txt", "a") as myfile:
			myfile.write(phrase + '\n')

		tokens = tokens[length:]

	else:
		break