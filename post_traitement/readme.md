Calcul_fix : fichier permettant de calculer les points de fixation dans une scene 2D pour toutes les personnes en même temps à l'aide de la fonction suivante : 
calculs_fixation(name_info_player_folder,
                     name_output_folder,
                     name_fixation_folder,
                     name_resultat_folder,
                     name_head_pose_tracker_folder,
                     name_export_folder,
                     name_image_folder)
Il faut remplier les dossiers avec les élèments suivant 

- name_info_player_folder :  dossier contenants les fichiers info.player.json
- name_output_folder =  dossier contenants les fichiers de la calibration de l'eyetracker 
- name_fixation_folder = dossier contenants les fichiers fixations_on_surface_Surface 1.csv
- name_resultat_folder =  dossier contenants les fichiers resultat_enquete.csv 
- name_head_pose_tracke_folderr = dossier contenants les fichiers head_pose_tracker.csv
- name_image_folder = dossier contenants toutes les images pour récupérer leurs dimensions
- name_export_folder = dossier pour l'export 



regroupement_data : permet de regroupe les points de fixation d'une image dans un fichier pour l'ensemble des participants pour une session  :
regroupement_data(name_folder_input,name_output_folder)
input : 
- name_folder_input:dossier contenants les fichiers coord_fixation_on_map_x.csv
- name_output_folder : dossier pour l'ecport 

heatmap: generation of heatmaps and images with bindings
input :
 - resultat/*: set of coord_fixation_image.csv files
 - image/* : images corresponding to the coords file