import pickle


if __name__ == '__main__':
	f = open("active.pkl", "wb")
	pickle.dump({}, f)
	f.close()