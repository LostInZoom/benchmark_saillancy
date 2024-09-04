

from PIL import Image, ImageDraw, ImageChops
import geopandas as gpd
import numpy as np
import glob
import os 
from PIL import Image,ImageDraw,ImageChops
import csv
import pandas as pd
import matplotlib.pyplot as plt
import geopandas as gpd
from shapely.geometry import Polygon as ShapelyPolygon
import numpy as np
from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection
import cv2
from comparaison import create_mask, calcul_histograme,compare_histograms,create_buffer_mask

# Chemins vers les fichiers
heatmap_path = "heatmap/heatmap_ecran_gm_8.jpg"
image_path = "image/ecran_gm_8.png"
liste_path_image = glob.glob('image/*')
liste_path_heatmap = glob.glob('heatmap/*')

for k in range(len(liste_path_image)):
    name=liste_path_image[k].split("\\")[1]
    image = cv2.imread(liste_path_image[k])
    heatmap = cv2.imread(liste_path_heatmap[k])

    masque_heatmap = create_mask(175,heatmap)
    contours, _ = cv2.findContours(masque_heatmap, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)


    image_with_contours = image.copy()
    for i, contour in enumerate(contours):
        cv2.drawContours(image_with_contours, [contour], -1, (0, 0, 255), 2)  # Couleur rouge (BGR) et épaisseur 2
    
        M = cv2.moments(contour)
        if M["m00"] != 0:
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
        else:
            cX, cY = contour[0][0]  # Si le moment est zéro, utilisez le premier point du contour
    
    # Ajouter le numéro à côté du contour
        cv2.putText(image_with_contours, str(i+1), (cX, cY), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

    # Enregistrer l'image avec les contours
    output_path = os.path.join("draw", name)
    cv2.imwrite(output_path, image_with_contours)
