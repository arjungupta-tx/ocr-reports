from src.api_components.openai import merge_documents_with_openai,runsheet_generation,chain_of_title
from src.api_components.anthropic import chai_of_title_anthropic
from src.entity_variables.llm_api_entity import OpenaiKeyVariables,AnthropicKeyVariables
from src.entity_variables.promt import prompt_for_merge_document
import time





class LLM_API_LIST:
    def __init__(self) -> None:
        self._OpenaiKeyVariables = OpenaiKeyVariables()
        self._AnthropicKeyVariables = AnthropicKeyVariables()
        # self._prompt_for_merge_document = prompt_for_merge_document



    def merge_with_openai(self,doc1, doc2, doc3):

        start_time = time.time()

        txt_merge, tokensopenai = merge_documents_with_openai(doc1=doc1,
                                    doc2=doc2,
                                    doc3=doc3,
                                    openai_key=self._OpenaiKeyVariables.openai_api_key
                                    )
        
        end_time = time.time()
        elapsed_time_sec = end_time - start_time

        # Convert to minutes and seconds
        minutes = int(elapsed_time_sec // 60)
        seconds = elapsed_time_sec % 60

        total_time_comperision = f"{minutes} min {seconds:.2f} sec" if minutes > 0 else f"{seconds:.2f} seconds"

        return txt_merge, tokensopenai,total_time_comperision    




    def runsheet(self,doc):

        resut,token = runsheet_generation(doc=doc,openai_key=self._OpenaiKeyVariables.openai_api_key)

        return resut,token
    



    def chai_of_title(self,doc):

        resut,token = chain_of_title(doc=doc,openai_key=self._OpenaiKeyVariables.openai_api_key)

        return resut,token
    

    def chai_of_title_anthropic(self,doc):

        resut,token = chai_of_title_anthropic(doc=doc,api_key=self._AnthropicKeyVariables.anthropict_api_key,MODEL_NAME=self._AnthropicKeyVariables.anthropic_model)

        return resut,token

