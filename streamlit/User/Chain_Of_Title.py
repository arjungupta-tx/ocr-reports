import streamlit as st
import pandas as pd
from src.pipeline.llm_api import LLM_API_LIST



st.set_page_config(
    page_title="Project",
    layout="wide",
)

llm_obj  = LLM_API_LIST()


def chainoftitle():

    try:
        uploaded_file = st.file_uploader("Choose an Excel file", type=["xlsx", "xls"])

        
        if uploaded_file is not None:
           
           df = pd.read_excel(uploaded_file, engine="openpyxl")
           print(df)
        #    jsondata = llm_obj.chai_of_title_anthropic(df) 
           jsondata,token_ = llm_obj.chai_of_title(df)
           st.markdown(jsondata)
           st.dataframe(df)
        #    st.json(jsondata)

        else:
            st.info("Please upload an Excel file to proceed.")


    except Exception as e:
        print(f"Error : {e}")





with st.container():
    chainoftitle()        