import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("/home/pks/Downloads/haberman.csv")

try:
	plt.boxplot(df['age'])
	plt.show()
except Exception as e:
	print(e)
