from pydantic import BaseModel

class Result(BaseModel):
    simulation_id: str
    content: str

    class Config:
        validate_assignment = True
        arbitrary_types_allowed=True