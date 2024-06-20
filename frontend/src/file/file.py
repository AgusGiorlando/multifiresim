from pydantic import BaseModel

class File(BaseModel):
    name: str
    content: str

    class Config:
        validate_assignment = True
        orm_mode = True
