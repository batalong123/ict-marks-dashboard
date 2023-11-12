import streamlit as st 
import numpy as np
import pandas as pd
from module.load_data import data
from scipy import stats



def create_data(data:pd.DataFrame) -> pd.DataFrame:
	df = pd.DataFrame({"trimester 1": round((data['seq 1']+data['seq 2'])/2, 2),  
		"trimester 2": round((data['seq 3']+data['seq 4'])/2, 2),
		"trimester 3": round((data['seq 5']+data['seq 6'])/2, 2),
		"age":data["age"]})
	return df

def subdata(data:pd.DataFrame, items:list) -> pd.DataFrame:
	if len(items) == 3:
		return data[(data[items[0][0]] == items[0][1]) & (data[items[1][0]] == items[1][1]) & (data[items[2][0]] == items[2][1])]['average_marks']

	if len(items) == 2:
		return data[(data[items[0][0]] == items[0][1]) & (data[items[1][0]] == items[1][1])]['average_marks']

	if len(items) == 1:
			return data[(data[items[0][0]] == items[0][1])]['average_marks']
			

def hypothesis_testing(group1:pd.DataFrame, group2:pd.DataFrame, label1:list, label2:list) -> list:

	mean1, std1, nobs1 = group1.mean(), group1.std(), group1.count()
	mean2, std2, nobs2 = group2.mean(), group2.std(), group2.count()

	res = stats.ttest_ind_from_stats(mean1=mean1, std1=std1, nobs1=nobs1, 
		mean2=mean2, std2=std2, nobs2=nobs2,equal_var=False)

	tvalue = res.statistic
	pvalue = res.pvalue 

	diff = mean1 - mean2
	std_error = np.sqrt((std1**2/nobs1) + (std2**2/nobs2))
	low_bound   = diff - tvalue*std_error
	upper_bound = diff + tvalue*std_error

	text1 = f"""
	:green[**Welch two-sample t-test**]

	**data**: group1={label1} and group2={label2}

	t = {tvalue:.4f}, diff = {diff:.4f}, p-value = {pvalue:.4f}

	**alternative hypothesis**: true difference in means is not equal to 0

	**95% confidence interval**: ({low_bound}, {upper_bound})

	**mean of group1**: {mean1:.3f}

	**mean of group2**: {mean2:.3f}
	"""

	text2 = f"""
	:green[**Welch two-sample t-test**]

	**data**: group1={label1} and group2={label2}

	t = {tvalue:.8f}, diff = {diff:.8f}, p-value = {pvalue:.8f}

	**null hypothesis**: true difference in means is equal to 0

	**mean of group1**: {mean1:.3f}

	**mean of group2**: {mean2:.3f}
	"""

	return text1 if pvalue < 0.05 else text2



