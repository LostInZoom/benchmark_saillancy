carte_fixation : sortie des carte avec les points de fixation
entree : emplacement du fichier name_im.csv ( l'ordre des images affichées lors d'une session) il faut mettre le fichier correspondant à la session 
heatmap : sortie des heatmaps
recordings : mettre info.player, fixation_on_surface.csv et resultat_carte.csv pour la génération du fichier coord_fixation_on_surface.csv dans 
resultat : fichier coord_fixation_on_image de toutes les images de la session
resultat_enquete : ensemble des coord_fixation_on_surface (notament pour le regroupement des coord)
image : ensemble d'image d'une session



Calcul_fix : fichier permettant de calculer les points de fixation dans une scene 2D
input :
- recordings/info.player.json
- recordings/fixations_on_surface_Surface 1.csv
- recordings/resultat_enquete.csv
output : 
- 'resultat_enquete/coord_fixation_on_map.csv'



regroupement_data : permet de regroupe les points de fixation d'une image dans un fichier pour l'ensemble des participants pour une session  :
input : 
- resultat_enquete/* (ensemble de fichier coord_fixation_on_map_x.csv)
- entree/name_in : lsite et ordre des images affichées
output : 
'resultat/coord_fixation_image.csv'


heatmap : génération des heatmaps et des images avec fixations
input :
 - resultat/* : ensemble des fichiers coord_fixation_image.csv
 - image/* : images correspondante au fichier des coords
output : 
 - heatmap/ ensemble des heatmaps
 - carte_fixation/ ensemble des cartes de fixation 