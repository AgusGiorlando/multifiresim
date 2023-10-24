from pydantic import BaseModel

class Simulation(BaseModel):
    result_filename: str
    model: str
    slope: str
    file_ign: str
    start_time: str
    end_time: str
