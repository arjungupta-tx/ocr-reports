import streamlit as st
from src.SQLdb.sql_query_engine import fetch_all,fetch_one
from src.Utils.utils import create_folders_users,extract_image,get_all_images_paths_list,count_all_files,delete_existing_files
from src.Utils.common import encode_image
from src.pipeline.google_storage import download_file_from_gcs
from src.pipeline.ocr_api import OCR_API_LIST
from src.pipeline.llm_api import LLM_API_LIST
from src.SQLdb.sql_query_engine import insert_data,execute_update
import time
from datetime import datetime
import os
import pandas as pd
import zipfile
from io import BytesIO



st.session_state.ocr_api_list = OCR_API_LIST()
st.session_state.comperision_ai = LLM_API_LIST()

def pdf_processing():
    
        user_id = st.session_state.user_id
        query = f"SELECT Id_Org,Title_Name FROM MORdb.ORG_Title where Id_user = {int(user_id)};"
        result = fetch_all(query)
        st.session_state.title_to_id_map = {title: id_org for id_org, title in result}
        # print(result)
        if result is not None:
            options=list(st.session_state.title_to_id_map.keys())
            options.insert(0,"Select")
            selected_title = st.selectbox(label="Select Project", options=options)   
            if selected_title != "Select":   
              
                print(f"Project naem {selected_title}")
                Id_org  = st.session_state.title_to_id_map[selected_title]  
                query2= f"SELECT Id_Pdf, Pdf_Name FROM Pdf_File_Name where Id_Org = {int(Id_org)} AND IsOcr = 0;"
                result2 = fetch_all(query2)
                print(result2)
                if not result2:
                    st.info(f"No pdf files are available for this project {selected_title}")

                else:    
                    st.session_state.pdf_file_to_id_map = {pdf_file: id_pad for id_pad, pdf_file in result2}
                    if result2 is not None:
                        results_list = [element for tuple_item in result2 for element in tuple_item]
                        print(f"pdf file list {results_list}")
                        print(f"pdf file {result2}")
                        options=list(st.session_state.pdf_file_to_id_map.keys())
                        options.insert(0,"Select")
                        st.session_state.select_pdf_file = st.selectbox(label="Select pdf file",options=options)
                        if st.session_state.select_pdf_file != "Select":
                            btn_pdf = st.button(label="Submit")
                            pdf_id = st.session_state.pdf_file_to_id_map[st.session_state.select_pdf_file]
                            print(st.session_state.select_pdf_file)
                            if btn_pdf:
                                user_email = st.session_state.user_email
                                st.session_state.user_file_path, st.session_state.pdf_file_path, st.session_state.image_file_path,st.session_state.txt_file_path,retrieve_mage_file_path = create_folders_users(User_file=user_email)
                                print(st.session_state.user_file_path)
                                print(st.session_state.pdf_file_path)
                                print(st.session_state.image_file_path)
                                delete_existing_files(st.session_state.pdf_file_path)
                                delete_existing_files(st.session_state.image_file_path)
                                delete_existing_files(st.session_state.txt_file_path)
                                
                                file_path1 = download_file_from_gcs(user_name=user_email,project_name=selected_title,destination_file_name=st.session_state.select_pdf_file,local_file_dir=f"{st.session_state.pdf_file_path}/{st.session_state.select_pdf_file}")
                                if file_path1 is not None:

                                    st.session_state.local_pdf_file_path = os.path.join(st.session_state.pdf_file_path,st.session_state.select_pdf_file)
                                    print(st.session_state.local_pdf_file_path)
                                    st.session_state.page_count = extract_image(st.session_state.local_pdf_file_path,st.session_state.image_file_path)
                                    if st.session_state.page_count >0:
                                        st.session_state.list_images = get_all_images_paths_list(st.session_state.image_file_path)
                                        print(st.session_state.list_images)
                                        with st.container(border=True):
                                            progress_bar = st.progress(0)
                                        with st.container(border=True):
                                            st.info(f"Total number of pages in pdf file is {st.session_state.page_count }")
                                            st.info(f"Total number of images in a extraced folder is {count_all_files(st.session_state.image_file_path)}")

                                        for k,i in enumerate(st.session_state.list_images):
                                            print(k,i)
                                            status_text =f"OCR Processing...... {k + 1}/{st.session_state.page_count}"
                                            progress_bar.progress(int(((k + 1)/(st.session_state.page_count))*100),text=status_text)
                                            # promt_txt=Prompt_txt_ocr
                                            
                                            st.session_state.image_base64 = encode_image(i)
                                            txt_docai,accuracy_docai, time_docai = st.session_state.ocr_api_list.document_ai_api(image=i)
                                            txt_anthropic,token_anthropic, time_anthropic  = st.session_state.ocr_api_list.anthropic_api(st.session_state.image_base64)
                                            txt_aponai,toketopenai, time_openai = st.session_state.ocr_api_list.open_ai_api(st.session_state.image_base64)
                                            txt_comperision, openai_token_compare, time_coperision = st.session_state.comperision_ai.merge_with_openai(doc1=txt_docai,doc2=txt_anthropic,doc3=txt_aponai)

                                           
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
                                                                    {int(pdf_id)}, 
                                                                    {int(k + 1)}, 
                                                                    {int(openai_token_compare)}, 
                                                                    '{str(time_coperision)}', 
                                                                    'Row Text', 
                                                                    '{str(datetime.now().strftime("%Y-%m-%d"))}'
                                                                );
                                                                """
                                            result = insert_data(query_insert)
                                            if result.get("rows_affected",0) > 0:
                                                with st.container(border=True):
                                                    
                                                    st.success(f"Accuracy for page number {k+1} is {accuracy_docai:.2f} %",icon=":material/thumb_up:")
                                                    st.write(f"Time elapsed by Document AI is: {time_docai} || Total token used: ....")
                                                    st.write(f"Time elapsed by OpenAI is: {time_openai} || Total token used: {toketopenai}")
                                                    st.write(f"Time elapsed by Anthopic is: {time_anthropic} || Total token used: {token_anthropic}")
                                                    st.write(f"Time elapsed in Comparision is: {time_coperision} || Total token used: {openai_token_compare}")

                                                    #   st.info("File Data saved successfully")
                                            else:
                                                st.error(result)    

                                        query_count = f"SELECT count(*) FROM MORdb.Ocr_Page where Id_Pdf = {int(pdf_id)};"   
                                        count = fetch_one(query_count)     
                                        if count[0] == st.session_state.page_count:
                                            query_update = f""" UPDATE Pdf_File_Name SET Total_Pages = {int(st.session_state.page_count)}, IsOcr = {int(1)} WHERE Id_Pdf = {int(pdf_id)} ;"""
                                            execute_update(query_update)
                                            query_zip = f"""SELECT Ocr_Comparable FROM MORdb.Ocr_Page WHERE Id_Pdf = {int(pdf_id)};"""
                                            result_retrieve=fetch_all(query_zip)
                                            if result_retrieve:
                                                with st.container(border=True):
                                                    column = ["Txt"]
                                                    df =pd.DataFrame(data=result_retrieve,columns=column)
                                                    # st.dataframe(df)
                                                    text_buffer = BytesIO()
                                                    text_data = df.to_string(index=False)  # Convert DataFrame to plain text
                                                    text_buffer.write(text_data.encode("utf-8"))
                                                    text_buffer.seek(0)

                                                    zip_buffer = BytesIO()
                                                    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
                                                        zip_file.writestr("data.txt", text_buffer.getvalue())  # Add text as "data.txt" in the zip
                                                    zip_buffer.seek(0)


                                                    st.download_button(
                                                                        label="Download Data as ZIP",
                                                                        data=zip_buffer,
                                                                        file_name="data.zip",
                                                                        mime="application/zip"
                                                                    )
                                        else:
                                            st.error(f"Total number of pages is {st.session_state.page_count} but OCR done only on {count} pages")    





                                    else:
                                        print("Pages are not extracted")


                        else:
                            st.info("Please select Pdf file")                
            else:
                st.info("Please select Project name")                                
                           




def pdf_FIle_processing():
    
        user_id = st.session_state.user_id
        query = f"SELECT Id_Org,Title_Name FROM MORdb.ORG_Title where Id_user = {int(user_id)};"
        result = fetch_all(query)
        st.session_state.title_to_id_map = {title: id_org for id_org, title in result}
        # print(result)
        if result is not None:
            options=list(st.session_state.title_to_id_map.keys())
            options.insert(0,"Select")
            selected_title = st.selectbox(label="Select Project", options=options)   
            if selected_title != "Select":   
              
                print(f"Project naem {selected_title}")
                Id_org  = st.session_state.title_to_id_map[selected_title]  
                query2= f"SELECT Id_Pdf, Pdf_Name FROM Pdf_File_Name where Id_Org = {int(Id_org)} AND IsOcr = 0;"
                result2 = fetch_all(query2)
                print(result2)
                if not result2:
                    st.info(f"No pdf files are available for this project {selected_title}")

                else:    
                    st.session_state.pdf_file_to_id_map = {pdf_file: id_pad for id_pad, pdf_file in result2}
                    if result2 is not None:
                        results_list = [element for tuple_item in result2 for element in tuple_item]
                        print(f"pdf file list {results_list}")
                        print(f"pdf file {result2}")
                        options=list(st.session_state.pdf_file_to_id_map.keys())
                        options.insert(0,"Select")
                        st.session_state.select_pdf_file = st.selectbox(label="Select pdf file",options=options)
                        if st.session_state.select_pdf_file != "Select":
                            btn_pdf = st.button(label="Submit")
                            pdf_id = st.session_state.pdf_file_to_id_map[st.session_state.select_pdf_file]
                            print(st.session_state.select_pdf_file)
                            if btn_pdf:
                                user_email = st.session_state.user_email
                                st.session_state.user_file_path, st.session_state.pdf_file_path, st.session_state.image_file_path,st.session_state.txt_file_path,retrieve_mage_file_path = create_folders_users(User_file=user_email)
                                print(st.session_state.user_file_path)
                                print(st.session_state.pdf_file_path)
                                print(st.session_state.image_file_path)
                                delete_existing_files(st.session_state.pdf_file_path)
                                delete_existing_files(st.session_state.image_file_path)
                                delete_existing_files(st.session_state.txt_file_path)
                                
                                file_path1 = download_file_from_gcs(user_name=user_email,project_name=selected_title,destination_file_name=st.session_state.select_pdf_file,local_file_dir=f"{st.session_state.pdf_file_path}/{st.session_state.select_pdf_file}")
                                if file_path1 is not None:

                                    st.session_state.local_pdf_file_path = os.path.join(st.session_state.pdf_file_path,st.session_state.select_pdf_file)
                                    print(st.session_state.local_pdf_file_path)
                                    st.session_state.page_count = extract_image(st.session_state.local_pdf_file_path,st.session_state.image_file_path)
                                    if st.session_state.page_count >0:
                                        st.session_state.list_images = get_all_images_paths_list(st.session_state.image_file_path)
                                        print(st.session_state.list_images)
                                        with st.container(border=True):
                                            progress_bar = st.progress(0)
                                        with st.container(border=True):
                                            st.info(f"Total number of pages in pdf file is {st.session_state.page_count }")
                                            st.info(f"Total number of images in a extraced folder is {count_all_files(st.session_state.image_file_path)}")

                                        for k,i in enumerate(st.session_state.list_images):
                                            print(k,i)
                                            status_text =f"OCR Processing...... {k + 1}/{st.session_state.page_count}"
                                            progress_bar.progress(int(((k + 1)/(st.session_state.page_count))*100),text=status_text)
                                            # promt_txt=Prompt_txt_ocr
                                            
                                            st.session_state.image_base64 = encode_image(i)
                                            txt_docai,accuracy_docai, time_docai = st.session_state.ocr_api_list.document_ai_api(image=i)
                                            txt_anthropic,token_anthropic, time_anthropic  = st.session_state.ocr_api_list.anthropic_api(st.session_state.image_base64)
                                            txt_aponai,toketopenai, time_openai = st.session_state.ocr_api_list.open_ai_api(st.session_state.image_base64)
                                            txt_comperision, openai_token_compare, time_coperision = st.session_state.comperision_ai.merge_with_openai(doc1=txt_docai,doc2=txt_anthropic,doc3=txt_aponai)

                                           
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
                                                                    {int(pdf_id)}, 
                                                                    {int(k + 1)}, 
                                                                    {int(openai_token_compare)}, 
                                                                    '{str(time_coperision)}', 
                                                                    'Row Text', 
                                                                    '{str(datetime.now().strftime("%Y-%m-%d"))}'
                                                                );
                                                                """
                                            result = insert_data(query_insert)
                                            if result.get("rows_affected",0) > 0:
                                                with st.container(border=True):
                                                    
                                                    st.success(f"Accuracy for page number {k+1} is {accuracy_docai:.2f} %",icon=":material/thumb_up:")
                                                    st.write(f"Time elapsed by Document AI is: {time_docai} || Total token used: ....")
                                                    st.write(f"Time elapsed by OpenAI is: {time_openai} || Total token used: {toketopenai}")
                                                    st.write(f"Time elapsed by Anthopic is: {time_anthropic} || Total token used: {token_anthropic}")
                                                    st.write(f"Time elapsed in Comparision is: {time_coperision} || Total token used: {openai_token_compare}")

                                                    #   st.info("File Data saved successfully")
                                            else:
                                                st.error(result)    

                                        query_count = f"SELECT count(*) FROM MORdb.Ocr_Page where Id_Pdf = {int(pdf_id)};"   
                                        count = fetch_one(query_count)     
                                        if count[0] == st.session_state.page_count:
                                            query_update = f""" UPDATE Pdf_File_Name SET Total_Pages = {int(st.session_state.page_count)}, IsOcr = {int(1)} WHERE Id_Pdf = {int(pdf_id)} ;"""
                                            execute_update(query_update)
                                            query_zip = f"""SELECT Ocr_Comparable FROM MORdb.Ocr_Page WHERE Id_Pdf = {int(pdf_id)};"""
                                            result_retrieve=fetch_all(query_zip)
                                            if result_retrieve:
                                                with st.container(border=True):
                                                    column = ["Txt"]
                                                    df =pd.DataFrame(data=result_retrieve,columns=column)
                                                    # st.dataframe(df)
                                                    text_buffer = BytesIO()
                                                    text_data = df.to_string(index=False)  # Convert DataFrame to plain text
                                                    text_buffer.write(text_data.encode("utf-8"))
                                                    text_buffer.seek(0)

                                                    zip_buffer = BytesIO()
                                                    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
                                                        zip_file.writestr("data.txt", text_buffer.getvalue())  # Add text as "data.txt" in the zip
                                                    zip_buffer.seek(0)


                                                    st.download_button(
                                                                        label="Download Data as ZIP",
                                                                        data=zip_buffer,
                                                                        file_name="data.zip",
                                                                        mime="application/zip"
                                                                    )
                                        else:
                                            st.error(f"Total number of pages is {st.session_state.page_count} but OCR done only on {count} pages")    





                                    else:
                                        print("Pages are not extracted")


                        else:
                            st.info("Please select Pdf file")                
            else:
                st.info("Please select Project name")                                
                           






with st.container(border=True):
   pdf_processing()
                      
