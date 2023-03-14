#Ce script permet de convertir les points de fixation dans la scène 3D en coordonnée par rapport à la carte afficher à l'écran 


import os
import pandas as pd
import matplotlib.pyplot as plt
import csv
import json
from PIL import Image
# resultat_carte.cvs est produit par l'enquête
# fixations_on_surface_Surface est produit par l'acquisition avec l'ET, il est dans export/surface
# info.player.json est dans le dossier produit par l'acquisition (il permet de calculer le temps réel)



f = open('recordings/info.player.json',)
json_time = json.load(f)


start_time_system = float(json_time["start_time_system_s"]) # System Time at recording start
start_time_synced = float(json_time["start_time_synced_s"])     # Pupil Time at recording start
# Calculate the fixed offset between System and Pupil Time
offset = start_time_system - start_time_synced


path_to_export = "recordings"
path_to_enquete = "resultat_enquete"
path_to_fixation = os.path.join(path_to_export, "fixations_on_surface_Surface 1.csv")
path_to_resultat= os.path.join(path_to_export, "resultat_enquete.csv")

assert os.path.exists(path_to_fixation)
fixation = pd.read_csv(path_to_fixation)

assert os.path.exists(path_to_resultat)
resultat = pd.read_csv(path_to_resultat)
# width_im = 1704
# height_im =856

coord_fixation =[]
# box_carte = [(1920/2-width_im/2)/1920,(1080/2-height_im/2)/1080,(1920/2+width_im/2)/1920,(1080/2+height_im/2)/1080] # a calculer en pourcentage (xmin,ymin,xmax,ymax)
# a voir comment faire 
def box(width_im,height_im):
    return [(1920/2-width_im/2)/1920,(1080/2-height_im/2)/1080,(1920/2+width_im/2)/1920,(1080/2+height_im/2)/1080] 
def map(timestamp):
    image = "false"
    time= 0
    for t in range(len(resultat)):
        if (timestamp+offset)*1000 >= resultat["time"][t]:
            image = resultat["etape"][t]
            time = resultat["time"][t]
            continue
        else:
            break
    return image,time

for k in range(len(fixation)):
    id = fixation["fixation_id"][k]
    world_index = fixation["world_index"][k]
    dispersion = fixation["dispersion"][k]
    
    if int(fixation["world_index"][k]) > 10: # on enleve les points de debut lors du lancement de l'acquisition 
    #on prend en compte les points qui sont positionnée sur la carte 
        

        image,time = map(fixation["world_timestamp"][k])

            # on calcul la position relative du point dans la carte
        if image != "false":
            path = "image/"+image
            img = Image.open(path)
            width = img.width
            height = img.height
            box_carte = box(width,height)
            if float(fixation["norm_pos_x"][k]) > box_carte[0] and float(fixation["norm_pos_x"][k]) < box_carte[2]:   
                if float(fixation["norm_pos_y"][k]) > box_carte[1] and float(fixation["norm_pos_y"][k]) < box_carte[3]:
                    x_relatif = (float(fixation["norm_pos_x"][k])-box_carte[0])/(box_carte[2]-box_carte[0])
                    y_relatif = (float(fixation["norm_pos_y"][k])-box_carte[1])/(box_carte[3]-box_carte[1])
                    coord_fixation.append([world_index,id,time,x_relatif,y_relatif,dispersion,image,height,width])


with open('resultat_enquete/coord_fixation_on_map.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["world_index","id_fixation","time","x","y","dispersion","image","height","width"]) # rajouter le zoom
    for i in range(len(coord_fixation)):
        writer.writerow(coord_fixation[i])
