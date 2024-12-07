import base64
# from anthropic import Anthropic
from pathlib import Path
import anthropic
from src.loging import logger

# MODEL_NAME = "claude-3-opus-20240229"




def get_base64_encoded_image(image_path):
    with open(image_path, "rb") as image_file:
        binary_data = image_file.read()
        base_64_encoded_data = base64.b64encode(binary_data)
        base64_string = base_64_encoded_data.decode('utf-8')
        return base64_string
    


def ocr_anthropic(image_strin:base64,api_key,prompt:str,MODEL_NAME:str):
    client = anthropic.Anthropic(api_key=api_key)

    try:

        message_list = [
                            {
                                "role": 'user',
                                "content": [
                                    {"type": "image", "source": {"type": "base64", "media_type": "image/png", "data": image_strin}},
                                    {"type": "text", "text": prompt}
                                    #"Transcribe this text. Only output the text and nothing else."
                                ]
                            }
                        ]

        response = client.messages.create(
            model=MODEL_NAME,
            max_tokens=6000,
            messages=message_list
        )
        
        total_tokens = response.usage.input_tokens + response.usage.output_tokens
        return response.content[0].text , total_tokens
    

    except Exception as e:
        print(f"Error in ocr_anthropic funcion and error is {e}")
        logger.error(f"Error in ocr_anthropic funcion and error is {e}")
   



def chai_of_title_anthropic(doc,api_key,MODEL_NAME = "claude-3-5-sonnet-latest"):
    client = anthropic.Anthropic(api_key=api_key)

    
    prompt_system ="""

  You are a helpful AI assistant designed to analyze land records and identify relationships between transactions. You are provided with data from an Excel sheet containing land ownership records with the following columns:

* **Instrument Type:** The type of legal document (e.g., Deed, Mortgage, Release)
* **Grantor:** The person or entity transferring ownership
* **Grantee:** The person or entity receiving ownership
* **Volume/Page:**  Reference for the recorded document
* **Effective Date:** The date the transfer is legally in effect
* **Execution Date:** The date the document was signed 
* **File Date:** The date the document was officially filed
* **Legal Description:** The legal description of the property
* **Transferred Interests:**  Specific interests transferred (e.g., Fee Simple, Mineral Rights) 
* **Reserved Rights:** Rights kept by the Grantor
* **Conditional Rights:** Rights granted with conditions
* **Rights:**  General description of rights involved
* **Remarks:**  Additional notes
* **Documents:**  Links to document images or PDFs 

Your goal is to help identify chains of title, showing how ownership of land has passed from one party to another over time.


 """

    prompt_user =f""" 
  Create Chain of title:

Analyze the following data and generate the relationship as specified:
Relationship must be linked to each other and also display associated data
And Create Chain of title using {doc}
"""

    try:

        message_list = [
            
                            {
                                "role": 'user',
                                "content": [
                                    
                                    {"type": "text", "text": prompt_user}
                                    #"Transcribe this text. Only output the text and nothing else."
                                ]
                            }
                        ]

        response = client.messages.create(
            model=MODEL_NAME,
            system=prompt_system,
            max_tokens=8192,
            
            messages=message_list
        )
        
        total_tokens = response.usage.input_tokens + response.usage.output_tokens
        return response.content[0].text , total_tokens
    

    except Exception as e:
        print(f"Error in ocr_anthropic funcion and error is {e}")
        logger.error(f"Error in ocr_anthropic funcion and error is {e}")
   
