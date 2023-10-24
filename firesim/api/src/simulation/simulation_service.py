import asyncio
import logging
import os
from subprocess import Popen, PIPE, CalledProcessError
from .simulation import Simulation

async def run_simulation(simulation: Simulation):
    try:      
        # Configuracion de logging
        logging.basicConfig(level=logging.DEBUG)       
        logger = logging.getLogger(__name__)
        
        file_handler = logging.FileHandler('logs.log')
        file_handler.setLevel(logging.DEBUG)
        
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        
        # Ruta del resultado
        result_filepath = os.path.join("../api/results", simulation.result_filename)
        logger.debug(f"Ruta del result: {result_filepath}")
        
        # Inicia la simulación de manera asincrónica
        logger.debug("Iniciando simulador")
        process = await asyncio.create_subprocess_exec(
            "../../src/fireSim", result_filepath, simulation.model, simulation.slope, simulation.file_ign, simulation.start_time, simulation.end_time,
            stdout=PIPE, stderr=PIPE, cwd="../src"
        )

        # Espera a que termine la simulacion
        stdout, stderr = await process.communicate()
        logger.debug("Simulacion terminada")
        
        # Verifica si hubo errores en la ejecución del simulador
        if process.returncode != 0:
            decoded_stdout = stdout.decode()
            logger.debug(decoded_stdout.strip())
            raise CalledProcessError(process.returncode, process, decoded_stdout.strip())
        logger.debug(f"Archivo result: {result_filepath}")

        return simulation.result_filename
    except CalledProcessError as e:
        raise Exception(e.output.strip())
    except Exception as e:
        raise Exception(str(e))