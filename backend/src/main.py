import httpx
from fastapi import FastAPI
from simulation.simulation import Simulation

app = FastAPI()


@app.get("/")
def index():
    return {"message": "Backend"}


@app.post("/simulate")
async def simulate(simulation: Simulation):
    try:
        url = "http://localhost:8081/simulate"
        data = simulation.model_dump()
        
        # Encabezados si son necesarios
        headers = {"Content-Type": "application/json"}
        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=data, headers=headers)
        return {'response' : response.content}
    except Exception as e:
        return {"Backend error": str(e)}, 500
