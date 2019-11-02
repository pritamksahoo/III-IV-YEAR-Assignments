keyboard = 	[['q', '#', 'w', '#', 'e', '#', 'r', '#', 't', '#', 'y', '#', 'u', '#', 'i', '#', 'o', '#', 'p'],
			['#', 'a', '#', 's', '#', 'd', '#', 'f', '#', 'g', '#', 'h', '#', 'j', '#', 'k', '#', 'l', '#'],
			['#', '#', 'z', '#', 'x', '#', 'c', '#', 'v', '#', 'b', '#', 'n', '#', 'm', '#', '#', '#', '#']]

i_cost, rm_cost = 1, 1

def rp_cost(ch1, ch2, key_dict):
	'''Calculate replacement cost'''
	loc1, loc2 = key_dict[ch1], key_dict[ch2]
	diff_x, diff_y = abs(loc1[0] - loc2[0]), abs(loc1[1] - loc2[1])

	if diff_x == 0:
		diff_y = diff_y - 1

	elif diff_y == 0:
		diff_x = diff_x - 1

	return max(diff_x, diff_y)

def min_mat_ind(m):
	'''Return index with minimum value'''
	ret_ind = 0

	if m[ret_ind] > m[1]:
		ret_ind = 1

	if m[ret_ind] > m[2]:
		ret_ind = 2

	return ret_ind


if __name__ == '__main__':

	'''Remembering location of all keys on keyboard'''
	key_dict = {}

	row_len = len(keyboard[0])
	for i in range(3):
		for j in range(row_len):
			if keyboard[i][j] != '#':
				key_dict[keyboard[i][j]] = (i,j)

	# String input
	s1, s2 = input(), input()
	len1, len2 = len(s1), len(s2)

	'''[insert, remove, replacement, min of all, [from where minimum came from]]'''
	mat = [[[0, 0, 0, 0, [0, 0]] for j in range(len2+1)] for i in range(len1+1)]

	# Initialization
	mat[0][0] = [0, 0, 0, 0, [0, 0]]

	for i in range(1, len1+1):
		mat[i][0] = [i, i, i, i, [i-1, 0]]

	for j in range(1, len2+1):
		mat[0][j] = [j, j, j, j, [0, j-1]]

	# Calculating minimum edit distance
	for i in range(1, len1+1):
		for j in range(1, len2+1):
			if s1[i-1] == s2[j-1]:
				mat[i][j][0] = i_cost + mat[i][j-1][3]
				mat[i][j][1] = rm_cost + mat[i-1][j][3]
				mat[i][j][2] = mat[i-1][j-1][3]

			else:
				mat[i][j][0] = i_cost + mat[i][j-1][3]
				mat[i][j][1] = rm_cost + mat[i-1][j][3]
				mat[i][j][2] = rp_cost(s1[i-1], s2[j-1], key_dict) + mat[i-1][j-1][3]

			min_ind = min_mat_ind(mat[i][j])

			if min_ind == 0:
				mat[i][j][3] = mat[i][j][min_ind]
				mat[i][j][4] = [i, j-1]

			elif min_ind == 1:
				mat[i][j][3] = mat[i][j][min_ind]
				mat[i][j][4] = [i-1, j]

			else:
				mat[i][j][3] = mat[i][j][min_ind]
				mat[i][j][4] = [i-1, j-1]

	print("\nEdit distance : ", mat[len1][len2][3])

	# Printing all the optimal moves
	print("\nPrinting Optimal moves for converting", s1, "to", s2, "( From the end ) :\n")
	x, y = len1, len2

	while x != 0 and y != 0:
		prev_x, prev_y = mat[x][y][4]

		if prev_x == x-1 and prev_y == y-1:
			if s1[x-1] == s2[y-1]:
				print("Keep", s1[x-1])
			else:
				print("Replace", s1[x-1], "with", s2[y-1])

		elif prev_x == x-1:
			print("Remove", s1[x-1])

		else:
			print("Insert", s2[y-1])

		x, y = prev_x, prev_y

	print()