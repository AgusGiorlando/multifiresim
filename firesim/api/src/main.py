import traceback
import asyncio
import time
import rediswq
from simulation.simulation import Simulation  # Importa la clase Simulation
from simulation.simulation_service import run_simulation  # Importa la función run_simulation.


async def simulate(simulation: Simulation):
    try:
        # Ejecuta la simulación
        result_filepath = await run_simulation(simulation)  
        # print(f"Simulation result file: {result_filepath}")
        
        # Abrir el archivo en modo lectura (WITH es para que cierre al finalizar el archivo)
        with open(result_filepath, 'r') as file:
            # Lee el contenido
            content = file.read()
            print(content)
        
    except FileNotFoundError:
        print(f'Error: El archivo "{result_filepath}" no se encuentra.')
    except Exception as e:
        just_the_string = traceback.format_exc()
        print(f"Firesim error: {str(e)}")
        print(f"Traceback: {just_the_string}")


async def main():
    # Conexion con redis
    host="redis-master"
    q = rediswq.RedisWQ(name="firesim-jobs", host=host, port=6379)
    while not q.empty():
        item = q.lease(lease_secs=10, block=True, timeout=2) 
        if item is not None:
            itemstr = item.decode("utf-8")
            print("Working on " + itemstr)
            time.sleep(10) # Put your actual work here instead of sleep.
            q.complete(item)
        else:
            print("Waiting for work")
    print("Queue empty, exiting")

    # Crear una instancia de Simulation con los argumentos proporcionados
    #simulation_data = Simulation()
    # print(simulation_data)
    #await simulate(simulation_data)

if __name__ == "__main__":
  asyncio.run(main())