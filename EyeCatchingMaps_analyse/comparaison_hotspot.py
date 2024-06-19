import cv2
import numpy as np
import geopandas as gpd
import glob
import numpy as np
from matplotlib.path import Path
import cv2
import pandas as pd
import matplotlib.pyplot as plt
from comparaison import create_mask, calcul_histograme,compare_histograms,create_buffer_mask

if __name__ == '__main__':
    liste_path_image = glob.glob('image/*')
    liste_path_heatmap = glob.glob('heatmap/*')
#Comparaison de tous les hotspots

    liste_hist = []
    for k in range(len(liste_path_image)):
            
        image = cv2.imread(liste_path_image[k])
        heatmap = cv2.imread(liste_path_heatmap[k])

        masque = create_mask(175, heatmap)

        hist =calcul_histograme(image,masque)
        liste_hist.append(hist)
    resultas = []
    liste_name_1 = []
    lsite_name_2 =[]
    for i in range(len(liste_hist)):
        for j in range(i + 1, len(liste_hist)):
            
            distance = compare_histograms(liste_hist[i], liste_hist[j])
            resultas.append(distance)
            liste_name_1.append(liste_path_image[j].split("\\")[1])
            lsite_name_2.append(liste_path_image[i].split("\\")[1])

    donnees_dist_hist = pd.DataFrame({'image_1': liste_name_1,
                                    'image_2':lsite_name_2, 
                                    'distance': resultas
                                    })
    donnees_dist_hist.to_csv('export_analyse/donnees_distance_hist.csv', index = False, header = True)


#comparaison hotspot /map
    liste_hist_hotspot = []
    liste_hist = []
    resultats = []
    liste_name_1 = []
    for k in range(len(liste_path_image)):
            
        image = cv2.imread(liste_path_image[k])
        heatmap = cv2.imread(liste_path_heatmap[k])

        masque = create_mask(175, heatmap)

        hist_hotspot =calcul_histograme(image,masque)
        hist_map = calcul_histograme(image, None)

        resultats.append(compare_histograms(hist_map,hist_hotspot))
        liste_name_1.append(liste_path_image[k].split("\\")[1])
        


    donnees_dist_hist = pd.DataFrame({'image': liste_name_1,
                                    'distance': resultats
                                    })
    donnees_dist_hist.to_csv('export_analyse/donnees_distance_hist_hotspot_map.csv', index = False, header = True)

#compairaison hotsppot /buffer

    liste_hist_hotspot = []
    liste_hist = []
    resultats = []
    liste_name_1 = []
    size = 100
    for k in range(len(liste_path_image)):
            
        image = cv2.imread(liste_path_image[k])
        heatmap = cv2.imread(liste_path_heatmap[k])

        masque = create_mask(175, heatmap)

        hist_hotspot =calcul_histograme(image,masque)
        masque_buffer = create_buffer_mask(masque,size)
        hist_buffer = calcul_histograme(image, masque_buffer)

        resultats.append(compare_histograms(hist_buffer,hist_hotspot))
        liste_name_1.append(liste_path_image[k].split("\\")[1])
        

    donnees_dist_hist = pd.DataFrame({'image': liste_name_1,
                                    'distance': resultats
                                    })
    donnees_dist_hist.to_csv('export_analyse/donnees_distance_hist_hotspot_buffer.csv', index = False, header = True)
