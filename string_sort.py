def ascii(ch):
	return ord(ch.lower())-ord('a')+1


def string_sort(arr, length):
	len_array = list(map(len, arr))
	max_len = max(len_array)

	temp1 = [list() for i in range(27)]
	# Considering last character and sort on the basis
	for j in range(length):
		string = arr[j]
		temp1[ascii(string[-1])].append(string)

	# Moving from the last character one by one and sorting on basis of them
	for i in range(1, max_len+1):
		temp2 = [list() for i in range(27)]
		
		for j in range(27):
			for string in temp1[j]:
				if i < len(string):
					temp2[ascii(string[-1-i])].append(string)
				else:
					temp2[j].append(string)

		temp1 = temp2.copy()

	# Finally coping the result to arr
	arr = []
	for j in range(27):
		for string in temp1[j]:
			arr.append(string)

	return arr


if __name__ == '__main__':
	no_str = int(input())
	store = []

	for i in range(no_str):
		store.append(input())

	store = string_sort(store, no_str)

	print('\n'.join(store))