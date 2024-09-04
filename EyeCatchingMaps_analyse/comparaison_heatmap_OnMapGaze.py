import numpy as np

import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from scipy.special import kl_div
import glob
import os
import os
import cv2
import numpy as np
import csv
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from sklearn.metrics import r2_score
import pandas as pd



def comparaison_heatmap_onMapGaze(image1,image2,name_image):
    name = []
    liste_threshold = []
    liste_heat_dif = []
    for threshold in np.linspace(0, 1, num=256):
            # Calculate difference
        diff = image1 - image2

            # Turn difference to table
        value = np.absolute(diff)

            # Accumulate counter for all pixels
        counter = 0
        for ii in range(value.shape[0]):
            for jj in range(value.shape[1]):
                if value[ii,jj] <= threshold * 255:
                    counter = counter + 1
                    heat_dif = (counter/((ii+1) * (jj+1)))
        name.append(name_image)
        liste_threshold.append(threshold)
        liste_heat_dif.append(heat_dif)
    return name, liste_heat_dif, liste_threshold
    

if __name__ == '__main__':

        
    path_image_FES = glob.glob('res_FES_benchmark/*')
    path_image_covSal = glob.glob('res_covSal_benchmark/*')
    liste_image_covSal = []
    liste_image_FES =[]
    lsite_image_heatmap = []

    for i in range(len(path_image_covSal)):
        
        liste_image_covSal.append(cv2.imread(path_image_covSal[i], 0).astype("int8"))

    for i in range(len(path_image_FES)):
        liste_image_FES.append(cv2.imread(path_image_FES[i], 0).astype("int8"))

        lsite_image_heatmap.append(cv2.imread('heatmap/heatmap_' + os.path.basename(path_image_FES[i]).split('.')[0]+'.jpg',0).astype("int8"))



    liste_name = []
    liste_threshold = []
    liste_heat_dif = []
    for i in range(len(liste_image_covSal)):
    

        image1 = lsite_image_heatmap[i]
        image2 = liste_image_covSal[i]
        image3 = liste_image_FES[i]
        name = os.path.basename(path_image_FES[i]).split('.')[0]
        print(name)

        name_CovSal, threshold_CovSal, heat_CovSal = comparaison_heatmap_onMapGaze(image1,image2,name+"CovSal")
        name_FES, threshold_FES, heat_FES = comparaison_heatmap_onMapGaze(image1,image3,name+"FES")
        liste_name+= name_CovSal
        liste_threshold += threshold_CovSal 
        liste_heat_dif += heat_CovSal
        liste_name+= name_FES
        liste_threshold += threshold_FES
        liste_heat_dif += heat_FES

    donnees = pd.DataFrame({'name': liste_name,
                                'threshold':liste_threshold, 
                                'heat_dif': liste_heat_dif

                                    })
    donnees.to_csv('export_analyse/comparaison_heatmap_OnMapGaze.csv', index = False, header = True)


