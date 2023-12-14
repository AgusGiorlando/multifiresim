import httpx
from fastapi import FastAPI
from fastapi.responses import FileResponse
from simulation.simulation import Simulation
import json
import traceback


app = FastAPI()


@app.get("/")
def index():
    return {"message": "Backend"}


@app.post("/simulate")
async def simulate(simulation: Simulation):
    try:
        data = simulation.dict()        
        url = "http://firesim-service/simulate"
    
        response = httpx.post(url, json=data)
        return {'response' : FileResponse(response.content, filename=simulation.result_filename)}
        # return {'response' : type(response)}
    except Exception as e:
        traceback_str = traceback.format_exc()
        return {"Backend error": str(e),
                'traceback' : traceback_str}, 500
