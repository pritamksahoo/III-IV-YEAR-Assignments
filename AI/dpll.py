def make_clause(clause, line, count_dict, line_no, unit_clause):
	'''
	Storing the propositional clauses
	'''
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

	clause[line_no] = new_clause

	'''
	Chaecking whether unit clause or not
	'''
	if len(proposition) == 1:
		unit_clause.append(line_no)


def assign_value(clause_list, proposition_count, unit_clause, var, assign, deletion, removal):
	'''
	Assigning the value to a propositional variable and perform changes in clauses
	and keeping the record of doing that
	'''
	ret = False
	'''Assigning and updating'''
	clause_key_list = list(clause_list.keys())

	for clause_key in clause_key_list:
		clause = clause_list[clause_key]

		sign = clause.get(var, None)
		if sign is not None:
			'''Same sense'''
			if sign == assign:
				print("Delete clause #" + str(clause_key))
				clause_list.pop(clause_key)
				'''Keeping the record of the clause being deleted'''
				deletion[clause_key] = clause
				'''Updating the count of occurrence of propositional variables'''
				for k in clause:
					v, s = k, clause[k]
					l = proposition_count[v]

					if s == 1:
						l[0] = l[0] - 1
					else:
						l[1] = l[1] - 1

					proposition_count[v] = l

				'''Removing dangling unit clause'''
				if len(clause) == 1:
					try:
						unit_clause.remove(clause_key)
					except:
						pass

			elif (sign + assign) == 0:
				'''Opposite sense'''
				'''Deleting the unnecessary variable from the clause and keeping that record'''
				print("Remove var '" + var + "' from clause #" + str(clause_key))
				clause.pop(var)
				clause_list[clause_key] = clause
				removal.append(clause_key)

				l = proposition_count[var]
				if sign == 1:
					l[0] = l[0] - 1
				else:
					l[1] = l[1] - 1

				proposition_count[var] = l

				'''Checking whether any unit clause is created'''
				if len(clause) == 1:
					unit_clause.append(clause_key)
					ret = True

	return ret


def revert_assignment(clause_list, proposition_count, unit_clause, var, assign, deletion, removal, unit):
	'''
	Reverting back whatever was assigned in the current stage
	'''
	for del_key in deletion:
		print("Adding clause #" + str(del_key))
		clause = deletion[del_key]

		'''Adding the deleted clauses back anf updating the count of occurrence of variables'''
		clause_list[del_key] = clause
		for k in clause:
			v, s = k, clause[k]
			l = proposition_count[v]

			if s == 1:
				l[0] = l[0] + 1
			else:
				l[1] = l[1] + 1

			proposition_count[v] = l

		if len(clause) == 1:
			unit_clause.append(del_key)

	'''Adding the deleted variable back to their clauses and also updating their count'''
	sign = (-1)*assign
	for clause_key in removal:
		print("Adding var '" + var + "' to clause #" + str(clause_key))
		clause_list[clause_key][var] = sign

		l = proposition_count[var]
		if sign == 1:
			l[0] = l[0] + 1
		else:
			l[1] = l[1] + 1

		proposition_count[var] = l

	'''If any unit clause was created, remove it'''
	if unit == True:
		unit_clause.pop(-1)


def dpll(clause_list, proposition_count, unit_clause):
	'''
	dpll algorithm
	return True if clause_list becomes True for certain combination of assignments to variables
	'''
	if len(clause_list) == 0:
		return True

	elif len(list(filter(lambda x: x==0, [len(clause_list[key]) for key in clause_list]))) != 0:
		return False

	else:
		var, assign = None, None
		'''
		Evaluating which variable should we assign a value and what value via heuristic
		'''
		if len(unit_clause) != 0:
			el = unit_clause.pop(0)

			var = list(clause_list[el].keys())[0]
			assign = clause_list[el][var]
		else:
			p_l = [(key, proposition_count[key][0], proposition_count[key][1]) for key in proposition_count]
			p_l = sorted(p_l, key=lambda x: x[1]+x[2], reverse=True)

			pick = p_l[0]
			var = pick[0]
			assign = 1 if pick[1] >= pick[2] else -1

		'''
		Assigning the value
		'''
		print("\n--------------------------------------\n")
		print("Assigning '" + var + "' = " + str(assign) + " : \n")
		deletion, removal, unit = {}, [], False
		unit = assign_value(clause_list, proposition_count, unit_clause, var, assign, deletion, removal)
		
		'''Preceeding to next phase'''
		effect = dpll(clause_list, proposition_count, unit_clause)

		if effect == True:
			'''Assignment has been found for which dpll becomes True...Job Done'''
			return True

		else:
			'''Dpll becomes false for current assignment combination...Try another'''
			print("\n--------------------------------------\n")
			print("Result False, So, Reverting '" + var + "' = " + str(assign) + " : \n")
			revert_assignment(clause_list, proposition_count, unit_clause, var, assign, deletion, removal, unit)
			'''Changing the value assigned'''
			assign = (-1)*assign

			deletion, removal, unit = {}, [], False
			'''Assigningment with new combination'''
			print("\n--------------------------------------\n")
			print("Assigning '" + var + "' = " + str(assign) + " : \n")
			unit = assign_value(clause_list, proposition_count, unit_clause, var, assign, deletion, removal)
			'''Preceeding to next phase'''
			effect_1 = dpll(clause_list, proposition_count, unit_clause)

			if effect_1 == True:
				'''Assignment has been found for which dpll becomes True...Job Done'''
				return True

			else:
				'''Dpll becomes false for current assignment combination...Try another'''
				print("\n--------------------------------------\n")
				print("Result False, So, Reverting '" + var + "' = " + str(assign) + " : \n")
				revert_assignment(clause_list, proposition_count, unit_clause, var, assign, deletion, removal, unit)
				print("\n--------------------------------------\n")
				print("NO AVAILABLE OPTIONS, BACKTRACK")
				return False



if __name__ == '__main__':
	clause_list = {}
	proposition_count = {}
	unit_clause = []

	line, line_no = input(), 0
	while line != "/":
		make_clause(clause_list, line, proposition_count, line_no, unit_clause)
		line_no = line_no + 1

		line = input()

	print("\nQuestion : \n")

	print("CLAUSES : ", clause_list)
	# print(proposition_count)
	# print(unit_clause)

	print()
	print("Solution : ")
	'''
	DPLL
	'''
	result = dpll(clause_list, proposition_count, unit_clause)

	print("\n--------------------------------------\n")
	if result:
		print("Result = " + str(result) + " (Not Entailed)\n")
	else:
		print("Result = " + str(result) + " (Entailed)\n")