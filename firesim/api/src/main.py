import os
import traceback
from fastapi import FastAPI
from fastapi.responses import FileResponse
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
from .simulation.simulation import Simulation
from .simulation.simulation_service import run_simulation

app = FastAPI()

MONGO_URI = "mongodb://mongodb:27017/"
client = AsyncIOMotorClient(MONGO_URI)
db = client["simulation_db"]

@app.get("/")
def index():
    version = "2337"
    return {"message": "Firesim " + version}

@app.post("/simulate")
async def simulate(simulation: Simulation):
    try:
        collection = db["files"]
        file = await collection.find_one({"_id": ObjectId(simulation.file_id)})
        if file:
            result_filename = await run_simulation(simulation, file)
            result_filepath = os.path.join("/api/results", result_filename)
            return FileResponse(result_filepath)
        else:
            return {"message": "File not found"}, 404 
        
    except Exception as e:
        just_the_string = traceback.format_exc()
        return {"Firesim error": str(e),
                'traceback' : just_the_string}, 500