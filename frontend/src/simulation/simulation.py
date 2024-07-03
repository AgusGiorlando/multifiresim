from typing import Optional
from pydantic import BaseModel
from datetime import datetime
from bson import ObjectId

class Simulation(BaseModel):
    result_filename: str
    model: str
    windSpd: float
    windDir: float
    file_ign: str
    start_time: float
    end_time: float
    create_date: datetime

    class Config:
        validate_assignment = True