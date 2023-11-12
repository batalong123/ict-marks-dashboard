import streamlit as st
from module.cards import welcome, about_me
from module.dataset import eda
from module.load_data import data
from module.data_viz import visualization
import numpy as np
from datetime import datetime

global LOW, HIGH, SEQUENCE, RESET

LOW = 10.0*np.ones((46,7))
HIGH = 20.0*np.ones((46,7))
SEQUENCE = ['seq 1','seq 2','seq 3','seq 4','seq 5','seq 6','average_marks']
RESET = True

st.set_page_config(
    page_title="ICT Mark's Dashboard",
    page_icon="📢",
    layout="wide")



st.title("📊 :red[ICT Mark's] Dashboard")

welcome()
about_me()

date = f"{datetime.today().date()} {datetime.today().hour}:{datetime.today().minute}:{datetime.today().second}"

#page = st.selectbox('Select page:', ['Dataset','EDA', 'Data Viz'])
tab1, tab2, tab3 = st.tabs(['**Dataset**','**EDA**', '**Data Viz**'])

with  tab1:
    
    st.info(f"You select Dataset page at the {date}", icon="💂")
    col1, col2, col3, col4 = st.columns(4)

    if col1.button(':orange[**highlight >10/20**]'):
        st.dataframe(data.style.highlight_between(axis=None, color="#fffd75", left=LOW, right=HIGH,
        subset=SEQUENCE), use_container_width=True)
        RESET = False

    if col2.button(':orange[**highlight max**]'):
        st.dataframe(data.style.highlight_max(color="green", subset=SEQUENCE), use_container_width=True)
        RESET = False

    if col3.button(':orange[**highlight min**]'):
        st.dataframe(data.style.highlight_min(color="red", subset=SEQUENCE), use_container_width=True)
        RESET = False
    
    if RESET:
        st.dataframe(data, use_container_width=True)

    if col4.button(':black[**reset**]'):
        st.dataframe(data, use_container_width=True)



    with st.expander("👁 Read more"):
        st.markdown("""
        This dataset is an :red[ICT Mark's] data come from the evaluation of the Tebap students. The attributes are defined as follows:

        > 1. :orange[$seq_{i, i = (1,2,3,4,5,6)}$]: are the 6 sequences that
        Tebap student's had undergone during school year 2018-2019.
        > 2. :orange[age]: the age of the students. 
        > 3. :orange[gender]: the gender of the students (M or F).
        > 4. :orange[form]: the class of students.
        > 5. :orange[average_marks]: the annual ICT mark's of each student.
          """)

with tab2 :
    st.info(f"You select EDA page at the {date}", icon="💂")
    st.header('Exploratory Data Analysis')
    eda()
	

with tab3:
    st.info(f"You select Data Viz page at the {date}", icon="💂")
    st.header('Visualization')
    visualization() 


	

