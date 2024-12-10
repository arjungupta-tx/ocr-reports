from openai import OpenAI
import base64
import json
import os
from urllib.parse import urlparse
from pydantic import BaseModel
from src.loging import logger



def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')
    



def openai_ocr(base64_img,api_key,models,prompt):
    try:
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
            max_tokens=6000,
        )

        txt_respone = response.choices[0].message.content
        total_token = response.usage.total_tokens

        return (txt_respone,total_token)
    except Exception as e:
        print(f"Error in openai_ocr funtion and error is {e}")
        logger.error(f"Error in openai_ocr funtion and error is {e}")




def merge_documents_with_openai(doc1, doc2, doc3,openai_key):
    try:
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
    

    except Exception as e:
        print(f"Error in merge_documents_with_openai function and error is {e}")
        logger.error(f"Error in merge_documents_with_openai function and error is {e}")


# class ResearchPaperExtraction(BaseModel):
#     Instrument_Type: str
#     Grantor: list[str]
#     Grantee: list[str]
#     Volume_Page: list[str]
#     Effective_Date: str
#     Execution_Date: str
#     File_Date: str
#     Legal_Description: str
#     Transferred_Interests: str
#     Reserved_Rights: str
#     Conditional_Rights: str
#     Rights: str
#     Remarks: str

# def runsheet_generation(doc,openai_key):

#     try:
#         System_Prompt = """ 
        
#         You are a legal expert specializing in property law and land transactions. Extract the following details from the provided legal land document and proide output in valid JSON format:

#         Examples:

#         {
#     "Instrument Type": "Court Case Judgment",
#     "Grantor": "District Court of Liberty County, Texas",
#     "Grantee": "Jennie M. Braggard and A. Braggard",
#     "Volume/Page": "Volume L, Pages 461-62",
#     "Effective Date": "November 19, 1919",
#     "Execution Date": "August 30, 1919",
#     "File Date": "November 19, 1919",
#     "Legal Description": "Beginning at the N.W. corner of the Hugh Morgan League, at a point 5000 vrs N 10° W from the Hannah Nash North line at its intersection of Cedar Bayou on the West side of said Bayou, which is the N.W. corner of Hugh Morgan, as described in the title.",
#     "Transferred Interests": "All rights, title, and interest in the land described, except for the land adjudged to Defendants Isa Jones and J.D. Staygall.",
#     "Reserved Rights": "None specified",
#     "Conditional Rights": "None specified",
#     "Rights": "NA",
#     "Remarks": "The judgment was set aside for Isa Jones and J.D. Staygall but remained in effect against C.C. Francisco. The Plaintiffs recovered all lands in controversy except those adjudged to Isa Jones and J.D. Staygall."
#     }
            


#         """
        

#         user_propmt =f""" 

#     Extract the following information from the provided legal land document {doc} and return it in JSON format:

#     Instrument Type: Type of document or transaction (e.g., deed, mortgage). If no specific type is listed, provide a brief description.
#     Grantor: Name(s) of the person or entity transferring rights. If the document is a probate, will, last will and testament, or death certificate, list who died. If it is a court case, provide the name of the court. If the document is a ratification or affidavit, identify who requested the ratification or affidavit.
#     Grantee: Name(s) of the person or entity receiving rights. If the document is a probate, will, or last will and testament, list the beneficiaries. If it is a ratification or affidavit, provide the countersigning party.
#     Volume/Page: Reference number for locating the document in legal records.
#     Effective Date: Date when the document's terms take effect. If not explicitly stated, use the latest date near a signature block.
#     Execution Date: Date when the document was signed.
#     File Date: Date when the document was officially filed, if available.
#     Legal Description: Description of the property being transferred, often listed in terms of Parcels, Lots, Blocks, or as a metes and bounds description.
#     Transferred Interests: Specify the real estate interests being transferred, such as mineral rights, royalty interests, production rights, lease rights, surface rights, or other specified interests. If all rights are being transferred, indicate "All rights, title, and interest."
#     Reserved Rights: List any rights explicitly retained or reserved by the grantor, such as overriding royalty interests, rights to minerals at certain depths, or similar retained interests.
#     Conditional Rights: Identify any conditional rights, options, or triggering circumstances that apply to the transfer, such as rights held by production for a certain timeframe or rights that require specific conditions to be effective.
#     Rights:What are the real estate interests in the land described in the legal description that are being tranfered in this agreement? Often the transfered interests involve mineral rights, mineral rights to certain depths, royalty interests, working interests, production rights, lease rights, surface rights, right of ingress, right of egress, or other similar interests., return "NA".
#     Remarks: Any additional notes or comments that would be helpful to a Landman researching the chain of title for mineral or leasehold rights of this property in Texas.



