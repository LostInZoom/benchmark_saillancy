import cv2
import numpy as np
import geopandas as gpd
import glob
import numpy as np
from matplotlib.path import Path
import cv2
import pandas as pd

import os




def create_polygon_mask(image, polygon_vertices):
    height, width = image.shape[:2]
    
    y, x = np.mgrid[:height, :width]
    
    polygon_path = Path(polygon_vertices)
    
    mask = polygon_path.contains_points(np.vstack((x.flatten(), y.flatten())).T)
    mask = mask.reshape((height, width))
    
    return mask

# def calcul_similarite(region1, region2):
#     correlation = cv2.matchTemplate(region1, region2, cv2.TM_CCOEFF_NORMED)
#     similarite = correlation[0][0]
#     return similarite

def calcul_homogene(region):
    mask = region != 0
    non_zero_pixels = region[mask]
    variance = np.var(non_zero_pixels)
    mean = np.mean(non_zero_pixels)
    median = np.median(non_zero_pixels)

    return variance,mean,median



if __name__ == '__main__':
    liste_shapefile = glob.glob('couche_shape/*.shp')
    liste_name =[]
    liste_moyenne =[]
    liste_median = []
    liste_variance = []
    liste_id = []

    for path_shapefile in liste_shapefile:
        gdf = gpd.read_file(path_shapefile)
        image_path = 'image/'+ path_shapefile.split('\\')[1].split('.')[0]+  '.png'
        if os.path.exists(image_path):
            image = cv2.imread(image_path)
        else:
            image_path = 'image/' + path_shapefile.split('\\')[1].split('.')[0] + '.PNG'
            if os.path.exists(image_path):
                image = cv2.imread(image_path)
            else:
                print("Aucun fichier CSV trouvé pour", path_shapefile.split('\\')[1].split('.')[0])

        liste_masque = []
        for idx, row in gdf.iterrows():
            liste_name.append(image_path)
            liste_id.append(row['id'])
            exterior_coords = row['geometry'].exterior.coords
            new_exterior_coords = [(x, -y) for x, y in exterior_coords]
            polygon_coords = np.array(new_exterior_coords)

            image_copie = image.copy()
            masque_polygone = create_polygon_mask(image, polygon_coords)
            image_copie[masque_polygone == False] = 0 
            liste_masque.append(image_copie)
            variance,mean,median = calcul_homogene(image_copie)
            liste_variance.append(variance)
            liste_moyenne.append(mean)
            liste_median.append(median)

    donnees_homogene = pd.DataFrame({'name': liste_name,
                                    'id':liste_id, 
                                    'moyenne': liste_moyenne,
                                    'median': liste_median,
                                    'var':liste_variance

                                    })
    donnees_homogene.to_csv('export_analyse/donnees_zone_homogene_image.csv', index = False, header = True)





        
