def make_clause(clause, line, count_dict):
	proposition = line.split()
	new_clause = dict()

	for p in proposition:
		elem, sign = None, None

		if p[0] == '!':
			elem = p[1]
			sign = -1
		else:
			elem = p
			sign = 1

		new_clause[elem] = sign

		'''
		Incrementing count of propositional variable
		'''
		if count_dict.get(elem, None) is None:
			count_dict[elem] = [0, 0]

		count_list = count_dict[elem]
		if sign == 1:
			count_list[0] = count_list[0] + 1
		else:
			count_list[1] = count_list[1] + 1

		count_dict[elem] = count_list

	clause.append(new_clause)


if __name__ == '__main__':
	clause_list = []
	proposition_count = {}

	line = input()
	while line != "/":
		make_clause(clause_list, line, proposition_count)

		line = input()

	print(clause_list)
	print(proposition_count)