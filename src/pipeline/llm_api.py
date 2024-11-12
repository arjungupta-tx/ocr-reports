from src.api_components.openai import merge_documents_with_openai
from src.entity_variables.llm_api_entity import OpenaiKeyVariables
from src.entity_variables.promt import prompt_for_merge_document
import time





class LLM_API_LIST:
    def __init__(self) -> None:
        self._OpenaiKeyVariables = OpenaiKeyVariables()
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
