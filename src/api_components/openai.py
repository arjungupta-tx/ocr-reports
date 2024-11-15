from openai import OpenAI
import base64
import json
import os
from urllib.parse import urlparse



def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')
    



def openai_ocr(base64_img,api_key,models,prompt):
    client = OpenAI(api_key=api_key) #Best practice needs OPENAI_API_KEY environment variable
# client = OpenAI('OpenAI API Key here')

    base64 = f"data:image/png;base64,{base64_img}"

    response = client.chat.completions.create(
        model=models,
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {
                        "type": "image_url",
                        # for online images
                        # "image_url": {"url": image_url}
                        "image_url": {"url": f"{base64}"}
                    }
                ],
            }
        ],
        max_tokens=4000,
    )

    txt_respone = response.choices[0].message.content
    total_token = response.usage.total_tokens

    return (txt_respone,total_token)




def merge_documents_with_openai(doc1, doc2, doc3,openai_key):
    prompt_for_merge_document=f""" 
        I have three OCR outputs from the same document. Each OCR result may have missing sentences, incorrect text, or variations in formatting. 
        I want you to analyze the three versions and create one perfect document by combining all the accurate and missing content.


        Here are the documents:

            1. Document 1:
            {doc1}

            2. Document 2:
            {doc2}

            3. Document 3:
            {doc3}

        Your task is to:
            - Identify missing sentences or text in any of the documents.
            - Resolve inconsistencies or differences.
            - Combine all the content into one coherent, accurate document.
            - Ensure that the final document is well-formatted and complete.

            Please return the merged document. Nothing else.


        """
    

    client = OpenAI(api_key=openai_key)

    completion = client.chat.completions.create(
                                                    model="gpt-4o",
                                                    messages=[
                                                        {"role": "system", "content": "You are a helpful assistant."},
                                                        {
                                                            "role": "user",
                                                            "content": prompt_for_merge_document
                                                        }
                                                    ]
                                                )
    result = completion.choices[0].message.content
    total_token = completion.usage.total_tokens
    return result,total_token




def runsheet_generation(doc,openai_key):
    System_Prompt = """ 
     
     You are a legal expert specializing in property law and land transactions. Extract the following details from the provided legal land document and return the information in JSON format:


        


     """
    

    user_propmt =f""" 

Extract the following information from the provided legal land document {doc} and return it in JSON format:

Instrument Type: Type of document or transaction (e.g., deed, mortgage). If no specific type is listed, provide a brief description.
Grantor: Name(s) of the person or entity transferring rights. If the document is a probate, will, last will and testament, or death certificate, list who died. If it is a court case, provide the name of the court. If the document is a ratification or affidavit, identify who requested the ratification or affidavit.
Grantee: Name(s) of the person or entity receiving rights. If the document is a probate, will, or last will and testament, list the beneficiaries. If it is a ratification or affidavit, provide the countersigning party.
Volume/Page: Reference number for locating the document in legal records.
Effective Date: Date when the document's terms take effect. If not explicitly stated, use the latest date near a signature block.
Execution Date: Date when the document was signed.
File Date: Date when the document was officially filed, if available.
Legal Description: Description of the property being transferred, often listed in terms of Parcels, Lots, Blocks, or as a metes and bounds description.
Transferred Interests: Specify the real estate interests being transferred, such as mineral rights, royalty interests, production rights, lease rights, surface rights, or other specified interests. If all rights are being transferred, indicate "All rights, title, and interest."
Reserved Rights: List any rights explicitly retained or reserved by the grantor, such as overriding royalty interests, rights to minerals at certain depths, or similar retained interests.
Conditional Rights: Identify any conditional rights, options, or triggering circumstances that apply to the transfer, such as rights held by production for a certain timeframe or rights that require specific conditions to be effective.
Rights:What are the real estate interests in the land described in the legal description that are being tranfered in this agreement? Often the transfered interests involve mineral rights, mineral rights to certain depths, royalty interests, working interests, production rights, lease rights, surface rights, right of ingress, right of egress, or other similar interests., return "NA".
Remarks: Any additional notes or comments that would be helpful to a Landman researching the chain of title for mineral or leasehold rights of this property in Texas.

Use this list legal land document 

Make sure your response must be in json format


"""
    

    client = OpenAI(api_key=openai_key)

    completion = client.chat.completions.create(
                                                    model="gpt-4o",
                                                    messages=[
                                                        {"role": "system", "content": System_Prompt},
                                                        {
                                                            "role": "user",
                                                            "content": user_propmt
                                                        }
                                                    ]
                                                )
    result = completion.choices[0].message.content
    total_token = completion.usage.total_tokens
    return result,total_token