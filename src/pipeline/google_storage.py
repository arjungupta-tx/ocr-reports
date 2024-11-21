from google.cloud import storage
from google.oauth2 import service_account
import streamlit as st
from src.loging import logger

credentials = service_account.Credentials.from_service_account_info(st.secrets["arjun_gcs_connection"])

def create_bucket_and_folder(project_name:str,usernmae ,folder_name_pdf,folder_name_image):
    try:
        # Initialize a Google Cloud Storage client
        client = storage.Client(project="my-project-6750-ai-2024",credentials=credentials)
        
        # Create the bucket (check if it exists first)
        # bucke_names = bucket_name.replace(" ","_")
        bucket_name = "alok-ocr"
        bucket = client.bucket(bucket_name)
        if not bucket.exists():
            bucket = client.create_bucket(bucket_name)
            print(f"Bucket '{bucket_name}' created.")
        else:
            print(f"Bucket '{bucket_name}' already exists.")

        # Define folder path within the bucket
        folder_path_pdf = f"{usernmae}/{project_name}/{folder_name_pdf}"
        folder_path_image = f"{usernmae}/{project_name}/{folder_name_image}"

        # Create a "dummy" blob to represent the folder
        blob_pdf = bucket.blob(folder_path_pdf + "/")
        blob_pdf.upload_from_string("")  # Upload an empty file to create the folder

        blob_image = bucket.blob(folder_path_image + "/")
        blob_image.upload_from_string("")  # Upload an empty file to create the folder

        print(f"Project '{project_name}' and Folder '{folder_path_pdf}' created in bucket '{bucket_name}'.")
        return f"gs://{bucket_name}/{folder_path_pdf}" + "," + f"gs://{bucket_name}/{folder_path_image}"
    
    except Exception as e:
        print(e)
        logger.error(f"error in create_bucket_and_folder function and error is {e}")
        return None
    





import streamlit as st
from google.cloud import storage

# Initialize Google Cloud Storage client


def upload_file_to_gcs(project_name, user_name, file, destination_filename):

    try:

        client = storage.Client(project="my-project-6750-ai-2024",credentials=credentials)
        # Get the bucket
        bucket_name = "alok-ocr"
        bucket = client.bucket(bucket_name)
        folder_name_pdf = "pdf_folder"
        # Define the blob path within the bucket (folder + file name)
        blob_path = f"{user_name}/{project_name}/{folder_name_pdf}/{destination_filename}"
        blob = bucket.blob(blob_path)
        
        # Upload the file-like object from Streamlit without saving locally
        blob.upload_from_file(file)
        
        # st.success(f"File uploaded to gs://{bucket_name}/{blob_path}")
        print(f"File uploaded to gs://{project_name}/{blob_path}")
        file_url = f"gs://{bucket_name}/{blob_path}"
        return file_url

    # Streamlit file uploader
        # uploaded_file = st.file_uploader("Choose a file to upload")

        # # Form submission to upload the file to Google Cloud Storage
        # if uploaded_file is not None:
        #     bucket_name = "runsheet_tilte_ocr"
        #     folder_path = "pdf_folder"  # Folder path within the bucket
        #     destination_filename = uploaded_file.name  # Use the uploaded file's name or customize it
            
        #     # Upload the file if the upload button is clicked
        #     upload_file_to_gcs(bucket_name, folder_path, uploaded_file, destination_filename)


    except Exception as e:
        print(f"Error: {e}")
        logger.error(f"error in upload_file_to_gcs function and error is {e}")
        return None



# from google.cloud import storage

def download_file_from_gcs(user_name,project_name,destination_file_name,local_file_dir):

    try:
    # Initialize the Google Cloud Storage client
        client = storage.Client(project="my-project-6750-ai-2024",credentials=credentials)
        
        # Access the bucket and blob (file)
        bucket_name = "alok-ocr"
        folder_name_pdf = "pdf_folder"
        source_blob_name= f"{user_name}/{project_name}/{folder_name_pdf}/{destination_file_name}"
        bucket = client.bucket(bucket_name)
        blob = bucket.blob(source_blob_name)
        
        # Download the blob to a local file
        blob.download_to_filename(local_file_dir)
        
        # Return a success message
        return source_blob_name
    
    except Exception as e:
        print(f"Error: {e}")
        logger.error(f"error in download_file_from_gcs function and error is {e}")
        return None


# # Usage
# bucket_name = 'your_bucket_name'
# source_blob_name = 'path/to/your_file.pdf'
# destination_file_name = 'your_file.pdf'

# result = download_file_from_gcs(bucket_name, source_blob_name, destination_file_name)
# print(result)




def upload_text_to_gcs(project_name, text_content, destination_blob_name):
    """
    Uploads a text file to the specified Google Cloud Storage bucket.
    
    Parameters:
    - bucket_name (str): The name of your GCS bucket.
    - text_content (str): The OCR-extracted text content to upload.
    - destination_blob_name (str): The name of the file in the bucket (e.g., 'foldername/file.txt').

    """
    bucket_name = "alok-ocr"
    folder_name_text = "text_folder"
    client = storage.Client(project="my-project-6750-ai-2024",credentials=credentials)
    bucket = client.get_bucket(bucket_name)
    
    # Create a blob in the bucket
    blob = bucket.blob(destination_blob_name)
    
    # Upload the text content
    blob.upload_from_string(text_content, content_type="text/plain")
    
    print(f"Text file uploaded to {destination_blob_name} in bucket {bucket_name}")

# Usage
bucket_name = "your-bucket-name"  # Replace with your actual bucket name
text_content = "Extracted OCR text here..."  # Replace with the actual OCR text
destination_blob_name = "your-folder/file.txt"  # Replace with the desired file path in GCS

upload_text_to_gcs(bucket_name, text_content, destination_blob_name)