#     Make sure your response must be in json format


#     """
        

#         client = OpenAI(api_key=openai_key)

#         completion = client.chat.completions.create(
#                                                         model="gpt-4o",
#                                                         messages=[
#                                                             {"role": "system", "content": System_Prompt},
#                                                             {
#                                                                 "role": "user",
#                                                                 "content": user_propmt
#                                                             }
#                                                         ],
#                                                         response_format= { "type": "json_object" },
#                                                         temperature=0.20
#                                                     )
#         result = completion.choices[0].message.content
#         total_token = completion.usage.total_tokens
#         return result,total_token
    

#     except Exception as e:
#         print(f" Error in runsheet_generation funtion and error is {e}")
#         logger.error(f" Error in runsheet_generation funtion and error is {e}")





# from openai import OpenAI
def runsheet_generation(doc,openai_key):

    try:
        System_Prompt = """ 
        
        **You are a legal expert extraction algorithm specializing in property law and land transactions.**
        **Extract the following details from the provided legal land document and proide output in valid JSON format.**
        
        **You have to think step by step.**

        
        Step 1: Please check, Is there evidence that there are multiple full legal documents present in this file?

              substep: IF YES:Exctract that information separately as Stub Documents.

              substep: IF NO: Is there evidence of partial additional legal documents that may have been incidentally on the same county recording page in this file?

              substep: IF YES: Ignore all partial documents.

        Step 2: Instrument Type: Extract out  What type of legal instrument or document is in this file (deed, oil and gas lease, quitclaim, death certificate, option to lease, will and testament, etc.)? If the type is an amendment, return what kind of instrument it is amending.
            
             substeps: based on Instrument Type excract the following information Recording Information,Recording Date,Execution Date,Effective Date,Grantor(s),Grantee(s),Property Description.Reservations,Conditions

              
        Examples:
               
                {

                "runsheet":
                            {
                        "Instrument Type": "Court Case Judgment",
                        "Recording Information" : "No. 2529, County Court of Matagorda County, Texas",
                        "Recording Date" : "August 30, 1919"
                        "Grantor(s)": "District Court of Liberty County, Texas",
                        "Grantee(s)": "Jennie M. Braggard and A. Braggard",
                        "Volume/Page": "Volume L, Pages 461-62",
                        "Effective Date": "November 19, 1919",
                        "Execution Date": "August 30, 1919",
                        "Recording Date": "November 19, 1919",
                        "Property Description": "Beginning at the N.W. corner of the Hugh Morgan League, at a point 5000 vrs N 10° W from the Hannah Nash North line at its intersection of Cedar Bayou on the West side of said Bayou, which is the N.W. corner of Hugh Morgan, as described in the title.",
                        "Reservations": "All rights, title, and interest in the land described, except for the land adjudged to Defendants Isa Jones and J.D. Staygall.",
                        "Reserved Rights": "None specified",
                        "Conditions": "None specified",
                        },
                "Stub Documents": {
                                 
                                 "Document": "Stub Documents Details........"
                
                }


        -Make sure Stubs docments other information of same file should be store in "Stub Documents" in json during return.        

                        


        """
        

        user_propmt =f""" 

    Extract Informational Step by Step. Here is Steps.

     Step 1: Please check, Is there evidence that there are multiple full legal documents present in this file?

              substep: IF YES:Exctract that information separately as Stub Documents.

              substep: IF NO: Is there evidence of partial additional legal documents that may have been incidentally on the same county recording page in this file?

              substep: IF YES: Ignore all partial documents.

        Step 2: Instrument Type: Extract out  What type of legal instrument or document is in this file (deed, oil and gas lease, quitclaim, death certificate, option to lease, will and testament, etc.)? If the type is an amendment, return what kind of instrument it is amending.
            
             substeps: based on Instrument Type excract the following information Recording Information,Recording Date,Execution Date,Effective Date,Grantor(s),Grantee(s),Property Description.Reservations,Conditions
        
        Step 3: Use Instructions based on below condtion.

                ""If Instrument Type is Deed:""
                        
                       Recording Information : Tell me the informaiton that is used by the county to identify and record this document. That information is generally in The form of the county in which the document was recorded for public record, A volume and page number, A recording date, or A recording number and other recording information, Return all of the details about how the county identifies and records this document.
                       Recording Date : What is the date on which the deed was recorded or filed with the county?
                       Execution Date : What is the latest date on which a grantor or grantee signed the document?
                       Effective Date : What is the date of the transfer of ownership?
                       Grantor(s) : Who is selling the property or rights?
                       Grantee(s) : Who is buying the property or rights?
                       Property Description: What is the description of the property being transferred?
                       Reservations: Is there any property or rights which are explicitly excluded from the transaction by the Grantor(s)?
                       Conditions:Are there any conditions that must be met after the effective date to finalize or avoid reversion of the sale?



                ""If Instrument Type is Lease:""  

                    Recording Information : Extract the information of recorded country,A volume and page number, A recording date, or A recording number and other recording information. Make sure all information must be in one column which is "Recording Information".
                    Recording Date : What is the date on which the lease was recorded or filed with the county?
                    Execution Date : What is the latest date on which a lessor or lessee signed the document?
                    Effective Date : What is the date the lease is effective?
                    Grantor(s) : Who is granting rights under this lease?
                    Grantee(s) : Who is receiving rights under this lease?
                    Property Description : What is the description of the rights being transferred, including a description of the land they are associated with?
                    Reservations : Are there rights which are explicitly excluded from the transaction by the lessors?
                    Conditions : Are there any conditions that must be met after the effective date to finalize, maintain, or extend the lease?  


                ""If Instrument Type is Release:""

                    Recording Information : Extract the information of recorded country,A volume and page number, A recording date, or A recording number and other recording information. Make sure all information must be in one column which is "Recording Information".
                    Recording Date : What is the date on which the release was recorded or filed with the county?
                    Execution Date : What is the latest date on which the release was signed?
                    Effective Date : What is the date that the release went into effect?
                    Grantor(s) : Who is releasing the rights or property?
                    Grantee(s) : Who is gaining the rights or property?
                    Property Description : What is the description of the rights or property being transferred, including a description of the land they are associated with?
                    Reservations : Are there rights which are explicitly excluded from the release?
                    Conditions : Are there any conditions that must be met after the effective date to finalize or avoid negating the release?   


               ""If Instrument Type is Waiver:""

                    Recording Information : Extract the information of recorded country,A volume and page number, A recording date, or A recording number and other recording information. Make sure all information must be in one column which is "Recording Information".
                    Recording Date : What is the date on which the release was recorded or filed with the county?
                    Execution Date : What is the latest date on which the release was signed?
                    Effective Date : What is the date that the release went into effect?
                    Grantor(s) : Who is releasing the rights or property?
                    Grantee(s) : Who is gaining the rights or property?
                    Property Description : What is the description of the rights or property being transferred, including a description of the land they are associated with?
                    Reservations : Are there rights which are explicitly excluded from the release?
                    Conditions : Are there any conditions that must be met after the effective date to finalize or avoid negating the release? 

                ""If Instrument Type is Quitclaim:""

                    Recording Information : Extract the information of recorded country,A volume and page number, A recording date, or A recording number and other recording information. Make sure all information must be in one column which is "Recording Information".
                    Recording Date : What is the date on which the quitclaim was recorded or filed with the county?
                    Execution Date : What is the latest date on which the quitclaim was signed?
                    Effective Date : What is the date that the quitclaim went into effect?
                    Grantor(s) : Who is releasing the rights or property?
                    Grantee(s) : Who is gaining the rights or property?
                    Property Description : What is the description of the rights or property being transferred, including a description of the land they are associated with?
                    Reservations : Are there rights which are explicitly excluded from the quitclaim?
                    Conditions : Are there any conditions that must be met after the effective date to finalize the quitclaim?

               ""If Instrument Type is Option:""

                    Recording Information : Extract the information of recorded country,A volume and page number, A recording date, or A recording number and other recording information. Make sure all information must be in one column which is "Recording Information".
                    Recording Date : What is the date on which the option was recorded or filed with the county?
                    Execution Date : What is the latest date on which the option was signed?
                    Effective Date : What is the date that the option went into effect?
                    Grantor(s) : Who granted the option?
                    Grantee(s) : Who received the option right?
                    Property Description : What is the description of the rights or property being optioned, including a description of the land they are associated with?
                    Reservations : Are there rights which are explicitly excluded from the option?
                    Conditions : How long is the option and what are the conditions that must be met to exercise the option?

               
               ""If Instrument Type is Easement or Right of Way:""

                    Recording Information : Extract the information of recorded country,A volume and page number, A recording date, or A recording number and other recording information. Make sure all information must be in one column which is "Recording Information".
                    Recording Date : What is the date on which the easement was recorded or filed with the county?
                    Execution Date : What is the latest date on which the easement was signed?
                    Effective Date : What is the date that the easement went into effect?
                    Grantor(s) : Who granted the easement?
                    Grantee(s) : Who received the easement?
                    Property Description : What is the description of the rights of the easement, including a description of the land they cover?
                    Reservations : Are there rights which are explicitly excluded from the easement?
                    Conditions : Are there any conditions that must be met after the effective date to finalize or continue the easement?    


              ""If Instrument Type is Ratification:""

                    Recording Information : Extract the information of recorded country,A volume and page number, A recording date, or A recording number and other recording information. Make sure all information must be in one column which is "Recording Information".
                    Recording Date : What is the date on which the ratification was recorded or filed with the county?
                    Execution Date : What is the latest date on which the ratification was signed?
                    Effective Date : What is the date that the ratification went into effect?
                    Grantor(s) : Who was the grantor in the agreement being ratified?
                    Grantee(s) : Who is the grantee in the agreement being ratified?
                    Property Description : What rights or property are being confirmed or transfered in this ratification, including a description of the land involved?
                    Reservations : Are there rights or property which are explicitly excluded from the ratification?
                    Conditions : What conditions were met to ratify the original agreement? Are there any remaining conditions?



              ""If Instrument Type is Affidavit:""

                    Recording Information : Extract the information of recorded country,A volume and page number, A recording date, or A recording number and other recording information. Make sure all information must be in one column which is "Recording Information".
                    Recording Date : What is the date on which the affidavit was recorded or filed with the county?
                    Execution Date : What is the latest date on which the affidavit was signed?
                    Effective Date : Return: N/A
                    Grantor(s) : Who was attesting to the information provided?
                    Grantee(s) : Return: N/A
                    Property Description : What is being attested to in the affidavit?
                    Reservations : Return: N/A
                    Conditions : Return: N/A     

                    
               ""If Instrument Type is Probate:""

                    Recording Information : Extract the information of recorded country,A volume and page number, A recording date, or A recording number and other recording information. Make sure all information must be in one column which is "Recording Information".
                    Recording Date : What is the date on which the probate was recorded or filed with the county?
                    Execution Date : What is the latest date on which the probate document was signed?
                    Effective Date : What is the effective date of the probate document?
                    Grantor(s) : Who died?
                    Grantee(s) : Who are the heirs or beneficiaries that will receive property?
                    Property Description : List each heir or beneficiary of probate and what assets they received
                    Reservations : Return: N/A
                    Conditions : List each heir or beneficiary of probate and whether there are conditions that must be met for them to receive assets?   


              ""If Instrument Type is Will and Testament:""

                    Recording Information : Extract the information of recorded country,A volume and page number, A recording date, or A recording number and other recording information. Make sure all information must be in one column which is "Recording Information".
                    Recording Date : What is the date on which the will was recorded or filed with the county?
                    Execution Date : What is the latest date on which the will was signed?
                    Effective Date :Return: N/A
                    Grantor(s) : Who died?
                    Grantee(s) : Who are the heirs or beneficiaries that will receive property?
                    Property Description : List each heir or beneficiary of the will and what assets they received.
                    Reservations : Return: N/A
                    Conditions : List each heir or beneficiary of the will and whether there are conditions that must be met for them to receive assets? 

              ""If Instrument Type is Death Certificate:""

                    Recording Information : Extract the information of recorded country,A volume and page number, A recording date, or A recording number and other recording information. Make sure all information must be in one column which is "Recording Information".
                    Recording Date : What is the date of the death certificate?
                    Execution Date : Return: N/A
                    Effective Date :Return: N/A
                    Grantor(s) : Who died?
                    Grantee(s) : Return: N/A
                    Property Description : Return: N/A
                    Reservations : Return: N/A
                    Conditions : Return: N/A  

              ""If Instrument Type is Obituary:""

                    Recording Information : Extract the information of recorded country,A volume and page number, A recording date, or A recording number and other recording information. Make sure all information must be in one column which is "Recording Information".
                    Recording Date : What is the date of the obituary?
                    Execution Date : Return: N/A
                    Effective Date :Return: N/A
                    Grantor(s) : Who died?
                    Grantee(s) : Who are the surviving family members and what is their connection to the deceased?
                    Property Description : Return: N/A
                    Reservations : Return: N/A
                    Conditions : Return: N/A     



              ""If Instrument Type is Divorce:""

                    Recording Information : Extract the information of recorded country,A volume and page number, A recording date, or A recording number and other recording information. Make sure all information must be in one column which is "Recording Information".
                    Recording Date : What is the date that the divorce filing was recorded or filed with the county?
                    Execution Date : What is the latest date on which the divorce filing was signed?
                    Effective Date : What is the effective date of the divorce finalization?
                    Grantor(s) : Who was the spouse filing for divorce?
                    Grantee(s) : Who was the other spouse?
                    Property Description : List each spouse and the property they received in the divorce
                    Reservations : Return: N/A
                    Conditions : Are there any conditions that must be met for the distribution of property to take place as described in the divorce filing?


               ""If Instrument Type is Adoption:""

                    Recording Information : Extract the information of recorded country,A volume and page number, A recording date, or A recording number and other recording information. Make sure all information must be in one column which is "Recording Information".
                    Recording Date : What is the date the adoption was recorded or filed with the county?
                    Execution Date : What is the latest date that the adoption documents were signed?
                    Effective Date : Return: N/A
                    Grantor(s) : Who was doing the adopting?
                    Grantee(s) : Who was adopted?
                    Property Description : Return: N/A
                    Reservations : Return: N/A
                    Conditions : Return: N/A   



              ""If Instrument Type is Court Case:""

                    Recording Information : Extract the information of recorded country,A volume and page number, A recording date, or A recording number and other recording information. Make sure all information must be in one column which is "Recording Information".
                    Recording Date : What is the date of the court case recording or filing with the county?
                    Execution Date : Return: N/A
                    Effective Date : What is the date that the ruling of the court case goes into effect?
                    Grantor(s) : Who is the plaintiff?
                    Grantee(s) : Who is the defendant?
                    Property Description : Does the court case ruling result in the transfer of rights or property? If so, what rights or property are transfered?
                    Reservations : Are there any rights or property explicitly excluded from the ruling?
                    Conditions : Are there any conditions that must be met in order for the transfer of rights to take place?       



                ""If Instrument Type is Assignment:""

                    Recording Information : Extract the information of recorded country,A volume and page number, A recording date, or A recording number and other recording information. Make sure all information must be in one column which is "Recording Information".
                    Recording Date : What is the date of the assignment recording or filing with the county?
                    Execution Date : What is the latest date on which party signed the assignment?
                    Effective Date : What is the effective date of the assignment?
                    Grantor(s) :Who is the grantor in this assignment?
                    Grantee(s) : Who is the grantee in this assignment?
                    Property Description : Return: N/A
                    Reservations : Return: N/A
                    Conditions : Return: N/A      



              ""If Instrument Type is Other:""

                    Recording Information : Extract the information of recorded country,A volume and page number, A recording date, or A recording number and other recording information. Make sure all information must be in one column which is "Recording Information".
                    Recording Date : What is the date on which the document was recorded or filed with the county?
                    Execution Date : What is the latest date on which party signed the document?
                    Effective Date : What is the date the document is effective?
                    Grantor(s) : Who is giving property or rights?
                    Grantee(s) : Who is receiving property or rights?
                    Property Description : What is the description of the property or rights being transferred?
                    Reservations : Is there any property or rights which are explicitly excluded from the transaction?
                    
                    Conditions   : Are there any conditions that must be met after the effective date to finalize the transfer?      




        Step 4: This step is to check stub documents or other information mention in same documens.

                substep: Please check, Is there evidence that there are multiple full legal documents present in this file?
          

                        If YSE:
                         
                             "Document": " provide details of that."

                         IF NO: 

                               "Document": Is there evidence of partial additional legal documents that may have been incidentally on the same county recording page in this file?
                                                        
                    
                                                             

    Extract the following information from the provided legal land document {doc} and return it in JSON format:

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
                                                        ],
                                                        response_format= { "type": "json_object" },
                                                        temperature=0,
                                                        top_p=1
                                                    )
        result = completion.choices[0].message.content
        total_token = completion.usage.total_tokens
        return result,total_token
    

    except Exception as e:
        print(f" Error in runsheet_generation funtion and error is {e}")
        # logger.error(f" Error in runsheet_generation funtion and error is {e}")







# 



from openai import OpenAI
def chain_of_title(doc,openai_key):

    try:
        System_Prompt = """ 

             You are a legal document relationship analyzer. Your task is to analyze structured data about land ownership records and extract meaningful relationships between the parties involved. Specifically, you need to create relationships between "Grantor" and "Grantee" for each record, including the nature of the transaction, the date it was filed, and the legal description.
