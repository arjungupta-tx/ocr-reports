from google.api_core.client_options import ClientOptions
from google.cloud import documentai
import base64
from anthropic import Anthropic
from dotenv import load_dotenv
from google.oauth2 import service_account
from pathlib import Path
import os
import streamlit as st



MIME_TYPE ='image/png'


def remove_first_line_if_number(text):
    lines = text.split('\n')
    
    # Check if the first line contains only digits
    if lines[0].strip().isdigit():
        lines = lines[1:]  # Remove the first line
    
    return '\n'.join(lines)


def ocr_doc(FILE_PATH:Path):
    load_dotenv()
    PROJECT_ID = os.getenv('PROJECT_ID')
    LOCATION =  os.getenv('LOCATION')  
    PROCESSOR_ID = os.getenv('PROCESSOR_ID') 
    credentials = service_account.Credentials.from_service_account_info(st.secrets["gcs_connections"])
  

    try:
       
        
       if FILE_PATH is not None:
           #Instantiates a client
        docai_client = documentai.DocumentProcessorServiceClient(client_options=ClientOptions(api_endpoint=f"{LOCATION}-documentai.googleapis.com"),credentials=credentials)

        # The full resource name of the processor, e.g.:
        # projects/project-id/locations/location/processor/processor-id
        # You must create new processors in the Cloud Console first
        RESOURCE_NAME = docai_client.processor_path(PROJECT_ID, LOCATION, PROCESSOR_ID)

        # Read the file into memory
        with open(FILE_PATH, "rb") as image:
            image_content = image.read()

        # Load Binary Data into Document AI RawDocument Object
        raw_document = documentai.RawDocument(content=image_content, mime_type=MIME_TYPE)

        # Configure the process request
        request = documentai.ProcessRequest(name=RESOURCE_NAME, raw_document=raw_document)

        # Use the Document AI client to process the sample form
        result = docai_client.process_document(request=request)

        document_object = result.document
        # lines = document_object.text.split('\n')
        # if lines[0].strip().isdigit():
        #     lines = lines[1:]  
        # txt = '\n'.join(lines)
        accuracy= (result.document.pages[0].layout.confidence)*100
        # return remove_first_line_if_number(document_object.text), accuracy
        return document_object.text, accuracy
        # print("Document processing complete.")
        # print(f"Text: {document_object.text}")
                
       
    except Exception as e:
       raise e
       




