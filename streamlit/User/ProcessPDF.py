import streamlit as st
from src.SQLdb.sql_query_engine import fetch_all,insert_data,fetch_one
from src.pipeline.google_storage import upload_file_to_gcs
import pandas as pd
# import PyPDF2



st.set_page_config(
    page_title="Project",
    layout="wide",
)

@st.dialog("Upload Files")
def file_uploads():

    try:

        with st.form("File"):
            user_id = st.session_state.user_id
            query = f"SELECT Id_Org,Title_Name FROM MORdb.ORG_Title where Id_user = {int(user_id)};"
            result = fetch_all(query)
            title_to_id_map = {title: id_org for id_org, title in result}
            print(result)
            if result is not None:
             selected_title = st.selectbox(label="Select Project", options=list(title_to_id_map.keys()))


            threshold_accuracy = st.selectbox(label="Select Threshold Accuracy",options=[70,75,80,85,90]) 
            uploaded_file = st.file_uploader("Upload a file",type=["pdf"])

    
            submitted = st.form_submit_button("Submit")
            if submitted:
                if selected_title:
                    if threshold_accuracy:
                        if uploaded_file:

                            query = f"SELECT COUNT(*) FROM Pdf_File_Name WHERE Pdf_Name = '{str(uploaded_file.name)}';"
                            data =fetch_one(query)
                            if  data[0] > 0:
                                st.warning("pdf file already exits")
                            else:    
                                Id_org = title_to_id_map[selected_title]

                                project_name = selected_title
                            
                                user_name = st.session_state.user_email
                        
                                file_pth = upload_file_to_gcs(project_name=project_name,user_name=user_name,file=uploaded_file,destination_filename=uploaded_file.name)
                                if file_pth is not None:

                                    Total_page = 0
                                    IOCSR = 0
                                    File_type = "NaN"
                                    Manual_review = "NaN"
                                    runsheet_details = "NaN"
                                    st.info("file uploaded successfuly")
                                    query1 = f""" 
                                            INSERT INTO Pdf_File_Name(Pdf_Name,Total_Pages,IsOcr,Accuracy_Threshold,File_Type,Manual_Review_Page_Numbers,File_Path_Server,Id_Org,Runsheet_Details)

                                            VALUES('{str(uploaded_file.name)}',{int(Total_page)},{int(IOCSR)},{int(threshold_accuracy)},'{str(File_type)}','{str(Manual_review)}','{str(file_pth)}',{int(Id_org)},'{str(runsheet_details)}')
                                    
                                            """
                                    
                                    result = insert_data(query1)
                                    if result.get("rows_affected",0) > 0:
                                        st.info("File Data saved successfully")
                                        st.rerun()

                        else:
                            st.warning("Please upload file")     

                    else:
                        st.warning("Please select Threshold accuracy")        
                else:
                    st.warning("Please select Project")    

    except Exception as e:
        print(f"error {e}")                


def display_data():
    user_id = st.session_state.user_id
    query_data = f""" SELECT  og.Title_Name, pd.Pdf_Name,pd.Total_Pages,pd.IsOcr, pd.Accuracy_Threshold, pd.File_Type, pd.Manual_Review_Page_Numbers, pd.Runsheet_Details FROM Pdf_File_Name as pd  RIGHT JOIN ORG_Title as og ON pd.Id_Org =  og.Id_Org where og.Id_user = {int(user_id)};"""
    result = fetch_all(query_data)
    if result:

        column = ["Project Name","File Name","Total Pages","IsOcr","Accuracy Threshold","File Type","Manual Review Page_Numbers","Runsheet Details"]
        df =pd.DataFrame(data=result,columns=column)
        st.dataframe(df,use_container_width=True,selection_mode="single-row",hide_index=True)


# st.session_state.id_org = None
# def pdf_processing():
#     with st.form("PDF Processing"):
#         user_id = st.session_state.user_id
#         query = f"SELECT Id_Org,Title_Name FROM MORdb.ORG_Title where Id_user = {int(user_id)};"
#         result = fetch_all(query)
#         title_to_id_map = {title: id_org for id_org, title in result}
#         # print(result)
#         if result is not None:
#             selected_title = st.selectbox(label="Select Project", options=list(title_to_id_map.keys()))   
#             if selected_title is not None:   
#                 btn_select = st.form_submit_button(label="Next")
#                 if btn_select:
#                     print(f"Project naem {selected_title}")
#                     Id_org  = title_to_id_map[selected_title]  
#                     query2= f"SELECT Pdf_Name FROM Pdf_File_Name where Id_Org = {int(Id_org)};"
#                     result2 = fetch_all(query2)
#                     if result2 is not None:
#                         print(f"pdf file {result2}")
#                         select_pdf_file = st.selectbox(label="Select pdf file",options=list(result2))
#                         if select_pdf_file:
#                          st.write(select_pdf_file)

                    # st.form_submit_button(label="Submit")          


# def select_pdf():
#     query2= f"SELECT Pdf_Name FROM Pdf_File_Name where Id_Org = {int(st.session_state.id_org )};"
#     result2 = fetch_all(query2)
#     if result2 is not None:
#         print(f"pdf file {result2}")
#         select_pdf_file = st.selectbox(label="Select pdf file",options=list(result2))
#         if select_pdf_file:
#             st.write(select_pdf_file)







with st.container():

    if st.button("Upload Files"):
     file_uploads()

with st.container(border=True):
    display_data()


with st.container(border=True):
#    pdf_processing()
    pass
        


