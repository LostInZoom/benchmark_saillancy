import os
import pandas as pd
import matplotlib.pyplot as plt

import matplotlib.image as mpimg
from PIL import Image
import numpy as np
import matplotlib.cm as cm
from scipy.ndimage.filters import gaussian_filter

import glob
# les fichiers coord_fixation_on_image
liste_fichier_coord = glob.glob('resultat/*')
# image
liste_image = glob.glob('image/*')


fixation = []

for i in range(len(liste_fichier_coord)):
    assert os.path.exists(liste_fichier_coord[i])
    
    fixation.append(pd.read_csv(liste_fichier_coord[i]))



im = []
for i in range(len(liste_image)):
    im.append(mpimg.imread(liste_image[i]))

liste_coord = []


for t in range(len(im)):
    liste_x = []
    liste_y = []
    for k in range(len(fixation[t])):
        liste_x.append(fixation[t]["x"][k]*im[t].shape[1] )
        liste_y.append((1-fixation[t]["y"][k])*im[t].shape[0])
    liste_coord.append([liste_x,liste_y])

def myplot(x, y, s,l, bins=1000):
    heatmap, xedges, yedges = np.histogram2d(x, y, bins=bins,range = [[0,im[l].shape[1]],[0,im[l].shape[0]]])
    heatmap = gaussian_filter(heatmap, sigma=s)
    
    extent = [xedges[0], xedges[-1], yedges[0], yedges[-1]]
    return heatmap.T, extent

for t in range(len(im)):
    
    image,extent = myplot(liste_coord[t][0], liste_coord[t][1],60,t)
    plt.imshow(image,extent=extent,origin='upper', cmap=cm.jet)
    plt.axis("off")

    plt.savefig("heatmap/"+liste_image[t].split("\\")[1].split(".")[0]+"_heatmap.png", bbox_inches='tight',pad_inches = 0)
    plt.close()

for t in range(len(im)):
    plt.imshow(im[t])
    plt.axis("off")
    for k in range(len(fixation[t])):
        plt.plot(fixation[t]["x"][k]*im[t].shape[1], (1-fixation[t]["y"][k])*im[t].shape[0], "og", markersize=5)
    plt.savefig("carte_fixation/"+liste_image[t].split("\\")[1].split(".")[0]+"_fixation.png", bbox_inches='tight',pad_inches = 0)
    plt.close()
 
