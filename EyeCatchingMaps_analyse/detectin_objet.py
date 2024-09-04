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

from comparaison import create_mask, calcul_histograme,compare_histograms,create_buffer_mask





def detection_objet(image):
    img_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    stop_data = cv2.CascadeClassifier('stop_data.xml') 
    found = stop_data.detectMultiScale(img_gray, 
                                   minSize =(20, 20))
    
    return found
def calcul_valeur(masque, edges):
    edges_masque = cv2.bitwise_and(edges, edges, mask=masque)
    mean = np.mean(edges_masque[masque == 1])
    variance = np.var(edges_masque[masque == 1])
    median = np.median(edges_masque[masque == 1])

    total_pixels = np.sum(masque == 1)
    edge_pixels = np.sum(edges_masque > 0)
    densite = edge_pixels / total_pixels if total_pixels != 0 else 0
    return variance, mean, densite,median



if __name__ == '__main__':
    liste_path_image = glob.glob('image/*')
    liste_path_heatmap = glob.glob('heatmap/*')
    liste_name =[]
    liste_moyenne =[]
    liste_densite = []
    liste_variance = []
    liste_median = []

    for k in range(1):
        image = cv2.imread(liste_path_image[k],cv2.IMREAD_COLOR)
        img_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
        heatmap = cv2.imread(liste_path_heatmap[k])
        objet = detection_objet(image)
        amount_found = len(objet)

        if amount_found != 0:
       

            for (x, y, width, height) in objet:
     
                cv2.rectangle(img_rgb, (x, y), 
                      (x + height, y + width), 
                      (0, 255, 0), 5)
           
        plt.subplot(1, 1, 1)
        plt.imshow(img_rgb)
        plt.show()

    # donnees = pd.DataFrame({'name': liste_name,
    #                             'densite':liste_densite, 
    #                             'moyenne': liste_moyenne,
    #                             'median': liste_median,
    #                             'var':liste_variance

    #                                 })
    # donnees.to_csv('export_analyse/donnees_edges.csv', index = False, header = True)


