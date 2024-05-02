import httpx
import os
import json
from io import StringIO
import matplotlib.pyplot as plt
import seaborn as sns
import traceback
import pandas as pd

#BACKEND_URL = "http://localhost:5000/"
BACKEND_URL = "http://backend/"


def findFileContentById(file_id):
    backend_url = BACKEND_URL + "files/" + file_id
    response = httpx.get(backend_url)
    if response.status_code == 200:
        try:
            filepath = response.json().get("filepath")
            return filepath
        except json.decoder.JSONDecodeError:
            return "La respuesta no es un JSON válido"
    else:
        # Manejar el caso donde la respuesta no es exitosa
        return "La solicitud no fue exitosa. Código de estado: {response.status_code}"

def saveFileImage(content, image_filename):
    try:
        index = content.find("\n")
        if index != -1:
           # Separa las dimensiones del mapa
           dims = content[:index]
           map = content[index+1:]
       # Convertir la matriz en un objeto StringIO
           map_io = StringIO(map)
           # Leer la matriz como un DataFrame
           plt.figure(figsize=(10,8))
           image = pd.read_csv(map_io, sep=" ", header=None)
           sns.heatmap(image, cmap = "YlOrRd")      
           # Elimina ejes del grafico
           sns.despine(ax=plt.gca(), left=True, bottom=True, right=True, top=True, offset=None, trim=False) 
           # Elimina numeros en ejes
           plt.xticks([])
           plt.yticks([])
       # Eliminar el archivo heatmap.png si ya existe
           if os.path.exists(image_filename):
               os.remove(image_filename)
       # Guardar el gráfico como una imagen                
           plt.savefig(image_filename)
    except Exception as e:
        raise e  # Levanta la excepción original
        
def findSimulationsByFile(file_id):
    try:
        results = []
        backend_url = BACKEND_URL + "simulations/" + file_id
        response = httpx.get(backend_url)
        if response.status_code == 200:
            for simulation in response.json():
                results.append(simulation)
            return results
        else:
            # Manejar el caso donde la respuesta no es exitosa
            return "La solicitud no fue exitosa. Código de estado: {response.status_code}"
    except Exception as e:
        raise e



