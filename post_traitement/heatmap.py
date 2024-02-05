import os
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from PIL import Image
import numpy as np
from scipy.ndimage.filters import gaussian_filter
import glob


liste_fichier_coord = glob.glob('resultat/*')
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

def myplot(x, y, s,l):
    bins_x = im[l].shape[1]  
    bins_y = im[l].shape[0] 
    heatmap, xedges, yedges = np.histogram2d(x, y, bins=[bins_x, bins_y], range=[[0, im[l].shape[1]], [0, im[l].shape[0]]])
    heatmap = gaussian_filter(heatmap, sigma=s/2.355)
    
    extent = [0, im[l].shape[1], 0, im[l].shape[0]]  
    print(liste_image[l],extent,liste_fichier_coord[l])
    return heatmap.T, extent




for t in range(len(im)):
    mean_disp = fixation[t]["accuracy"].mean()
    distance_cm =fixation[t]["distance"].mean()
    ecran_cm =  np.tan(np.deg2rad(mean_disp)) * distance_cm
    pixel_ecran =ecran_cm / 0.02
    image,extent = myplot(liste_coord[t][0], liste_coord[t][1],pixel_ecran,t)
    image_normalized = ((image - np.min(image)) / (np.max(image) - np.min(image)) * 255).astype(np.uint8)
    heatmap_image = Image.fromarray(image_normalized, mode='L')

    heatmap_image.save("heatmap/heatmap_" + liste_image[t].split("\\")[1].split(".")[0] + ".jpg")

    plt.close()


# for t in range(len(im)):
#     plt.imshow(im[t])
#     plt.axis("off")
#     for k in range(len(fixation[t])):
#         plt.plot(fixation[t]["x"][k]*im[t].shape[1], (1-fixation[t]["y"][k])*im[t].shape[0], "og", markersize=5)
#     plt.savefig("carte_fixation/fixation_"+liste_image[t].split("\\")[1].split(".")[0]+".jpg", bbox_inches='tight',pad_inches = 0,format='jpg')
#     plt.close()
 


