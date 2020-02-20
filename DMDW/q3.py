import numpy as np

def process(mat1, mat2):
	n_mat1, n_mat2 = np.array(mat1), np.array(mat2)

	addition = np.add(n_mat1, n_mat2)

	mult = np.dot(n_mat1, n_mat2)

	print("Addition : ")
	print(addition)

	print("Multiplication : ")
	print(mult)

if __name__ == '__main__':
	row, col = tuple(map(int, input().split()))

	mat1 = [ [ int(input()) for j in range(col) ] for i in range(row) ]
	mat2 = [ [ int(input()) for j in range(col) ] for i in range(row) ]

	process(mat1, mat2)
