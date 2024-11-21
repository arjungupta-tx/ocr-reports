from src.api_components.anthropic import ocr_anthropic
from src.api_components.documentsai import ocr_doc
from src.api_components.openai import openai_ocr
from src.Utils.common import encode_image
from src.entity_variables.llm_api_entity import AnthropicKeyVariables,OpenaiKeyVariables,DocumentaiKeyVariables
from dotenv import load_dotenv
from google.oauth2 import service_account
import time
from src.loging import logger








class OCR_API_LIST:
    def __init__(self) -> None:
        
        self._AnthropicKeyVariables = AnthropicKeyVariables()
        self._OpenaiKeyVariables = OpenaiKeyVariables()
        # self._DocumentaiKeyVariables = DocumentaiKeyVariables()


    def anthropic_api(self,image_base64):

        try:
        
            start_time = time.time()
            response_anthropic,token_enthropic = ocr_anthropic(image_strin=image_base64,
                                            api_key=self._AnthropicKeyVariables.anthropict_api_key,
                                            prompt=self._AnthropicKeyVariables.prompt,
                                            MODEL_NAME=self._AnthropicKeyVariables.anthropic_model)
            end_time = time.time()
            elapsed_time_sec = end_time - start_time

            # Convert to minutes and seconds
            minutes = int(elapsed_time_sec // 60)
            seconds = elapsed_time_sec % 60

            total_time_anthropic = f"{minutes} min {seconds:.2f} sec" if minutes > 0 else f"{seconds:.2f} seconds"

            return response_anthropic,token_enthropic,total_time_anthropic
        except Exception as e:
            logger.error(f"Error in anthropic_api function and erro is {e}")




    def document_ai_api(self,image):

        try:

            start_time = time.time()

            print(f"Image path {image}")


            response_documentai,accuracy_documentai = ocr_doc(FILE_PATH=image                                                         
                                                            )
            end_time = time.time()
            elapsed_time_sec = end_time - start_time

            # Convert to minutes and seconds
            minutes = int(elapsed_time_sec // 60)
            seconds = elapsed_time_sec % 60

            total_time_docai = f"{minutes} min {seconds:.2f} sec" if minutes > 0 else f"{seconds:.2f} seconds"

            return response_documentai,accuracy_documentai, total_time_docai
        except Exception as e:
            logger.error(f"Error in document_ai_api function and erro is {e}")



    def open_ai_api(self,image_base64):

        try:

            start_time = time.time()


            response_openai,token_openai = openai_ocr(base64_img=image_base64,
                                                    api_key=self._OpenaiKeyVariables.openai_api_key,
                                                    models=self._OpenaiKeyVariables.openai_model,
                                                    prompt=self._OpenaiKeyVariables.prompt)
            
            end_time = time.time()
            elapsed_time_sec = end_time - start_time

            # Convert to minutes and seconds
            minutes = int(elapsed_time_sec // 60)
            seconds = elapsed_time_sec % 60

            total_time_openai = f"{minutes} min {seconds:.2f} sec" if minutes > 0 else f"{seconds:.2f} seconds"
            


            return response_openai,token_openai,total_time_openai
        
        except Exception as e:
            logger.error(f"Error in open_ai_api function and erro is {e}")

            


