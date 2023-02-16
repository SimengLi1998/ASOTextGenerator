from pydantic import BaseModel
from typing import List, Union

class Keyword(BaseModel):
    times: int
    keyword: str

class AsoInput(BaseModel):
    gameName: str
    gameDescribe: str
    gameFeature: str
    style: int
    language: str
    # total_character: int 
    keywords: List[Keyword]  = []


class AsoInputInner(BaseModel):
    gameName: str
    gameDescribe: str
    gameFeature: str
    style: int
    language: str
    emoji:int
    total_character: int 
    keywords: List[Keyword]  = []

    
class Segment(BaseModel):
    sid: int
    scene_describe: str
    scene_text: str
    
class CodeInput(BaseModel):
    task_id: int
    code_language: str
    scene_list: Union[List[Segment], None] = None    
    
    
class PromptModel(BaseModel):
    content: str
    
    
class TextContent(BaseModel):
    text: str