import cv2
import numpy as np
import geopandas as gpd
import glob
import numpy as np
from matplotlib.path import Path
import cv2
import pandas as pd
import matplotlib.pyplot as plt
import math 
def create_mask( seuil,heatmap):
    masque = heatmap > seuil    
    masque_dilate = cv2.dilate(masque.astype(np.uint8), np.ones((5, 5), np.uint8), iterations=1)
    masque_erode = cv2.erode(masque_dilate, np.ones((5, 5), np.uint8), iterations=1)    
    masque_erode = masque_erode[:, :, 0]  

    return masque_erode.astype(np.uint8)

def calcul_valeur(region):
    mask = region != 0
    non_zero_pixels = region[mask]
    variance = np.var(non_zero_pixels)
    mean = np.mean(non_zero_pixels)
    median = np.median(non_zero_pixels)

    return variance,mean,median


def calcul_histograme(image, masque):
    color = ('r','g','b')
    hist =[]
    for i,col in enumerate(color):
        hist_image = cv2.calcHist([image],[i],masque,[256],[0,256])
        hist_image_norm = hist_image/np.sum(hist_image)
        hist.append(hist_image_norm)
    return hist

def compare_histograms(hist1,hist2):
    # Calculer la distance de Bhattacharyya pour chaque canal de couleur

    distance = 0
    for i in range(3):  # Trois canaux de couleur (rouge, vert, bleu)
        distance_channel = - math.log(np.sum(np.sqrt(hist1[i] * hist2[i])))

        distance += distance_channel
    return distance / 3  # Moyenne des distances pour chaque canal

def create_buffer_mask(masque, buffer_size):
    buffer_mask = cv2.dilate(masque, np.ones((buffer_size, buffer_size), np.uint8), iterations=1)
    buffer_mask = buffer_mask - masque
    return buffer_mask
