import streamlit as st 
import plotly.express as px
import pandas as pd
from module.load_data import data   
from module.dataset import create_data
import plotly.express as px
from sklearn.tree import DecisionTreeClassifier, export_graphviz
import matplotlib.pyplot as  plt

#plt.style.use('seaborn-dark-palette')

def grades(mark):
	if mark >= 0 and mark < 5:
		return 'U'
	elif  mark >= 5 and mark < 9:
		return 'E'
	elif mark >= 9 and mark < 12:
		return 'D'
	elif mark >= 12 and mark < 15:
		return 'C'
	elif mark >= 15 and mark < 18:
		return 'B'
	else:
		return 'A'

def segmentation(data:pd.DataFrame):
	df = data.copy()
	factor = pd.factorize(df.form)
	df['form'] = factor[0]; definition=factor[1]

	cols = [f'seq {i+1}' for i in range(6)] + ['age','form']
	tree = DecisionTreeClassifier(random_state=31012020)
	tree.fit(df[cols], df['gender'])
	
	export_graphviz(tree, out_file="images/tree.dot", class_names=["Female", "Male"],
		feature_names=cols, impurity=False, filled=True,rounded=True)
	result = pd.DataFrame({"Feature":cols, "Gain":tree.feature_importances_})
	return result

def scatterplot(female=None, male=None, line_separator=None, x_axis=None, y_axis=None):
	fig = plt.figure(figsize=(5,5))
	plt.scatter(female[x_axis], female[y_axis], marker='v', color='red', label="Girl", lw=1.2)
	plt.scatter(male[x_axis], male[y_axis], marker='o', color='blue', label="Boy",lw=1.2)
	plt.xlabel(x_axis); plt.ylabel(y_axis)
	plt.title("Decision line", fontweight="bold")
	for u in  line_separator[0]:
		plt.vlines(line_separator[0], 0, female[y_axis].max(), color="black",
		 linestyles="-.", lw=1.75)

	for v in  line_separator[1] :
		plt.hlines(line_separator[1], -1, female[y_axis].max(), color="black",
		 linestyles="dashed", lw=1.75)

	plt.legend(loc="best", frameon=True, fancybox=True, shadow=True, title="Gender")
	return fig


df_trim = create_data(data)
total_students = len(data)
average_age = data.age.mean()
gca1 = df_trim["trimester 1"].mean()
gca2 = df_trim["trimester 2"].mean()
gca3 = df_trim["trimester 3"].mean()
annual_gca = (gca1+gca2+gca3)/3

evaluations = ['seq 1', 'seq 2','seq 3','seq 4','seq 5','seq 6']

sgca = pd.DataFrame(columns=['Male','Female'], index=evaluations)

sgca['Male'] = data[data.gender == 'M'][evaluations].mean()
sgca['Female'] = data[data.gender == 'F'][evaluations].mean()

form_counts = data.form.value_counts()
gender_counts = data.gender.value_counts()

progression = sgca.diff()

pass_or_fail =pd.DataFrame({seq:data[seq].apply(lambda x: 'Passed' if x >= 10.0 else 'Failed').value_counts().to_dict() for seq in evaluations})   

student_grade =  pd.DataFrame({seq:data[seq].apply(grades).value_counts().to_dict() for seq in evaluations})

##print(student_grade)

bar_polar = px.bar_polar(data_frame=sgca, r='Male', 
	theta=sgca.index, color='Female', 
	title='General Class Average (GCA) for each evaluation',
	barmode="overlay",width=1200, height=500)
pie_form = px.pie(data_frame=form_counts, names=form_counts.index, values=form_counts,
 title="Form", hole=0.25, width=500, height=500)
pie_gender = px.pie(data_frame=gender_counts, names=gender_counts.index, values=gender_counts,
 title="Gender", hole=0.25, width=500, height=500)


feature_importances = segmentation(data)

bar_feature_importance = px.bar(data_frame=feature_importances, x="Feature", y="Gain",
  title="Feature importances bar", width=500)

with open("images/tree.dot") as f:
	dot_graph = f.read()

female = data[data.gender == "F"]
male   = data[data.gender == "M"]


