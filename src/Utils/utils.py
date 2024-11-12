import os
import pymupdf
import re
from PIL import Image
from pathlib import Path
from src.entity_variables.globals import *
import streamlit as st
import os
import zipfile
import io




def create_folders(pdf_process_dir= "pdf_process_dir", 
                   pdf_folder_dir = "pdf_folder_dir", 
                   Extracted_Image_dir = "Extracted_Image_dir", 
                   Extracted_txt_dir = "Extracted_txt_dir",
                   Zip_File_Dir = "Zip_File_Dir"
                   ):

    try:
        # Define the parent folder path
        parent_path = Path(pdf_process_dir)

        # Define the subfolder paths
        Pdf_Folder_Path = parent_path / pdf_folder_dir
        Extracted_Image_path = parent_path / Extracted_Image_dir
        Extracted_txt_path = parent_path / Extracted_txt_dir
        Zip_File_path = parent_path / Zip_File_Dir

        # Create the parent folder and subfolders
        Pdf_Folder_Path.mkdir(parents=True, exist_ok=True)
        Extracted_Image_path.mkdir(parents=True, exist_ok=True)
        Extracted_txt_path.mkdir(parents=True, exist_ok=True)
        Zip_File_path.mkdir(parents=True, exist_ok=True)

        # Return the paths of the subfolders
        return Pdf_Folder_Path, Extracted_Image_path, Extracted_txt_path,Zip_File_path
    except Exception as e:
        raise e
    


def create_folders_users(pdf_process_dir= "pdf_process_dir", 
                   User_file = "userfilename", 
                   pdf_file = "pdf_files", 
                   image_file = "image_files",
                   txt_file = "txt_file",
                   retreve_images = "retrieve_image"
                  
                   ):

    try:
        # Define the parent folder path
        parent_path = Path(pdf_process_dir)

        # Define the subfolder paths
        parent_dir = parent_path / User_file
        pdf_folder_dir = parent_dir / pdf_file
        image_dir = parent_dir / image_file
        txt_dir = parent_dir / txt_file
        retrieve_image = parent_dir / retreve_images
        

        # Create the parent folder and subfolders
        parent_dir.mkdir(parents=True, exist_ok=True)
        pdf_folder_dir.mkdir(parents=True, exist_ok=True)
        image_dir.mkdir(parents=True, exist_ok=True)
        txt_dir.mkdir(parents=True,exist_ok=True)
        retrieve_image.mkdir(parents=True,exist_ok=True)
       

        # Return the paths of the subfolders
        return parent_dir, pdf_folder_dir, image_dir,txt_dir,retrieve_image
    except Exception as e:
        raise e    



def extract_image(pdf_path,image_dir):
       
       try:
 
        # pdf_name = os.path.splitext(os.path.basename(pdf_path))[0]
        #    output_dir = f"Extracted_Image_png{pdf_name}"
        os.makedirs(image_dir, exist_ok=True)
        doc = pymupdf.open(pdf_path)
        # Page_count_pdf = doc.page_count
        Page_count_pdf = doc.page_count
        # print(Page_count_pdf)
        # print(doc.page_count)
        # pdf_name = os.path.splitext(os.path.basename(pdf_path))[0]
        for page_num in range(len(doc)):
                page = doc.load_page(page_num)  # get page
                pix = page.get_pixmap()  # extract images
                image_name =  f"page_{page_num + 1}"+"."+"png"
                path_file = os.path.join(image_dir,image_name)
                Image.frombytes("RGB", [pix.width, pix.height], pix.samples).save(path_file,format='png')
                jpeg_image = Image.open(path_file)
                jpeg_image.save(path_file)

        return Page_count_pdf

       except Exception as e:
           raise e




def delete_existing_files(folder):
    for filename in os.listdir(folder):
        if filename is not None:

            file_path = os.path.join(folder, filename)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)  # Delete the file
            except Exception as e:
                # st.error(f"Error deleting file {file_path}: {e}")      
                raise e 
        



def count_all_files(directory_path):
    """
    Count all files in a directory and its subdirectories.

    Args:
        directory_path (str): The path of the directory.

    Returns:
        int: The total number of files.
    """
    total_files = 0
    
    for root, dirs, files in os.walk(directory_path):
        total_files += len(files)
    
    return total_files     




# def get_all_images_paths_list(directory):
#     file_paths = []
    
#     # Walk through the directory
#     for root, dirs, files in os.walk(directory):
#         for file in files:
#             # Join root and file name to get full path
#             file_paths.append(os.path.join(root, file))
    
#     return sorted(file_paths)


def get_all_images_paths_list(directory):
    # List all files in the specified directory
    file_paths = [os.path.join(directory, file) for file in os.listdir(directory)]
    
    # Filter out non-files (just in case there are subdirectories)
    file_paths = [f for f in file_paths if os.path.isfile(f)]
    
    # Sort the files numerically by the number at the end of the filename
    file_paths.sort(key=lambda f: int(re.search(r'\d+', os.path.basename(f)).group()))
    
    return file_paths



def write_txt_to_folder(folder_path, file_name,content):
    """
    Writes the given content to a text file in the specified folder.

    Args:
        file_path (str): The full path to the desired file, including the filename and extension.
        content (str): The content to be written to the file.
    """

    try:
        # Create the folder if it doesn't exist
        # folder_path = os.path.dirname(file_path)
        # os.makedirs(folder_path, exist_ok=True)
        file_path = os.path.join(folder_path, file_name)

        # Write the content to the file
        with open(file_path, 'w') as f:
            f.write(content)

        print(f"File '{file_path}' written successfully.")
    except Exception as e:
        print(f"Error writing file: {e}")    








def zip_folder(folder_path, output_zip):
    # Create a ZipFile object in write mode
    with zipfile.ZipFile(output_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
        # Walk through all the files and directories in the folder
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                # Add file to zip archive
                zipf.write(file_path, os.path.relpath(file_path, folder_path))