import numpy as np

def print_hmm_probability(all_possibility, no_states, seq, hmm_prob):
	temp_all_possibility = all_possibility.copy()
	tot_prob = 0.0

	for s, prob in temp_all_possibility:
		tot_prob = tot_prob + prob

	for index in range(len(temp_all_possibility)):
		temp_all_possibility[index][1] = temp_all_possibility[index][1] / tot_prob

	for state in range(no_states):
		for sq in range(len(seq)):
			filter_prob = list(filter(lambda x: x[0][sq] == state, temp_all_possibility))

			sum_prob = 0.0
			for s, prob in filter_prob:
				sum_prob = sum_prob + prob

			hmm_prob[state].append(sum_prob)


def recur_possibility(all_possibility, state, state_array, obs_array, pi_array, seq, no_states, cur_obs):
	if cur_obs == len(seq):
		# Calc probability
		prob = pi_array[state[0]] * obs_array[state[0]][int(seq[0])]

		for i in range(1, len(seq)):
			prob = prob * state_array[state[i-1]][state[i]] * obs_array[state[i]][int(seq[i])]

		all_possibility.append([state, prob])

	else:

		for st in range(no_states):
			cur_state = state.copy()
			cur_state.append(st)

			recur_possibility(all_possibility, cur_state, state_array, obs_array, pi_array, seq, no_states, cur_obs+1)


def create_hmm_table(state_array, obs_array, pi_array, seq, no_states):
	all_possibility = []
	state = []

	recur_possibility(all_possibility, state, state_array, obs_array, pi_array, seq, no_states, 0)
	return all_possibility


if __name__ == '__main__':

	#Taking I/P
	no_states = int(input("Enter number of states: "))
	no_obs = int(input("Enter number of observation: "))

	#Intializing Arrays
	state_array = np.zeros((no_states, no_states))
	obs_array = np.zeros((no_states, no_obs))
	pi_array = np.zeros((no_states))

	#Matrix I/P
	print("Enter the state array values:")
	for i in range(no_states):
		for j in range(no_states):
			state_array[i][j] = float(input())

	#print(state_array)
	print("Enter the observation array values:")
	for i in range(no_states):
		for j in range(no_obs):
			obs_array[i][j] = float(input())

	print("Enter the PI matrix values:")
	for i in range(no_states):
		pi_array[i]=float(input())

	#Sequnece I/P
	seq = input(("Enter the obs sequence:"))

	# print('\n',state_array,'\n\n', obs_array,'\n\n', pi_array, '\n')
	print("\n\n--------------------------------------------\nState sequence probabilities : \n")
	print("   Sequence               Probability")

	all_possibility = create_hmm_table(state_array, obs_array, pi_array, seq, no_states)
	# print(all_possibility)

	for pos, prob in all_possibility:
		print(pos, "-", prob)

	print("\n--------------------------------------------\nHMM Probabilities : \n")

	hmm_prob = [[], []]
	print_hmm_probability(all_possibility, no_states, seq, hmm_prob)

	for index, state in enumerate(hmm_prob):
		print("P(" + str(index) + ") :- ", end='')
		print(state) 

	print("--------------------------------------------\n")
	# #Creating Alpha table
	# alpha_table = np.zeros((len(seq),no_states))

	# #intializing first Row using PI
	# for i in range(no_states):
	# 	alpha_table[0][i] = pi_array[i]*obs_array[i][int(seq[0])]
	# print(alpha_table)
	# #Calculating other entries
	# for i in range(1,len(seq)):
	# 	for j in range(no_states):
	# 		alpha_table[i][j]=0
	# 		for k in range(no_states):
	# 			#print(alpha_table[i-1][k],obs_array[k][int(seq[i])],state_array[k][j])
	# 			alpha_table[i][j]=alpha_table[i][j]+alpha_table[i-1][k]*obs_array[j][int(seq[i])]*state_array[k][j]

	# print('Alpha Table:')
	# print(alpha_table)

	# #Calculating Beta table
	# beta_table=np.zeros((len(seq),no_states))

	# #Initialzing Beta Table
	# for i in range(no_states):
	# 	beta_table[len(seq)-1][i]=1
	# #Claculating other enteries
	# for i in range(len(seq)-2,-1,-1):
	# 	for j in range(no_states):
	# 		for k in range(no_states):
	# 			beta_table[i][j]=beta_table[i][j]+beta_table[i+1][k]*state_array[j][k]*obs_array[k][int(seq[i+1])]

	# print('Beta Table')
	# print(beta_table)

	# #Creating Gamma Table
	# gamma_table=np.zeros((len(seq),no_states))
	# #deno
	# deno=0
	# for i in range(no_states):
	# 	deno=alpha_table[len(seq)-1][i]+deno

	# gamma_table=np.multiply(alpha_table,beta_table)

	# gamma_table=gamma_table / deno

	# print('Gamma Table')
	# print(gamma_table)