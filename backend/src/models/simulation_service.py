from io import StringIO
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import os
import logging

IMAGES_FOLDER = "images/"

def saveFileImage(content, image_filename):
    try:
        # logging.error(f"Contenido recibido: {content}")

        if not os.path.exists(IMAGES_FOLDER):
            logging.error(f"El directorio {IMAGES_FOLDER} no existe")
            return None
        
        index = content.find("\n")
        if index == -1:
            logging.warning("No se encontraron dimensiones, se procederá con el contenido sin dimensiones.")
            map = content
        else:
            dims = content[:index]
            map = content[index+1:]

        logging.info("Generando mapa a partir del contenido")
        map_io = StringIO(map)
        plt.figure(figsize=(10, 8))
        image = pd.read_csv(map_io, sep=" ", header=None)
        sns.heatmap(image, cmap="YlOrRd")
        sns.despine(ax=plt.gca(), left=True, bottom=True, right=True, top=True, offset=None, trim=False)
        plt.xticks([])
        plt.yticks([])

        image_filepath = IMAGES_FOLDER + image_filename + '.png'
        logging.info(f"Guardando imagen en {image_filepath}")
        if os.path.exists(image_filepath):
            os.remove(image_filepath)
        plt.savefig(image_filepath)
        logging.info("Imagen guardada exitosamente")
        
        return image_filepath
    except Exception as e:
        logging.error(f"Error al guardar la imagen: {e}")
        return None