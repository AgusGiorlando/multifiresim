import httpx
from fastapi import FastAPI, HTTPException, Request
from models.simulation_service import saveFileImage
from models.simulation import Simulation
from models.file import File
from models.result import Result
import traceback
from datetime import datetime
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId

# Configuración de la aplicación
app = FastAPI()

# Configuración de MongoDB
MONGO_URI = "mongodb://mongodb:27017/"

client = AsyncIOMotorClient(MONGO_URI)
db = client["simulation_db"]

@app.get("/")
def index():
    return {"message": "Backend local"}

@app.post('/files/upload')
async def upload_file(file: File):
    try:      
        collection = db["files"]
        data = file.dict()
        
        # Guarda en Base de datos
        result = await collection.insert_one(data)
        if result.inserted_id:
            # Guarda la imagen
            image_filepath = saveFileImage(data['content'], str(result.inserted_id))
            await collection.update_one({"_id": result.inserted_id}, {"$set": {"filepath": image_filepath}})
            data['filepath'] = image_filepath
            return {"message": "Archivo subido correctamente", "file_id": str(result.inserted_id), "image_filepath" : image_filepath}
        else:
            traceback_str = traceback.format_exc()
            raise HTTPException(status_code=500, detail=traceback_str)    
    except Exception as e:
        traceback_str = traceback.format_exc()
        return {"Backend error": str(e),
                'traceback' : traceback_str}, 500

@app.get("/files/{file_id}")
async def get_file(file_id):
    try:
        collection = db["files"]
        file = await collection.find_one({"_id": ObjectId(file_id)})
        
        if file:
            file_data = {
                "id": str(file["_id"]),
                "name": file.get("name"),
                "filepath": file.get("filepath")
            }
            return file_data
        else:
            return {"message": "File not found"}, 404  # Devolver un mensaje de error si el archivo no se encuentra
    except Exception as e:
        return {"error": str(e)}, 500  # Devolver un mensaje de error

@app.get("/files/")
async def get_file():
    collection = db["files"]
    files_data = []
    async for file in collection.find():
        file_data = {
            "id": str(file["_id"]),  # Convertir el ObjectId a una cadena
            "name": file.get("name")
        }
        files_data.append(file_data)
    return files_data

@app.post("/simulate")
async def simulate(simulation: Simulation):
    try:
        collection = db["simulations"]
        data = simulation.dict()      
        
        # Guarda la simulacion 
        sim = await collection.insert_one(data)
        if not sim.inserted_id :
            raise HTTPException(status_code=500, detail="Failed to create simulation")
        
        # Request para el simulador
        request = {
            "file_id" : data['file_id'],
            "model": data['model'],
            "slope": data['slope'],
            "start_time": data['start_time'],
            "end_time": data['end_time']
        }
    
        # Llama al simulador
        url = "http://firesim/simulate"
        response = httpx.post(url, json=request)
        
        # Guarda la respuesta como Result
        result_data = {
            "simulation_id" : str(sim.inserted_id),
            "content" : response.content.decode('utf-8')
        }
        
        collection = db["results"]
        res = await collection.insert_one(result_data)
        if not res.inserted_id :
            raise HTTPException(status_code=500, detail="Failed to create result")
        
        # Guarda la imagen
        image_filepath = saveFileImage(result_data['content'], str(res.inserted_id))
        
        if image_filepath is None:
            raise HTTPException(status_code=500, detail="Failed to save image")
        
        await collection.update_one({"_id": res.inserted_id}, {"$set": {"filepath": image_filepath}})
        
        return {'result' : str(res.inserted_id)}
        
    except Exception as e:
        traceback_str = traceback.format_exc()
        return {"Backend error": str(e),
                'traceback' : traceback_str}, 500
        
@app.get("/database-ping")
async def database_ping():
    if await db.command("ping"):
        return {"message": "Connection to MongoDB successful"}
    else:
        raise HTTPException(status_code=500, detail="Failed to connect to MongoDB")
    
@app.get("/simulations/{file_id}")
async def get_simulations(file_id):
    collection = db["simulations"]
   
    cursor = collection.find({"file_id": file_id})
    simulations = await cursor.to_list(length=None)
    
    for simulation in simulations:
        simulation["_id"] = str(simulation["_id"])
        cursor = db["results"].find({"simulation_id": simulation["_id"]})
        results = await cursor.to_list(length=None)
        for result in results:
            #result["_id"] = str(result["_id"])
            simulation["results"] = str(result["_id"])
    return  simulations
