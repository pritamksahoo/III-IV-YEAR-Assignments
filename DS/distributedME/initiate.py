import pickle

f = open("active.pkl", "wb")
pickle.dump({}, f)
f.close()