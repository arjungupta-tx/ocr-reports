import streamlit as st
from src.SQLdb.sql_query_engine import fetch_all,insert_data,fetch_one
from src.pipeline.google_storage import upload_file_to_gcs
import pandas as pd

from src.SQLdb.sql_query_engine import fetch_all,fetch_one,insert_data,execute_update
from src.Utils.utils import create_folders_users,extract_image,get_all_images_paths_list,count_all_files,delete_existing_files
from src.Utils.common import encode_image
from src.pipeline.google_storage import download_file_from_gcs
from src.pipeline.ocr_api import OCR_API_LIST
from src.pipeline.llm_api import LLM_API_LIST

from datetime import datetime
import os

# import zipfile
# from io import BytesIO



st.session_state.ocr_api_list = OCR_API_LIST()
st.session_state.comperision_ai = LLM_API_LIST()



st.set_page_config(
    page_title="Project",
    layout="wide",
)

def color_status(val):
    color = ''
    if val == 'Completed':
        color = 'background-color: green; color: white'
    elif val == 'In Progress':
        color = 'background-color: yellow; color: black'
    elif val == 'Pending':
        color = 'background-color: grey; color: white'
    return color

# @st.dialog("Upload Files")
def file_uploads():

    try:

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


                    threshold_accuracy = st.selectbox(label="Select Threshold Accuracy",options=["Select",70,75,80,85,90]) 
                    if threshold_accuracy == "Select":
                        st.info("Please select accuracy")
                    else:    
                        uploaded_files = st.file_uploader("Upload a file",type=["pdf"],accept_multiple_files=True)
                        print(f"Total files {len(uploaded_files)} and file is --- {uploaded_files}")

                
                        submitted = st.button("Upload Files")
                        if submitted:
                            st.session_state.Id_org = st.session_state.title_to_id_map [st.session_state.selected_title]
                            query_ocr = f"SELECT status FROM MORdb.ORG_Title WHERE Id_Org = {int(st.session_state.Id_org)}"
                            
                            result_ocr = fetch_one(query_ocr)
                            print(f"OCR status {result_ocr[0]}")
                            if result_ocr[0] == "OCR Completed":
                                st.info(f"OCR has been completed for this project: {st.session_state.selected_title}")
                            else:
                                
                                if st.session_state.selected_title:
                                    if threshold_accuracy:
                                        if len(uploaded_files) > 0:
                                            progress = st.progress(0,text="Uploading Files....")
                                            total_files_to_upload = len(uploaded_files)
                                            for k,uploaded_file in enumerate(uploaded_files):
                                                

                                                query = f"SELECT COUNT(*) FROM Pdf_File_Name WHERE Pdf_Name = '{str(uploaded_file.name)}' AND Id_Org = {int( st.session_state.Id_org)};"
                                                data =fetch_one(query)
                                                if  data[0] > 0:
                                                    # st.warning("pdf file already exits")
                                                    pass
                                                else:    
                                                    # Id_org = title_to_id_map[selected_title]

                                                    project_name = st.session_state.selected_title
                                                
                                                    user_name = st.session_state.user_email
                                            
                                                    file_pth = upload_file_to_gcs(project_name=project_name,user_name=user_name,file=uploaded_file,destination_filename=uploaded_file.name)
                                                    if file_pth is not None:

                                                        Total_page = 0
                                                        IOCSR = 0
                                                        File_type = "NaN"
                                                        Manual_review = "NaN"
                                                        runsheet_details = "NaN"
                                                        # st.info("file uploaded successfuly")
                                                        query1 = f""" 
                                                                INSERT INTO Pdf_File_Name(Pdf_Name,Total_Pages,IsOcr,Accuracy_Threshold,File_Type,Manual_Review_Page_Numbers,File_Path_Server,Id_Org,Runsheet_Details)

                                                                VALUES('{str(uploaded_file.name)}',{int(Total_page)},{int(IOCSR)},{int(threshold_accuracy)},'{str(File_type)}','{str(Manual_review)}','{str(file_pth)}',{int(st.session_state.Id_org)},'{str(runsheet_details)}')
                                                        
                                                                """
                                                        
                                                        result = insert_data(query1)
                                                        if result.get("rows_affected",0) > 0:
                                                            print(f"Data Inserted successfully")
                                                            progress.progress(int(((k+1)/total_files_to_upload)*100), text=f"Uploading Files......{k+1}/{total_files_to_upload}")
                                            
                                            query2= f"SELECT Id_Pdf, Pdf_Name FROM Pdf_File_Name where Id_Org = {int(st.session_state.Id_org)} AND IsOcr = 0;"
                                            result2 = fetch_all(query2)
                                            print(result2)
                                            if not result2:
                                                st.info(f"No pdf files are available for this project {st.session_state.selected_title}")

                                            else:    
                                                st.session_state.pdf_file_to_id_map = {pdf_file: id_pad for id_pad, pdf_file in result2}
                                                if result2 is not None:
                                                    # st.session_state.pdf_file_name_list = [element for tuple_item in result2 for element in tuple_item]
                                                    print(f"pdf file list {st.session_state.pdf_file_to_id_map}")
                                                    print(f"pdf file {result2}")
                                                    data ={"File Name": list(st.session_state.pdf_file_to_id_map.keys()),
                                                            # "Total Pages":0,
                                                            "Status": ["Pending"] * len(st.session_state.pdf_file_to_id_map),
                                                            "Details": ["--"] * len(st.session_state.pdf_file_to_id_map)
                                                            }
                                                    with st.container(border=True):
                                                        st.session_state.df = pd.DataFrame(data)
                                                        st.session_state.table_placeholder = st.empty()  # Placeholder for the table
                                                        st.session_state.table_placeholder.dataframe(st.session_state.df,use_container_width=True)

                                                    for inx,(pdf_file_name,pdf_file_id) in enumerate(st.session_state.pdf_file_to_id_map.items()):
                                                        st.session_state.user_file_path, st.session_state.pdf_file_path, st.session_state.image_file_path,st.session_state.txt_file_path,retrieve_mage_file_path = create_folders_users(User_file=st.session_state.user_email)
                                                        print(st.session_state.user_file_path)
                                                        print(st.session_state.pdf_file_path)
                                                        print(st.session_state.image_file_path)

                                                        
                                                        st.session_state.df.at[inx, "File Name"] = pdf_file_name
                                                        # st.session_state.df.at[inx, "Total Pages"] = st.session_state.page_count
                                                        st.session_state.df.at[inx, "Status"] = "In Progress"
                                                        
                                                        st.session_state.df_style=st.session_state.df.style.applymap(color_status, subset=['Status'])
                                                        st.session_state.table_placeholder.dataframe(st.session_state.df_style,use_container_width=True) 

                                                        delete_existing_files(st.session_state.pdf_file_path)
                                                        delete_existing_files(st.session_state.image_file_path)
                                                        delete_existing_files(st.session_state.txt_file_path)
                                                        file_path1 = download_file_from_gcs(user_name=st.session_state.user_email,project_name=st.session_state.selected_title,destination_file_name=pdf_file_name,local_file_dir=f"{st.session_state.pdf_file_path}/{pdf_file_name}")
                                                        if file_path1 is not None:
                                                            st.session_state.local_pdf_file_path = os.path.join(st.session_state.pdf_file_path,pdf_file_name)
                                                            print(st.session_state.local_pdf_file_path)
                                                            st.session_state.page_count = extract_image(st.session_state.local_pdf_file_path,st.session_state.image_file_path)
                                                            
                                                            # Need to upload extraced image
                                                            if st.session_state.page_count >0:
                                                                st.session_state.list_images = get_all_images_paths_list(st.session_state.image_file_path)
                                                                print(st.session_state.list_images)
                                                                for k,i in enumerate(st.session_state.list_images):
                                                                    print(k,i)
                                                                    st.session_state.df.at[inx, "Details"] = f"OCR Progress: {k+1}/{st.session_state.page_count}"
                                                                    st.session_state.df_style=st.session_state.df.style.applymap(color_status, subset=['Status'])
                                                                    st.session_state.table_placeholder.dataframe(st.session_state.df_style,use_container_width=True) 
                                                                    
                                                                    image_base64 = encode_image(i)
                                                                    txt_docai,accuracy_docai, time_docai = st.session_state.ocr_api_list.document_ai_api(image=i)
                                                                    txt_anthropic,token_anthropic, time_anthropic  = st.session_state.ocr_api_list.anthropic_api(image_base64)
                                                                    txt_aponai,toketopenai, time_openai = st.session_state.ocr_api_list.open_ai_api(image_base64)
                                                                    txt_comperision, openai_token_compare, time_coperision = st.session_state.comperision_ai.merge_with_openai(doc1=txt_docai,doc2=txt_anthropic,doc3=txt_aponai)
                                                                    image_base64 = ""
                                                                    query_insert = f"""
                                                                                        INSERT INTO Ocr_Page (
                                                                                            Ocr_Accuracy, Ocr_Document_AI, Ocr_Open_AI, Ocr_Anthropic, Ocr_Comparable, 
                                                                                            Total_Time_Document_AI, Total_Time_Open_AI, Total_Time_Anthropic, 
                                                                                            Total_Token_Document_AI, Total_Token_Open_AI, Total_Token_Athropic, 
                                                                                            Total_Price_Document_AI, Total_Price_Open_AI, Total_Price_Anthropic, 
                                                                                            Id_Pdf, Pgae_Number, Total_Token_Comperision_api, Total_Time_Comperision, 
                                                                                            Txt_Update_Status, Date
                                                                                        ) VALUES (
                                                                                            {int(accuracy_docai)}, 
                                                                                            '{str(txt_docai).replace("'", "''")}', 
                                                                                            '{str(txt_aponai).replace("'", "''")}', 
                                                                                            '{str(txt_anthropic).replace("'", "''")}', 
                                                                                            '{str(txt_comperision).replace("'", "''")}', 
                                                                                            '{str(time_docai)}', 
                                                                                            '{str(time_openai)}', 
                                                                                            '{str(time_anthropic)}', 
                                                                                            {int(0)}, 
                                                                                            {int(toketopenai)}, 
                                                                                            {int(token_anthropic)}, 
                                                                                            {float(0.00)}, 
                                                                                            {float(0.00)}, 
                                                                                            {float(0.00)}, 
                                                                                            {int(pdf_file_id)}, 
                                                                                            {int(k + 1)}, 
                                                                                            {int(openai_token_compare)}, 
                                                                                            '{str(time_coperision)}', 
                                                                                            'Row Text', 
                                                                                            '{str(datetime.now().strftime("%Y-%m-%d"))}'
                                                                                        );
                                                                                        """
                                                                    result = insert_data(query_insert)
                                                                    if result.get("rows_affected",0) > 0:
                                                                        pass
                                                                        # add progressbar
                                                                    else:
                                                                        st.error(result)  
                                                                else:
                                                                    st.session_state.df.at[inx, "Status"] = "Completed"
                                                                    st.session_state.df_style=st.session_state.df.style.applymap(color_status, subset=['Status'])
                                                                    st.session_state.table_placeholder.dataframe(st.session_state.df_style,use_container_width=True)  
                                                                    query_count = f"SELECT count(*) FROM MORdb.Ocr_Page where Id_Pdf = {int(pdf_file_id)};"   
                                                                    count = fetch_one(query_count)     
                                                                    if count[0] == st.session_state.page_count:
                                                                        query_update = f""" UPDATE Pdf_File_Name SET Total_Pages = {int(st.session_state.page_count)}, IsOcr = {int(1)} WHERE Id_Pdf = {int(pdf_file_id)} ;"""
                                                                        execute_update(query_update)
                                                                        # runsheet genration
                                                                    else:
                                                                        print(f"Total number of pages is {st.session_state.page_count} but OCR done only on {count} pages")
                                                                        # runsheet genration
                                                    else:
                                                        passquery_update = f""" UPDATE ORG_Title SET status = '{str("OCR Completed")}' WHERE Id_Org = {int(st.session_state.Id_org)} ;"""
                                                        execute_update(passquery_update)
                                                    #update project status
                                                    # runsheet genration


    except Exception as e:
        print(f"error {e}")                





# def display_data():
#     user_id = st.session_state.user_id
#     query_data = f""" SELECT  og.Title_Name, pd.Pdf_Name,pd.Total_Pages,pd.IsOcr, pd.Accuracy_Threshold, pd.File_Type, pd.Manual_Review_Page_Numbers, pd.Runsheet_Details FROM Pdf_File_Name as pd  RIGHT JOIN ORG_Title as og ON pd.Id_Org =  og.Id_Org where og.Id_user = {int(user_id)};"""
#     result = fetch_all(query_data)
#     if result:

#         column = ["Project Name","File Name","Total Pages","IsOcr","Accuracy Threshold","File Type","Manual Review Page_Numbers","Runsheet Details"]
#         df =pd.DataFrame(data=result,columns=column)
#         st.dataframe(df,use_container_width=True,selection_mode="single-row",hide_index=True)


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

    file_uploads()
     

# with st.container(border=True):
#     display_data()


# with st.container(border=True):
# #    pdf_processing()
#     pass
        


