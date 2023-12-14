from pydantic import BaseModel

class Simulation(BaseModel):
    result_filename: str
    model: str
    slope: float
    file_ign: str
    start_time: float
    end_time: float

    class Config:
        validate_assignment = True