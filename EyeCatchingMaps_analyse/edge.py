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




def calcul_edge(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur_img = cv2.GaussianBlur(gray,(3,3),0)
    edges = cv2.Canny(image=blur_img, threshold1=100, threshold2=200)
    return edges



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
    liste_densite_buffer = []
    liste_densite_image = []
    liste_rapport_densite_buffer = []
    liste_rapport_densite_image = []
    for k in range(len(liste_path_image)):
            
        image = cv2.imread(liste_path_image[k],cv2.IMREAD_COLOR)
        heatmap = cv2.imread(liste_path_heatmap[k])
        edge = calcul_edge(image)

        masque = create_mask(175,heatmap)
        variance,mean,densite,median = calcul_valeur(masque,edge)
        liste_name.append(liste_path_image[k].split("\\")[1])
        liste_moyenne.append(mean)
        liste_densite.append(densite)
        liste_variance.append(variance)
        liste_median.append(median)
        masque_buffer = create_buffer_mask(masque, 100)
        _,_,densite_buffer,_ = calcul_valeur(masque_buffer,edge)
        densite_image = np.sum(edge > 0) / edge.size if  edge.size != 0 else 0
        liste_densite_image.append(densite_image)
        liste_densite_buffer.append(densite_buffer)
        liste_rapport_densite_buffer.append(densite/densite_buffer ) if densite_buffer != 0 else liste_rapport_densite_buffer.append(0) 
        liste_rapport_densite_image.append(densite/densite_image) if  densite_image != 0 else liste_rapport_densite_image.append(0)
        # plt.imshow(edge, cmap='gray') 
        
        # plt.show()
    # donnees = pd.DataFrame({'name': liste_name,
    #                             'densite':liste_densite, 
    #                             'densite_buffer' :liste_densite_buffer,
    #                             'densite_map' : liste_densite_image,
    #                             'rapport_densite_map':liste_rapport_densite_image,
    #                             'rapport_densite_buffer':liste_rapport_densite_buffer

    #                                 })
    # donnees.to_csv('export_analyse/donnees_edges.csv', index = False, header = True)


