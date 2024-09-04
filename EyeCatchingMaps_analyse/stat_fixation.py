import cv2
import numpy as np
import geopandas as gpd
import glob
import numpy as np
from matplotlib.path import Path
import cv2
import pandas as pd

import os

import statistics









if __name__ == '__main__':
    liste_fixation_coord = glob.glob('resultat/*')
    fixation = []
    for i in range(len(liste_fixation_coord)):
        assert os.path.exists(liste_fixation_coord[i])
        
        fixation.append(pd.read_csv(liste_fixation_coord[i]))


    
    liste_name_c = []
    liste_median_time_fixation = []
    liste_median_count_fixation = []
    liste_median_amplitude_fixation = []
    liste_mean_time_fixation = []
    liste_mean_count_fixation = []
    liste_mean_amplitude_fixation = []
    liste_ec_time_fixation = []
    liste_ec_count_fixation = []
    liste_ec_amplitude_fixation = []
    for p in range(len(fixation)): 
    
        fixation_k = fixation[p]
        liste_time = []
        liste_participant = []
        liste_count = []
        liste_centre_x = [ ]
        liste_centre_y = [ ]
        width = fixation_k['width'][0]
        height = fixation_k['height'][0]

        combinaisaon = fixation_k[['id_fixation', 'participant']].drop_duplicates()
        liste_name_c.append(liste_fixation_coord[p].split('coord_fixation_')[1].split(".csv")[0])

        liste_participant_all =  fixation_k['participant'].unique()
        for participant in liste_participant_all:
            fixation_participant = combinaisaon[combinaisaon['participant'] == participant].shape[0] 
            liste_count.append(fixation_participant)

        for idx, row in combinaisaon.iterrows():    
            id_fixation = row['id_fixation']
            participant = row['participant']
        
            fixation_unique = fixation_k[(fixation_k['id_fixation'] == id_fixation) & (fixation_k['participant'] == participant)]                
            if not fixation_unique.empty: 
                first_time = fixation_unique['time_to_map'].iloc[0]
                last_time = fixation_unique['time_to_map'].iloc[-1]
                time = last_time - first_time
                liste_time.append(time)

                liste_participant.append(participant)
                mean_x = fixation_unique['x'].mean()*width
                mean_y = fixation_unique['y'].mean()*height
                
                liste_centre_x.append(mean_x)
                liste_centre_y.append(mean_y)

        liste_median_time_fixation.append(statistics.median(liste_time))
        liste_median_count_fixation.append(statistics.median(liste_count))
        liste_mean_time_fixation.append(statistics.mean(liste_time))
        liste_mean_count_fixation.append(statistics.mean(liste_count))
        liste_ec_time_fixation.append(statistics.stdev(liste_time))
        liste_ec_count_fixation.append(statistics.stdev(liste_count))
        df_centre_fix = pd.DataFrame({'participant': liste_participant,
                            'x':liste_centre_x, 
                            'y': liste_centre_y
                                    })
        
        # calcul amplitude par personne par carte
        liste_amplitude = []
        for k in range(len(df_centre_fix)-1):
            if df_centre_fix['participant'][k] == df_centre_fix['participant'][k+1]:
                amplitude = np.sqrt((df_centre_fix['x'][k+1] - df_centre_fix['x'][k]) ** 2 + (df_centre_fix['y'][k+1] - df_centre_fix['y'][k]) ** 2)
                liste_amplitude.append(amplitude)
        liste_median_amplitude_fixation.append(statistics.median(liste_amplitude))
        liste_mean_amplitude_fixation.append(statistics.mean(liste_amplitude))
        liste_ec_amplitude_fixation.append(statistics.stdev(liste_amplitude))


        
    donnees = pd.DataFrame({'name': liste_name_c,
                            'median_duration':liste_median_time_fixation, 
                            'median_count': liste_median_count_fixation,
                            'median_amplitude':liste_median_amplitude_fixation,
                            'mean_duration':liste_mean_time_fixation, 
                            'mean_count': liste_mean_count_fixation,
                            'mean_amplitude':liste_mean_amplitude_fixation,
                            'ec_duration':liste_ec_time_fixation, 
                            'ec_count': liste_ec_count_fixation,
                            'ec_amplitude':liste_ec_amplitude_fixation
                                    })
    donnees.to_csv('export_analyse/donnees_stat_fixation.csv', index = False, header = True)


