def evaluate(board):
	for row in range(0, 3):
		if board[row][0] == board[row][1] and board[row][1] == board[row][2]:  
			if board[row][0] == 'x': 
				return 10 
			elif board[row][0] == 'o':  
				return -10

	# Checking for Columns for X or O victory.  
	for col in range(0, 3):
		if board[0][col] == board[1][col] and board[1][col] == board[2][col]:  
			if board[0][col]=='x': 
				return 10 
			elif board[0][col] == 'o':  
				return -10

	# Checking for Diagonals for X or O victory.  
	if board[0][0] == board[1][1] and board[1][1] == board[2][2]:
		if board[0][0] == 'x':  
			return 10 
		elif board[0][0] == 'o':  
			return -10 

	if board[0][2] == board[1][1] and board[1][1] == board[2][0]:
		if board[0][2] == 'x':  
			return 10 
		elif board[0][2] == 'o':  
			return -10 
		
	return 0

def minimax(board, depth, is_max, alpha, beta):
	val = evaluate(board)

	if val == 10:
		return val-depth
	elif val == -10:
		return val+depth
	elif len(list(filter(lambda x: x == '-', board[0]+board[1]+board[2]))) == 0:
		return 0

	else:
		if is_max:
			max_val = -1000
			for i in range(3):
				for j in range(3):
					if board[i][j] == '-':
						board[i][j] = 'x'

						val = minimax(board, depth+1, not is_max, alpha, beta)
						max_val = max(max_val, val)
						alpha = max(alpha, max_val)

						board[i][j] = '-'

						if beta <= alpha:
							return max_val

			return max_val

		else:
			min_val = 1000
			for i in range(3):
				for j in range(3):
					if board[i][j] == '-':
						board[i][j] = 'o'

						val = minimax(board, depth+1, not is_max, alpha, beta)
						min_val = min(min_val, val)
						beta = min(beta, min_val)

						board[i][j] = '-'

						if beta <= alpha:
							return min_val

			return min_val

def find_best_move(board, is_max, alpha, beta):
	best_val, row, col = -1000 if is_max else 1000, -1, -1

	for i in range(3):
		for j in range(3):
			if board[i][j] == '-':
				board[i][j] = 'x' if is_max == True else 'o'

				val = minimax(board, 0, not is_max, alpha, beta)

				if is_max and best_val < val:
					best_val = val
					alpha = max(alpha, best_val)
					row, col = i, j

				elif not is_max and best_val > val:
					best_val = val
					row, col = i, j

				board[i][j] = '-'

			if beta <= alpha:
				break

		if beta <= alpha:
			break

	board[row][col] = 'x' if is_max else 'o'

if __name__ == '__main__':
	board = []
	print("Enter current state of Tic Tac Toe (player - 'x', opponent - 'o', empty - '-')")
	for i in range(3):
		board.append(list(input()))

	chance = input("Whose move is this? ('x' or 'o') : ")
	is_max = True if chance == 'x' else False
	alpha, beta = -1000, 1000

	find_best_move(board, is_max, alpha, beta)

	print('\n'.join(list(map(lambda x: ' '.join(x), board))))