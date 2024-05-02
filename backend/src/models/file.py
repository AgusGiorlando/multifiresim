from pydantic import BaseModel

class File(BaseModel):
    name: str
    content:str
    
    class Config:
        validate_assignment = True
        arbitrary_types_allowed=True