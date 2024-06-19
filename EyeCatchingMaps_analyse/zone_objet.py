import cv2
import numpy as np
import geopandas as gpd
import glob
import numpy as np
from matplotlib.path import Path
import cv2
import pandas as pd
import re
import os
import matplotlib.pyplot as plt

from comparaison import create_mask, calcul_histograme,compare_histograms



def create_polygon_mask(image, polygon_vertices):
    height, width = image.shape[:2]
    
    y, x = np.mgrid[:height, :width]
    
    polygon_path = Path(polygon_vertices)
    
    mask = polygon_path.contains_points(np.vstack((x.flatten(), y.flatten())).T)
    mask = mask.reshape((height, width))
    
    return mask

def calcul_histograme(image, masque):
    color = ('r','g','b')
    hist =[]
    masque_bin = masque.astype(np.uint8) * 255
    for i,col in enumerate(color):
        hist_image = cv2.calcHist([image],[i],masque_bin,[256],[0,256])
        hist.append(hist_image/np.sum(hist_image))
    return hist


def calcul_homogene(region):
    mask = region != 0
    non_zero_pixels = region[mask]
    variance = np.var(non_zero_pixels)
    mean = np.mean(non_zero_pixels)
    median = np.median(non_zero_pixels)

    return variance,mean,median

def valeur_heatmap(heatmap, polygone):
    masque_polygone = create_polygon_mask(heatmap, polygone)
    valeurs_dans_polygone = heatmap[masque_polygone]
    moy = np.mean(valeurs_dans_polygone)
    med = np.median(valeurs_dans_polygone)
    variance = np.var(valeurs_dans_polygone)
    max =int(np.max(valeurs_dans_polygone))

    return moy, med,variance, max

if __name__ == '__main__':
    liste_shapefile = glob.glob('couche_objet/*.shp')
    liste_name =[]
    liste_moyenne =[]
    liste_median = []
    liste_variance = []
    liste_moyenne_heatmap =[]
    liste_median_heatmap = []
    liste_variance_heatmap = []
    liste_max_heatmap = []
    hotspot = []

    liste_id = []
    resultats = []
    liste_id_d = []
    liste_name_d = []

    for path_shapefile in liste_shapefile:
        gdf = gpd.read_file(path_shapefile)
        name = re.sub(r'_city|_road|_toponyme', '', path_shapefile.split('\\')[1].split('.')[0], flags=re.IGNORECASE)
        image_path = 'image/' + name + '.png'
        heatmap_path = 'heatmap/heatmap_'+name+'.jpg'
        heatmap =  cv2.imread(heatmap_path)

        if os.path.exists(image_path):
            image = cv2.imread(image_path)
        else:
            image_path = 'image/' + name + '.PNG'            
            if os.path.exists(image_path):
                image = cv2.imread(image_path)
            else: 
                print("Aucun fichier CSV trouvé pour", path_shapefile.split('\\')[1].split('.')[0])

        liste_hist = []
        liste_id_area = []
        liste_max = []

        for idx, row in gdf.iterrows():

            liste_name.append(name)
            liste_id.append(row['id'])
            exterior_coords = row['geometry'].exterior.coords
            new_exterior_coords = [(x, -y) for x, y in exterior_coords]
            polygon_coords = np.array(new_exterior_coords)
            moy_h, med_h, var_h, max_h = valeur_heatmap(heatmap,polygon_coords)

            image_copie = image.copy()
            masque_polygone = create_polygon_mask(image, polygon_coords)
            image_copie[masque_polygone == False] = 0 
            variance,mean,median = calcul_homogene(image_copie)

            liste_variance.append(variance)
            liste_moyenne.append(mean)
            liste_median.append(median)
            liste_variance_heatmap.append(var_h)
            liste_moyenne_heatmap.append(moy_h)
            liste_median_heatmap.append(med_h)
            liste_max_heatmap.append(max_h)
            hist = calcul_histograme(image,masque_polygone)
            liste_hist.append(hist)
            liste_id_area.append(row['id'])
            liste_max.append(max_h)

        for i in range(len(liste_hist)):
            for j in range(i + 1, len(liste_hist)):
                distance = compare_histograms(liste_hist[i], liste_hist[j])
                resultats.append(distance)
                liste_id_d.append([liste_id_area[i],liste_id_area[j]])
                liste_name_d.append(name)
                if liste_max[i] >175 or liste_max[j]:
                    hotspot.append(True)
                else:
                    hotspot.append(False)

 

    donnees_homohene_objet = pd.DataFrame({'name': liste_name,
                                    'id':liste_id, 
                                    'moyenne': liste_moyenne,
                                    'median': liste_median,
                                    'var':liste_variance,
                                    'moyenne_heatmap': liste_moyenne_heatmap,
                                    'median_heatmap': liste_median_heatmap,
                                    'var_heatmap':liste_variance_heatmap
                                    })
    donnees_homohene_objet.to_csv('export_analyse/donnees_homogene_objet.csv', index = False, header = True)


    donnees_hist_objet = pd.DataFrame({'name': liste_name_d,
                                    'id':liste_id_d, 
                                    'distance': resultats,
                                    'hotspot' :hotspot

                                    })
    donnees_hist_objet.to_csv('export_analyse/donnees_distance_hist_objet.csv', index = False, header = True)






        
