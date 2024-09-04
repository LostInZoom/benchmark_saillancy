import cv2
import geopandas as gpd
import glob
import numpy as np

import pandas as pd
import matplotlib.pyplot as plt
from skimage.segmentation  import felzenszwalb
import os

from comparaison import create_mask, calcul_histograme,compare_histograms,create_buffer_mask


from skimage.draw import circle_perimeter
from skimage.filters import gaussian





if __name__ == '__main__':
    liste_path_image = glob.glob('image/*')
    liste_path_heatmap = glob.glob('heatmap/*')
    liste_densite = []

    liste_densite_map = []
    liste_rapport = []
    liste_name = []
    for k in range(len(liste_path_image)):
            
        image = cv2.imread(liste_path_image[k],cv2.IMREAD_COLOR)
        heatmap = cv2.imread(liste_path_heatmap[k])
        masque = create_mask(175,heatmap)

        segments = felzenszwalb(image, scale=3.0, sigma=0.95, min_size=200)
        masked_image = cv2.bitwise_and(image, image, mask=masque)
        segments_masque = felzenszwalb(masked_image, scale=3.0, sigma=0.95, min_size=200)
        densite_hotspot = len(np.unique(segments_masque))/np.sum(masque > 0)
        densite_map =len(np.unique(segments))/(image.shape[0] * image.shape[1])
        liste_densite_map.append(densite_map)
        liste_densite.append(densite_hotspot)
        liste_rapport.append(densite_hotspot/densite_map)

        liste_name.append(liste_path_image[k].split("\\")[1])
    # fig, ax = plt.subplots(figsize=(10, 8))
    # ax.imshow(image)
    # print(len( np.unique(segments)))
    # for segment_id in np.unique(segments):
    #     mask = segments == segment_id
    #     color = np.random.rand(3,)
    #     ax.contour(mask, colors=[color], linewidths=0.5)

    # ax.set_title('Segments de Felzenszwalb')
    # plt.axis('off')
    # plt.show()


 


    donnees = pd.DataFrame({'name': liste_name,
                                'densite':liste_densite, 
                                'densite_map' :liste_densite_map,
                                'rapport_densite' : liste_rapport

                                    })
    donnees.to_csv('export_analyse/donnees_segmentation_200.csv', index = False, header = True)


