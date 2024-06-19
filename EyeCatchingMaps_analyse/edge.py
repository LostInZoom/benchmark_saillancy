import cv2
import numpy as np
import geopandas as gpd
import glob
import numpy as np
from matplotlib.path import Path
import cv2
import pandas as pd
import matplotlib.pyplot as plt

import os




def create_polygon_mask(image, polygon_vertices):
    new_exterior_coords = [(x, -y) for x, y in polygon_vertices]
    polygon_coords = np.array(new_exterior_coords)
    height, width = image.shape[:2]
    
    y, x = np.mgrid[:height, :width]
    
    polygon_path = Path(polygon_coords)
    
    mask = polygon_path.contains_points(np.vstack((x.flatten(), y.flatten())).T)
    mask = mask.reshape((height, width))
    
    return mask




def calcul_edge(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur_img = cv2.GaussianBlur(gray,(3,3),0)
    edges = cv2.Canny(image=blur_img, threshold1=100, threshold2=200)
    return edges

if __name__ == '__main__':
    image = cv2.imread('image\ecran_gm_monument_16_c.png',cv2.IMREAD_COLOR)
    gdf = gpd.read_file('couche_shape\ecran_gm_monument_16_c.shp')
    edge = calcul_edge(image)
    print(edge)
    plt.imshow(edge)
    plt.show()
    # liste_shapefile = glob.glob('couche_shape/*.shp')
    # liste_name =[]
    # liste_id = []

    # for path_shapefile in liste_shapefile:
    #     gdf = gpd.read_file(path_shapefile)
    #     image_path = 'image/'+ path_shapefile.split('\\')[1].split('.')[0]+  '.png'
    #     if os.path.exists(image_path):
    #         # image = pd.read_csv(image_path)
    #         image = cv2.imread(image_path,cv2.IMREAD_COLOR)
    #     else:
    #         image_path = 'image/' + path_shapefile.split('\\')[1].split('.')[0] + '.PNG'
    #         if os.path.exists(image_path):
    #             # image = pd.read_csv(image_path)
    #             image = cv2.imread(image_path,cv2.IMREAD_COLOR)
    #         else:
    #             print(path_shapefile.split('\\')[1].split('.')[0])

    #     liste_masque = []
    #     for idx, row in gdf.iterrows():
    #         liste_name.append(image_path)
    #         liste_id.append(row['id'])
    #         exterior_coords = row['geometry'].exterior.coords
    #         image_copie = image.copy()
    #         masque_polygone = create_polygon_mask(image, exterior_coords)
    #         image_copie[masque_polygone == False] = 0 




    # donnees_homogene = pd.DataFrame({'name': liste_name,
    #                                 'id':liste_id, 
    #                                 'moyenne': liste_moyenne,
    #                                 'median': liste_median,
    #                                 'var':liste_variance

    #                                 })
    # donnees_homogene.to_csv('export_analyse/donnees_zone_homogene.csv', index = False, header = True)