For each record:
- Identify the "Grantor" (the party transferring ownership or rights).
- Identify the "Grantee" (the party receiving ownership or rights).
- Include the "File Date" of the transaction.
- Include any relevant "Instrument Type" and "Legal Description."
- Try to generate linked Json format.

if Assignemnts - Deed, Lease, Assignment, Option, Quitclaim, Easement:
        {
        "Grantor": "Name of the Grantor"
        "Instrument Type" : [Instrument Type,Execution Date,Effective ,Filed Date,-User Notes-,Transfered Rights]
        "Grantee": "Name of the Grantee",
        "Right" : Grantee (Grantor with Retained Rights)
        }

        

if Evidence - Probate, Will and Testament, Heirship:
 {
        "Grantor": "Name of the Grantor"
        "Instrument Type" : [Instrument Type,Execution Date,Effective ,Filed Date,-User Notes-,Transfered Rights]
        "Grantee": ["Name of the Grantee",]
        "Right" : Grantee (Grantor with Retained Rights),
        "Death Certificate"   :[Death Certificate Details],
        "Affidavit of Heirship": [Affidavit of Heirship Details],
        "Obituary":Obituary Details,
        "Adoption / Divorce":Adoption / Divorce Details
        }

"""
        

        user_propmt =f""" 

Analyze the following data and generate the relationship as specified:
Create chain of title like node and edge.
Make sure utilised all row of dataframe.

Must include all grantor and grantee name.


use this dataframe :{doc}




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
                                                        ],
                                                        # response_format= { "type": "json_object" },
                                                        temperature=1,
                                                        top_p=1
                                                    )
        result = completion.choices[0].message.content
        total_token = completion.usage.total_tokens
        return result,total_token
    

    except Exception as e:
        print(f" Error in runsheet_generation funtion and error is {e}")
        # logger.error(f" Error in runsheet_generation funtion and error is {e}")
