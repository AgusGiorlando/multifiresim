from pydantic import BaseModel


class Simulation(BaseModel):
    file_id:str
    model: str
    windSpd: float
    windDir: float
    start_time: float
    end_time: float
    
    class Config:
        validate_assignment = True
        arbitrary_types_allowed = True