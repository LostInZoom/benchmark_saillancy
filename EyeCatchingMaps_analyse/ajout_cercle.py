import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.image as mpimg
import numpy as np
from PIL import Image

image_grand_format = mpimg.imread('image/ecran_gm_seaside_10.png')

image_petit_format = mpimg.imread('image/portable_osm_seaside_14.png')
theta = np.linspace(0, 2*np.pi, 100)


image_grand_format = Image.open('image/ecran_gm_seaside_10.png')
image_petit_format = Image.open('image/portable_osm_seaside_14.png')
heatmap_grand_format = Image.open('heatmap/heatmap_ecran_gm_seaside_10.jpg')
heatmap_petit_format = Image.open('heatmap/heatmap_portable_osm_seaside_14.jpg')
def calcul_stat_centre(heatmap,rayon):
    heatmap_array = np.array(heatmap)

    height, width = heatmap_array.shape[:2]

    y, x = np.ogrid[-height/2:height/2, -width/2:width/2]
    masque = x**2 + y**2 <= rayon**2
    valeurs_dans_cercle = heatmap_array[masque]

    moyenne = np.mean(valeurs_dans_cercle)
    ecart_type = np.std(valeurs_dans_cercle)
    median = np.median(valeurs_dans_cercle)
    return moyenne,ecart_type,median
