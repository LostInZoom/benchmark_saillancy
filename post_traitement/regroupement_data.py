import glob
import numpy as np
import os
import pandas as pd
import csv

def regroupement_data(name_folder_input,name_output_folder):
    result_files = glob.glob(name_folder_input +'/*')
    fixation = []
    for i in range(len(result_files)):
        assert os.path.exists(result_files[i])
        fixation.append(pd.read_csv(result_files[i]))


    resultat_liste = pd.DataFrame(columns=["id_fixation", "time", "x", "y", "dispersion", "image", "distance", "accuracy", "precision", "time_to_map", "participant"])
    
    for i in range(len(fixation)):
        
        participant = result_files[i].split(".")[0].split("_")[9]
        fixation[i]['participant'] = participant    
        resultat_liste = pd.concat([resultat_liste, fixation[i]], ignore_index=True)

    for image_name, group in resultat_liste.groupby("image"):
        group.to_csv(name_output_folder +"/coord_fixation_"+image_name+".csv", index=False)




__name__ == '__main__'

regroupement_data('coord_fixation_on_map','resultat')