import glob
import numpy as np
import os
import pandas as pd
import csv
#nom coord
test = glob.glob('resultat_enquete/*')


path_to_name = os.path.join('entree', "name_im.csv")
assert os.path.exists(path_to_name)
name = pd.read_csv(path_to_name,header = None)
fixation = []
liste_par_image = []

for i in range(len(test)):
    # path_to_fixation = os.path.join(path_to_export,test[i])
    assert os.path.exists(test[i])
    fixation.append(pd.read_csv(test[i]))

n=0   
nom_liste = name[0][n]
liste_p = []
for k in range(len(fixation[i])):
    if(nom_liste == fixation[i]["image"][k]):
        liste_p.append([fixation[i]["id_fixation"][k],fixation[i]["time"][k],fixation[i]["x"][k],fixation[i]["y"][k],fixation[i]["dispersion"][k],fixation[i]["image"][k]])
    else:            
        liste_par_image.append(liste_p)
        liste_p =[]
        n+=1
        nom_liste = name[0][n]
liste_par_image.append(liste_p)


for i in range(1,len(fixation)):
    n = 0
    nom_liste = name[0][n]

    for k in range(len(fixation[i])):
        if(nom_liste == fixation[i]["image"][k]):
            liste_par_image[n].append([fixation[i]["id_fixation"][k],fixation[i]["time"][k],fixation[i]["x"][k],fixation[i]["y"][k],fixation[i]["dispersion"][k],fixation[i]["image"][k]])
        else:            
            n+=1
            nom_liste = name[0][n]
            liste_par_image[n].append([fixation[i]["id_fixation"][k],fixation[i]["time"][k],fixation[i]["x"][k],fixation[i]["y"][k],fixation[i]["dispersion"][k],fixation[i]["image"][k]])





print(len(liste_par_image))

for k in range(len(liste_par_image)):
    with open('resultat/coord_fixation_'+name[0][k]+'.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["id_fixation","time","x","y","dispersion","image"]) # rajouter le zoom
        for i in range(len(liste_par_image[k])):
            writer.writerow(liste_par_image[k][i])
