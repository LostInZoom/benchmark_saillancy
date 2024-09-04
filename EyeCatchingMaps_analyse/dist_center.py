
import numpy as np
import os
import pandas as pd
# id_fixation,time,x,y,dispersion,image,distance,accuracy,precision,time_to_map,participant,world_index,height,width



# fixaton = pd.read_csv('resultat/coord_fixation_ecran_gm_12.png.csv')
# name = 'resultat/coord_fixation_ecran_gm_12.png.csv'
name_im_1 = pd.read_csv('autre/name_im_1.csv')
name_im_2 = pd.read_csv('autre/name_im_2.csv')


# type_map = name.split('_')[2]

def calcul_dist_centre(fixation,name_file,name_google):

    liste_dist =pd.DataFrame(columns=['distance', 'participant'])

    name = name_file.split('resultat\coord_fixation_')[1].split(".csv")[0]

    for k in range(len(fixation)):
       
       width =  int(fixation['width'][k])
       height =  int(fixation['height'][k])
       if name in name_im_1.iloc[:, 0].values:
           participant = "1_"+str(fixation['participant'][k])
       else:
           participant ="2_"+str(fixation['participant'][k])
       dist_center = np.sqrt((width/2-width*int(fixation['x'][k]))**2+(height/2-height*int(fixation['y'][k])))
       nouvelle_ligne = pd.DataFrame({'distance': [dist_center], 'participant': [participant]})
       liste_dist = pd.concat([liste_dist, nouvelle_ligne], ignore_index=True)
       
       

    moyennes_par_participant = liste_dist.groupby('participant')['distance'].mean().reset_index(name='mean_distance')   
    type_map = name_file.split('_')[2]
    if type_map == "ecran" or type_map =="portable" or type_map =="postable":
        if type_map =="postable":
            moyennes_par_participant['type_map'] = "portable" 
        else :
            moyennes_par_participant['type_map'] = type_map

        moyennes_par_participant['fdc'] = name_file.split('_')[3]
    else :
        moyennes_par_participant['type_map'] = "autre"
        name_image = name_file.split("_")[2].split(".csv")[0]
        if name_image in name_google.iloc[:, 0].values:
             moyennes_par_participant['fdc'] = "gm"
        else:
             moyennes_par_participant['fdc'] = "autre"
    
    return moyennes_par_participant,liste_dist