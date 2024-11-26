import streamlit as st
from src.SQLdb.sql_query_engine import fetch_all,insert_data,fetch_one
from src.loging import logger
import pandas as pd




def display_project(org_id):
    user_id = st.session_state.user_id
    query_data = f""" SELECT pd.Id_Pdf, pd.Pdf_Name,pd.Total_Pages,pd.IsOcr FROM Pdf_File_Name as pd WHERE pd.Id_Org = {int(org_id)};"""
    result = fetch_all(query_data)
    if result:

        column = ["PDF ID","File Name","Total Pages","IsOcr"]
        df =pd.DataFrame(data=result,columns=column)
        X= df.drop(df.columns[0], axis=1)
        y = dict(zip(df["File Name"], df["PDF ID"]))
        
        st.dataframe(X,use_container_width=True,selection_mode="single-row",hide_index=True)
        return y



def ocr_page_display(pdf_file):
    options = list(pdf_file.keys())
    options.insert(0,"Select")
    select_pdf = st.selectbox("Select pdf",options=options)
    if select_pdf == "Select":
        st.info("Please select pdf")
    else:
        pdf_id = pdf_file[select_pdf]
        st.info(pdf_id)
        
        query1 = f"SELECT Ocr_Accuracy,Pgae_Number FROM MORdb.Ocr_Page WHERE Id_Pdf = {int(pdf_id)}"
        result_select = fetch_all(query1)
        if result_select:
            column = ["Accuracy", "Page Number"]
            df1 = pd.DataFrame(data=result_select,columns=column)
            st.dataframe(df1[df1.columns[::-1]],use_container_width=True,selection_mode="single-row",hide_index=True)




def select_project():
    try:
         st.title("Project Details")

         with st.container(border=True):
            user_id = st.session_state.user_id
            query = f"SELECT Id_Org,Title_Name FROM MORdb.ORG_Title where Id_user = {int(user_id)};"
            result = fetch_all(query)
            st.session_state.title_to_id_map = {title: id_org for id_org, title in result}
            print(result)
            if result is not None:
                options = list(st.session_state.title_to_id_map.keys())
                options.insert(0,"Select")
                st.session_state.selected_title = st.selectbox(label="Select Project", options=options)
                if st.session_state.selected_title == "Select":
                    st.info("Plsese select Project")
                else:    
                    with st.container(border= True):
                        st.subheader("PDF Details",divider=True)
                        org_id = st.session_state.title_to_id_map[st.session_state.selected_title]

                        pdf_file = display_project(org_id)

                    with st.container(border=True):
                        st.subheader("OCR Page",divider=True)  

                        ocr_page_display(pdf_file)  







    except Exception as e:
        print(f"{e}")    






select_project()



