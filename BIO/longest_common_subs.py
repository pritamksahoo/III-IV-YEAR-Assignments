def find_longest_prefix(string1, string2):
	ind, len1, len2 = 0, len(string1), len(string2)

	while ind < len1 and ind < len2:
		if string1[ind] == string2[ind]:
			ind = ind + 1
		else:
			break

	return string1[:ind]


def find_longest_substring(string_list):
	start, end, temp_char = 0, 0, [string_list[0][-1]]
	longest_substring, max_len = [], 0

	length = len(string_list)

	while end < length:
		if len(set(temp_char)) == 3:
			substring = find_longest_prefix(string_list[start], string_list[end])

			if len(substring) == max_len:
				longest_substring.append(substring)

			elif len(substring) > max_len:
				longest_substring = [substring]
				max_len = len(substring)

			start = start + 1
			temp_char.remove(string_list[start-1][-1])

		else:
			end = end + 1
			if end < length:
				temp_char.append(string_list[end][-1])

	return longest_substring


if __name__ == '__main__':
	s1, s2, s3 = input(), input(), input()

	s1, s2, s3 = s1 + '#', s2 + '$', s3 + '@'

	suffixes = []

	for i in range(len(s1)-1):
		suffixes.append(s1[i:])

	for i in range(len(s2)-1):
		suffixes.append(s2[i:])

	for i in range(len(s3)-1):
		suffixes.append(s3[i:])

	suffixes = sorted(suffixes)

	longest_sub_list = find_longest_substring(suffixes)

	print("\nLongest common substring(s) is(are) : \n")
	print(' | '.join(longest_sub_list))
	print()