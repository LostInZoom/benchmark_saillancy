import numpy as np
from scipy.stats import pearsonr,wasserstein_distance
from dit.divergences import earth_movers_distance
from dit.divergences import kullback_leibler_divergence
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from scipy.special import kl_div
import glob
import os

# heatmap_image1 = mpimg.imread('res_covSal_benchmark/6.jpg')
# heatmap_image2 = mpimg.imread('res_FES_benchmark/6.jpg')
# heatmap_image3 = mpimg.imread('heatmap/heatmap_6.jpg')
# heatmap_matrix1 = np.mean(heatmap_image1, axis=-1)  
# heatmap_matrix2 = np.mean(heatmap_image2, axis=-1)


path_image_FES = glob.glob('res_FES_benchmark/*')
path_image_covSal = glob.glob('res_covSal_benchmark/*')
liste_image_covSal = []
liste_image_FES =[]
lsite_image_heatmap = []

for i in range(len(path_image_covSal)):
    liste_image_covSal.append(mpimg.imread(path_image_covSal[i]))

for i in range(len(path_image_FES)):
    liste_image_FES.append(mpimg.imread(path_image_FES[i]))

    lsite_image_heatmap.append(mpimg.imread('heatmap/heatmap_' + os.path.basename(path_image_FES[i]).split('.')[0]+'.jpg'))

for i in range(len(liste_image_covSal)):

    heatmap_image = np.mean(lsite_image_heatmap[i], axis=-1)  # Convertir en niveau de gris si nécessaire
    heatmap_FES = np.mean(liste_image_FES[i], axis=-1)
    heatmap_coVsal = np.mean(liste_image_covSal[i], axis=-1)
    pearson_FES = pearsonr(heatmap_image, heatmap_FES)
    pearson_covsal = pearsonr(heatmap_image, heatmap_coVsal)


    print(os.path.basename(path_image_FES[i]),'cov',pearson_covsal,'fes',pearson_FES)



# Calcul de la distance de Wasserstein
# emd = wasserstein_distance(heatmap_matrix1, heatmap_matrix2)
# pearson = pearsonr(heatmap_matrix1, heatmap_matrix2)
# kl_div = kl_div(heatmap_matrix1, heatmap_matrix2)


