import pickle


if __name__ == '__main__':
	f = open("active.pkl", "wb")
	pickle.dump({}, f)
	f.close()

	f = open("resource.pkl", "wb")
	rec = {
		1: {"total": 2, "available": 2, "holder": []},
		2: {"total": 1, "available": 1, "holder": []}
	}
	pickle.dump(rec, f)
	f.close()