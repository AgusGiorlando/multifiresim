import logging
import os
from pydantic import BaseModel
from fastapi import FastAPI
from fastapi.responses import FileResponse
from .simulation.simulation import Simulation
from .simulation.simulation_service import run_simulation
import traceback

app = FastAPI()

@app.get("/")
def index():
    version = "0734"
    return {"message": "Firesim " + version}

@app.post("/simulate")
async def simulate(simulation: Simulation):
    try:
        result_filename = await run_simulation(simulation)
        result_filepath = os.path.join("/api/results", result_filename)
        return FileResponse(result_filepath)
    except Exception as e:
        just_the_string = traceback.format_exc()
        return {"Firesim error": str(e),
                'traceback' : just_the_string}, 500