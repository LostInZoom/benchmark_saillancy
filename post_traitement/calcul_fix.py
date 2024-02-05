
import glob
import os
import pandas as pd
import matplotlib.pyplot as plt
import csv
import json
from PIL import Image


def box(width_im,height_im):
    return [(1920/2-width_im/2)/1920,(1080/2-height_im/2)/1080,(1920/2+width_im/2)/1920,(1080/2+height_im/2)/1080] 
def map(timestamp,resultat):
    image = "false"
    time= 0
    time_to_map= 0
    for t in range(len(resultat)):
        if (timestamp+offset)*1000 >= resultat["time"][t]:
            image = resultat["etape"][t]
            time = resultat["time"][t]
            time_to_map = (timestamp+offset)*1000 -resultat["time"][t]
            continue
        else:
            break
    return image,time,time_to_map
def calculs_fixation(name_info_player_folder,
                     name_output_folder,
                     name_fixation_folder,
                     name_resultat_folder,
                     name_head_pose_tracker_folder,
                     name_export_folder,
                     name_image_folder):
    
    name_info_player = glob.glob(name_info_player_folder+'/*')
    name_output = glob.glob(name_output_folder+'/*')
    name_fixation = glob.glob(name_fixation_folder+'/*')
    name_export = glob.glob(name_resultat_folder+'/*')
    name_head_pose_tracker = glob.glob(name_head_pose_tracker_folder+'/*')


    liste_fixation = []
    for i in range(len(name_fixation)):
        assert os.path.exists(name_fixation[i])
        liste_fixation.append(pd.read_csv(name_fixation[i]))

    liste_resultat = []
    for i in range(len(name_export)):
        assert os.path.exists(name_export[i])
        liste_resultat.append(pd.read_csv(name_export[i]))

    liste_head_pose_tracker = []
    for i in range(len(name_head_pose_tracker)):
        assert os.path.exists(name_head_pose_tracker[i])
        liste_head_pose_tracker.append(pd.read_csv(name_head_pose_tracker[i]))

    liste_output = []
    for i in range(len(name_output)):
        assert os.path.exists(name_output[i])
        f = open(name_output[i],)
        liste_output.append(json.load(f))

    liste_info_player = []
    for i in range(len(name_info_player)):
        assert os.path.exists(name_info_player[i])
        f = open(name_info_player[i],)
        liste_info_player.append(json.load(f))

    liste_coord_fixation =[]

    for p in range(len(liste_fixation)):
        fixation = liste_fixation[p]
        resultat = liste_resultat[p]
        json_accuracy = liste_output[p]
        json_time = liste_info_player[p]    
        fichier_distance = liste_head_pose_tracker[p]

        coord_fixation =[]
        start_time_system = float(json_time["start_time_system_s"]) # System Time at recording start
        start_time_synced = float(json_time["start_time_synced_s"])     # Pupil Time at recording start
        # Calculate the fixed offset between System and Pupil Time
        offset = start_time_system - start_time_synced

        distance = fichier_distance["translation_z"].mean()*2.3
        accuracy = json_accuracy[0]["accuracy"]["degrees"]
        precision = json_accuracy[0]["precision"]["degrees"]


        for k in range(len(fixation)):
            id = fixation["fixation_id"][k]
            world_index = fixation["world_index"][k]
            dispersion = fixation["dispersion"][k]
            
            if int(fixation["world_index"][k]) > 10: 

                image,time,time_to_map = map(fixation["world_timestamp"][k],resultat)

                if image != "false":
                    path = name_image_folder +"/"+image
                    img = Image.open(path)
                    width = img.width
                    height = img.height
                    box_carte = box(width,height)
                    if float(fixation["norm_pos_x"][k]) > box_carte[0] and float(fixation["norm_pos_x"][k]) < box_carte[2]:   
                        if float(fixation["norm_pos_y"][k]) > box_carte[1] and float(fixation["norm_pos_y"][k]) < box_carte[3]:
                            x_relatif = (float(fixation["norm_pos_x"][k])-box_carte[0])/(box_carte[2]-box_carte[0])
                            y_relatif = (float(fixation["norm_pos_y"][k])-box_carte[1])/(box_carte[3]-box_carte[1])
                            coord_fixation.append([world_index,id,time,x_relatif,y_relatif,dispersion,image,height,width,distance,accuracy,precision,time_to_map])

        liste_coord_fixation.append(coord_fixation)


    for p in range(len(liste_fixation)):
        name = 'coord_fixation_on_map'+name_fixation[p].split('fixations_on_surface_Surface')[1]
        coord_fixation = liste_coord_fixation[p]
        with open(name_export_folder+'/'+name, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["world_index","id_fixation","time","x","y","dispersion","image","height","width","distance","accuracy","precision","time_to_map"]) # rajouter le zoom
            for i in range(len(coord_fixation)):
                writer.writerow(coord_fixation[i])




__name__ == '__main__'

calculs_fixation('info_player','output','fixation','export','head_pose_tracker','coord_fixation_on_map')
