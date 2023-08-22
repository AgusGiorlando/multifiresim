from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from .simulation_service import run_simulation
from .simulation import Simulation
from typing import Optional

app = FastAPI()


@app.get("/")
def index():
    return {"message": "Hola"}


@app.post("/simulate")
async def simulate(simulation: Simulation):
    try:
        result_filepath = await run_simulation(simulation)
        return FileResponse(result_filepath)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
