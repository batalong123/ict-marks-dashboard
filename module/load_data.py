import pandas as pd


def get_data():
	data = pd.read_excel('data/Note_des_classes_6e_5e.xlsx')
	data['average_marks'] = round(data['average_marks'], 2)
	return data

data = get_data()