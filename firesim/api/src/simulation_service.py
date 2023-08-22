import asyncio
from subprocess import Popen, PIPE, CalledProcessError
from .simulation import Simulation


async def run_simulation(simulation: Simulation):
    try:
        # Ruta del resultado
        result_filepath = "../results/" + simulation.result_filename

        # Inicia la simulación de manera asincrónica
        process = await asyncio.create_subprocess_exec(
            "../src/fireSim", result_filepath, simulation.model, simulation.slope, simulation.file_ign, simulation.start_time, simulation.end_time,
            stdout=PIPE, stderr=PIPE, cwd="../src"
        )

        # Espera a que termine la simulacion
        stdout, stderr = await process.communicate()

        # Verifica si hubo errores en la ejecución del simulador
        if process.returncode != 0:
            raise CalledProcessError(
                process.returncode, process.args, stdout.decode().strip())

        return result_filepath
    except CalledProcessError as e:
        raise Exception(e.output.strip())
    except Exception as e:
        raise Exception(str(e))