def visualization():
	placeholder1 = st.empty()

	with placeholder1.container():
		kp1, kp2, kp3, kp4, kp5, kp6 = st.columns(6)

		kp1.metric(
			label= "**:red[👬 Total students]**",
			value = total_students,
			delta = ""
			)

		kp2.metric(
			label= ":red[**⏳ Average age**]",
			value = f"{average_age:.2f}" ,
			delta = ""
			)

		kp3.metric(
			label=":red[**✍ GCA-trimester 1**]",
			value=f"{gca1:.2f}/20",
			delta = 0.0
			)
		kp4.metric(
			label=":red[**✍ GCA-trimester 2**]",
			value = f"{gca2:.2f}/20",
			delta = round(gca2-gca1, 3) 
			)
		kp5.metric(
			label =":red[**✍ GCA-trimester 3**]",
			value = f"{gca3:.2f}/20",
			delta = round(gca3-gca2, 3) 
			)
		kp6.metric(
			label =":red[**🎓 Annual-GCA**]",
			value = f"{annual_gca:.2f}/20",
			delta = "" 
			)


	placeholder2 = st.empty()
	with placeholder2.container():
		col1, col2 = st.columns(2)
		col1.plotly_chart(pie_gender)
		col1.caption('**We represent the gender of students in form 6e-5e (francophone section one of the cameroonian education system).**')
		col2.plotly_chart(pie_form)
		col2.caption("""**We represent the number of students in each form 6e and 5e**. 
		**NB**: **Cameroon have two sub-education systems one is a francophone and a second is an anglosaxone.**   
			""")
	
	tab1, tab2, tab3 = st.tabs([':orange[**Performance**]', ':orange[**Distribution**]', ':orange[**Miscelaneous**]'])

	with tab1:
		tab1.plotly_chart(bar_polar)
		tab1.caption("""We represent the general class average of students in each sequence. Colors bar shows the marks 
			for female gender and bar polar also shows the marks for male gender.""")
		tab1.subheader('Progression')
		tab1.line_chart(progression)
		tab1.caption("""This chart shows a progression of students during the six evaluations. 
			We just make a difference between the previous sequence and the next sequence. 
			The x-axis represent a sequence and the y-axis represent the growth of students.""")

		tab1.subheader('Passed or Failed')
		col1, col2 = tab1.columns(2)
		col1.caption(':red[💃 passed or failed table 👉]')
		col1.dataframe(pass_or_fail)
		col1.caption("""
		- In left: We got this table to compute the number of students that the mark is  >10 (passed) or <10 (failed) for 
		each sequence.
		- In right: We plot this table. The chart explains how a student make some effort to succeed a ICT course.   
		- In general, we can appreciate the effort of the students in the form 6e and 5e for each evaluation.   
			""")
		col2.bar_chart(pass_or_fail.T)

		tab1.subheader("Student grades")
		col3, col4 = tab1.columns(2)
		col3.caption(':red[💃 grades table 👉]')
		col3.dataframe(student_grade.fillna(0))
		col3.caption("""   
			The student grade respect this decision:
			- U -> [0 - 5[;   E -> [5 - 9[
			- D -> [9 - 12[;  C -> [12 - 15[
			- B -> [15 - 18[; A -> [18 - 20[
			""")
		col4.bar_chart(student_grade.T)
		col4.caption('This bar chart shows the number of student in each grade for each sequence.')

	with tab2:
		tab2.subheader('evaluation and age distribution')
		tab2.caption('Histogram')
		var1 = tab2.selectbox('Choose items', evaluations+['age'], key=6)
		fig1 = px.histogram(data_frame=data, x=var1,  width=1200, height=500, opacity=0.75)
		tab2.plotly_chart(fig1)
		col1, col2 = tab2.columns(2)
		col1.caption('Boxplot'); col2.caption('Violin')
		var2 = col1.selectbox('Choose items', evaluations+['age'], key=7)
		var3 = col2.selectbox('Choose items', evaluations+['age'], key=8)
		col1.plotly_chart(px.box(data_frame=data, y=var2,  width=500, height=500))
		col2.plotly_chart(px.violin(data_frame=data, x=var3,  width=500, height=500))


	with tab3:
		st.subheader('Relation graph')
		container = tab3.empty()
		vcol1, vcol2, vcol3 = container.columns(3)

		trim1 = px.scatter(data_frame=df_trim, x="trimester 1", y="trimester 2", width=350, 
			height=350,title="trimester 1 & 2")
		vcol1.plotly_chart(trim1)

		trim2 = px.scatter(data_frame=df_trim, x="trimester 2", y="trimester 3", width=350, height=350,title="trimester 3 & 2")
		vcol2.plotly_chart(trim2)

		trim3 = px.scatter(data_frame=df_trim, x="trimester 3", y="trimester 1", width=350, height=350,title="trimester 1 & 3")
		vcol3.plotly_chart(trim3)

		tab3.caption("""
			The three charts shows the monotony of the relation function between the three trimesters. 
			Each chart prove that the students for form 6e-5e francophone education systems at the Tebap college make considerably
			an effort to succeed an ICT's course.
			""")
		tab3.subheader('Supervised segmentation with tree')
		tab3.caption(""" 
			In this section, we are making a supervised segmentation to segment the population of student into subgroups
			that have different values for the target gender. To find a subgroups, we are using a tree structured model.
			We cannot make a classification here because our dataset is just a size equal to 46. Let's go! 💂
			""")
		block = tab3.empty()
		hcol1, hcol2 = block.columns(2)
		hcol1.caption('**Feature importance table**👉')
		hcol1.dataframe(feature_importances)
		hcol1.caption("""  
			The table shows the features that the tree structured model 
			consider very importance for segmenting students
			population in to subgroups. 
			""")

		hcol2.plotly_chart(bar_feature_importance)
		tab3.subheader('Dot graph')
		tab3.graphviz_chart(dot_graph)
		tab3.caption("""
			Let's us interprete this graph.

			- node 0: the student that the mark in seq 6 <= 11.375 are female gender; the answer is False. In each node, we have 
			a condition where the next node give an answers.

			Let's plot the line separating the region.  
			""")

		bcol1, bcol2 = tab3.columns(2)

		
		var1 = bcol1.selectbox("Choose x-axis (line[i])", ['seq 1', "seq 2", "seq 4", "seq 6"])
		var2 = bcol1.selectbox("Choose y-axis (line[i+1])", reversed(['seq 1', "seq 2", "seq 4", "seq 6"]))
		
		line1 = bcol2.multiselect("Line separator for x-axis", [1.25, 2.75, 3.125, 4.375,5.0, 5.625, 11.375,13.5]) 
		line2 = bcol2.multiselect("Line separator for y-axis", [1.25, 2.75, 3.125, 4.375,5.0, 5.625, 11.375,13.5])
		tab3.caption("""  
			We have eight lines line 1 (node 0) to line 8 (node 12). We start to line 1 and line 2.  
			""")
		gplot = scatterplot(female, male, line_separator=[line1, line2], x_axis=var1, y_axis=var2)
		tab3.pyplot(gplot)

		

		

