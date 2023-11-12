import streamlit as st
from PIL import Image


image_file = "images/massock.jpg"
path_image = "images/SIPE_sketch.jpg"
image = Image.open(image_file)

text1 = """
*I am a young Cameroonian named **Massock Batalong Maurice Blaise** with a *Masters in specialty Materials/
Mechanics option Mechanics at the University of Yaoundé I* and a *Master in Science Mathematics at the
African Institute for Mathematical Sciences (AIMS-Cameroon)*. And holder of a *Certificate in Big Data
Analytics with python issued by AIMS-Cameroon*. I am also a Kaggle Notebook & Discussion Expert.*   

- **LinkedIn**: Massock Batalong Maurice Blaise
- **Email**: lumierebatalong@gmail.com
"""

text2 = """
*This dashboard is one little part of my project :green[**Creation of Intelligent system for an Education Performance (ISEP)**].*
"""

text3 = """
To construct an intelligent system able to evaluate an educational performance of students of an
establishment (school, secondary school, training center, university,...) given and to help respectively the
teacher staff and the administrative staff to arrest well an evolution of school teaching of theirs students.
Because in future, these students will be human ressources qualified able to releive the challenge and stakes
of Africa in the domain such that education, health, water, energy, agriculture, infrastructure, etc ...
"""



def welcome():

	placeholder = st.empty()

	with placeholder.container():
		kp1, kp2, kp3, kp4, kp5 = st.columns(5)

		kp1.metric(
			label= "🗓 **:red[School year]**",
			value = "2018-2019",
			delta = ""
			)

		kp2.metric(
			label= "👨🎓 :red[**College**]",
			value = "Tebap",
			delta = ""
			)
		kp3.metric(
			label="👩🏫 :red[**Form**]",
			value="6e-5e",
			delta = ""
			)

		kp4.metric(
			label="🏛 :red[**City**]",
			value="Yaounde",
			delta = ""
			)
		kp5.metric(
			label="🏴 :red[**Country**] ",
			value = "Cameroon",
			delta = "" 
			)

def about_me():
	st.sidebar.image(image)
	st.sidebar.markdown(text1)
	st.sidebar.markdown(text2)
	st.sidebar.header("Abstract")
	st.sidebar.markdown(text3)
	st.sidebar.image(path_image)

