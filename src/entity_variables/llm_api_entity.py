from dataclasses import dataclass
from pathlib import Path
import json
from src.CONSTANT import *
from src.entity_variables.globals import Prompt_txt_ocr







@dataclass(frozen=True)
class AnthropicKeyVariables:
    
    anthropict_api_key:str = ANTHROPIC_API_KEY
    prompt:str = Prompt_txt_ocr
    anthropic_model:str = "claude-3-5-sonnet-20241022"



@dataclass(frozen=True)
class OpenaiKeyVariables:
    
    openai_api_key:str = OPEN_AI_KEY
    prompt:str = Prompt_txt_ocr
    openai_model:str = "gpt-4o"


@dataclass(frozen=True)
class DocumentaiKeyVariables:
    PROJECT_ID:str = PROJECT_ID
    LOCATION:str = LOCATION
    PROCESSOR_ID:str = PROCESSOR_ID
    credentials = credentials