def eda():
	df = pd.DataFrame({"trimester 1": round((data['seq 1']+data['seq 2'])/2, 2),  
		"trimester 2": round((data['seq 3']+data['seq 4'])/2, 2),
		"trimester 3": round((data['seq 5']+data['seq 6'])/2, 2),
		"age":data["age"]})
	corr = df.corr()

	vif  = np.linalg.inv(corr.to_numpy()).diagonal()
	vifs = pd.Series(np.round(vif,2), index=df.columns.tolist(), name="VIF") 

	female = data[data.gender == 'F']
	male   = data[data.gender == 'M']

	df_female = create_data(female)
	df_male = create_data(male)

	items = ['F','M','6e','5e']


	st.subheader('Sequence')
	placeholder1 = st.empty()
	
	with placeholder1.container():
		col1, col2 = st.columns(2)
		col1.caption(':red[**Descriptive statistics**]')
		col1.dataframe(round(data.describe(), 2))
		col2.caption(':red[**Correlation**]')
		col2.dataframe(round(data.corr(), 2))

	st.subheader("Trimester")
	st.caption(':red[**Descriptive statistics**]')
	st.dataframe(round(df.describe(), 2), use_container_width=True)
	placeholder2 = st.empty()
	with placeholder2.container():
		col1, col2 = st.columns(2)
		col1.caption(':red[**Correlation**]')
		col1.dataframe(round(corr, 2))
		col2.caption(':red[**Variance Inflation Factor**]')
		col2.dataframe(vifs)

	with st.expander("👁 Read more"):
		st.markdown(""" 
			> 1. :orange[Descriptive statistics] help to define mean, standard deviation, minimun, maximun, median, etc.. 
			such that we can summarize the dataset and discover the patterns.
			> 2. :orange[Correlation] help to find the tendance or colinearity between two or more attributes in the dataset. 
			> 3. :orange[VIF] is a mesure of colinearity among predictor variables within a multiple regression. 
			>> 1. If outcome is 1, it's okay.
			>> 2. If it is between 1 and 5, it show low to average colinearity, and above 5 generally means highly redundant
			and variable should be dropped. 
			""")

	st.subheader('Sequence by gender')
	placeholder3 = st.empty()
	placeholder4 = st.empty()
	with placeholder3.container():
		col1, col2 = st.columns(2)
		col1.caption(':orange[**Descriptive statistics: Female**]')
		col1.dataframe(round(female.describe(), 2))
		col2.caption(':orange[**Descriptive statistics: Male**]')
		col2.dataframe(round(male.describe(), 2))

	with placeholder4.container():
		col1, col2 = st.columns(2)
		col1.caption(':orange[**Correlation: Female**]')
		col1.dataframe(round(female.corr(), 2))
		col2.caption(':orange[**Correlation: Male**]')
		col2.dataframe(round(male.corr(), 2))

	st.subheader('Trimester by gender')
	placeholder5 = st.empty()
	placeholder6 = st.empty()
	with placeholder5.container():
		col1, col2 = st.columns(2)
		col1.caption(':orange[**Descriptive statistics: Female**]')
		col1.dataframe(round(df_female.describe(), 2))
		col2.caption(':orange[**Descriptive statistics: Male**]')
		col2.dataframe(round(df_male.describe(), 2))

	with placeholder6.container():
		col1, col2 = st.columns(2)
		col1.caption(':orange[**Correlation: Female**]')
		col1.dataframe(round(df_female.corr(), 2))
		col2.caption(':orange[**Correlation: Male**]')
		col2.dataframe(round(df_male.corr(), 2))

	st.subheader('Assumption')
	st.markdown("""
		In this section, you can make your assumption to know which group is best than other group in this ICT course.
		For example: According to table trimester evaluation by gender, we have two groups (female students and male students). 

		By the observation, 
		> **Is it true that female students are best than male students in the ICT course for Tebap college?**  

		This question we allow us to compare the general annual class average (mean) for one group to other group. That's lead to 
		compute the difference between the two means. We have two hypothesis:

		1. **Null hypothesis:** :blue[ true difference in means is equal to 0].

		2. **Alternative hypothesis:** :blue[ true difference in means is not equal to 0]

		**NB**: difference = $\mu$(group1) - $\mu$(group2)

		We choose the right hypothesis as follows:
		- **if p-value < 5% then we reject null hypothesis**
		- **if p-value > 5% then we accept null hypothesis**
		""")
	placeholder7 = st.empty()
	with placeholder7.container():
		col1, col2 = st.columns(2)
		
		with col1:
			label1 = []
			st.caption(':red[Create group A]')
			scol1, scol2, scol3 = st.columns(3)
			
			gender1 = scol1.selectbox('Gender', ['Choose an option', 'F', 'M'])
			form1    = scol2.selectbox('Form',  ['Choose an option', '6e', '5e'])
			age1 = scol3.selectbox('Age', ['Choose an option',]+sorted(data.age.unique().tolist()))

			if gender1 != 'Choose an option':
				label1.append(('gender', gender1))
			if form1 != 'Choose an option':
				label1.append(('form', form1))
			if age1 != 'Choose an option':
				label1.append(('age', age1))
			
			group1 = subdata(data, label1)
			if type(group1) == pd.Series:
				scol2.write(group1)
			

		with col2:
			label2 = []
			st.caption(':red[Create group B]')
			tcol1, tcol2, tcol3 = st.columns(3)
			
			gender2 = tcol1.selectbox('Gender', ['Choose an option', 'F', 'M'], key=1)
			form2    = tcol2.selectbox('Form',  ['Choose an option', '6e', '5e'], key=2)
			age2 = tcol3.selectbox('Age', ['Choose an option',]+sorted(data.age.unique().tolist()), key=3)

			if gender2 != 'Choose an option':
				label2.append(('gender', gender2))
			if form2 != 'Choose an option':
				label2.append(('form', form2))
			if age2 != 'Choose an option':
				label2.append(('age', age2))
			
			group2 = subdata(data, label2)
			if type(group2) == pd.Series:
				tcol2.write(group2)

		st.caption('Choose only one or two item(s) per group. For example group A = (F, 5e) or group B = (M)')

		if (sorted(label2) == sorted(label1)) and not(len(label1) == 0 or len(label2) == 0):
			st.info(f'You cannot create two different groups with same items: label1 = {label1} & label2 = {label2}.')


		if st.button('t-test'):
			res = hypothesis_testing(group1, group2, label1, label2)
			st.write(res)

		





