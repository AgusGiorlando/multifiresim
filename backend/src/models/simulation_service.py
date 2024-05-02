from io import StringIO
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import os

IMAGES_FOLDER = "images/"

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
        # Path del archivo
            image_filepath = IMAGES_FOLDER + image_filename + '.png'
        # Eliminar el archivo heatmap.png si ya existe
            if os.path.exists(image_filepath):
               os.remove(image_filepath)
       # Guardar el gráfico como una imagen                
            plt.savefig(image_filepath)
            return image_filepath
           
    except Exception as e:
        raise e  # Levanta la excepción original