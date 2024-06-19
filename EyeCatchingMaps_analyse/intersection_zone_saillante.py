import glob
import geopandas as gpd
import numpy as np
from matplotlib.path import Path
import matplotlib.pyplot as plt
from shapely.geometry import Polygon
import cv2
import pandas as pd
from shapely.geometry import Point

import os



def create_polygon_mask(image, polygon_vertices):
    height, width = image.shape[:2]
    
    y, x = np.mgrid[:height, :width]
    
    polygon_path = Path(polygon_vertices)
    
    mask = polygon_path.contains_points(np.vstack((x.flatten(), y.flatten())).T)
    mask = mask.reshape((height, width))
    
    return mask

def valeur_intersection(shapefile,heatmap,name,csv):
    liste_moy = []
    liste_med = []
    liste_max = []
    liste_area = []
    liste_type = []
    liste_name = []
    liste_id = []
    liste_nb_participant = []
    liste_pourcentage = []

    for idx, row in shapefile.iterrows():
        liste_name.append(name)
        exterior_coords = row['geometry'].exterior.coords
        new_exterior_coords = [(x, -y) for x, y in exterior_coords]
        area = Polygon(exterior_coords).area

        polygon_coords = np.array(new_exterior_coords)
        masque_polygone = create_polygon_mask(heatmap, polygon_coords)

        valeurs_dans_polygone = heatmap[masque_polygone]
        liste_moy.append(np.mean(valeurs_dans_polygone))
        liste_med.append(np.median(valeurs_dans_polygone))
        liste_max.append(int(np.max(valeurs_dans_polygone)))
        liste_area.append(area)
        liste_type.append(row['type'])
        liste_id.append(row['id'])
        nbr, pourcentage = intersection_participant(polygon_coords,csv)
        liste_nb_participant.append(nbr)
        liste_pourcentage.append(pourcentage)
    return liste_moy,liste_med,liste_max,liste_area,liste_type,liste_name,liste_id,liste_nb_participant,liste_pourcentage

def intersection_participant(polygone,csv):
    liste_participant= []
    nbr_point =0
    polygone_shapely = Polygon(polygone) 
    for idx, row in csv.iterrows():
        x,y = float(row['width'])*float(row['x']),float(row['height'])*float(row['y'])
        point_obj = Point(x, y)
        if polygone_shapely.contains(point_obj):
            nbr_point+=1
            if row["participant"] not in liste_participant:  # Vérifier si le nom du participant est déjà dans la liste
                liste_participant.append(row["participant"]) 
    return len(liste_participant),nbr_point/len(csv)
if __name__ == '__main__':
        

        
    liste_shapefile = glob.glob('couche_shape/*.shp')
        
    liste_name =[]
    liste_moyenne =[]
    liste_median = []
    liste_max = []
    all_moy =[]
    liste_area = []
    liste_type = []
    liste_id = []
    liste_nb_partipant = []
    liste_pourcentage = []
    
    for path_shapefile in liste_shapefile:
        gdf = gpd.read_file(path_shapefile)
        heatmap_path ='heatmap/heatmap_'+ path_shapefile.split('\\')[1].split('.')[0]+'.jpg' 
        csv_path = 'resultat/coord_fixation_' + path_shapefile.split('\\')[1].split('.')[0]+  '.png.csv'
        if os.path.exists(csv_path):
            csv = pd.read_csv(csv_path)
        else:
            csv_path = 'resultat/coord_fixation_' + path_shapefile.split('\\')[1].split('.')[0] + '.PNG.csv'
            if os.path.exists(csv_path):
                csv = pd.read_csv(csv_path)
            else:
                print("Aucun fichier CSV trouvé pour", path_shapefile.split('\\')[1].split('.')[0])
        #id_fixation,time,x,y,dispersion,image,distance,accuracy,precision,time_to_map,participant,world_index,height,width
        heatmap =  cv2.imread(heatmap_path)
        moy,med,max,area,type,name,id,nb_part,pourcentage = valeur_intersection(gdf,heatmap,path_shapefile.split('\\')[1].split('.')[0],csv)
        liste_name+=name
        liste_moyenne+=moy
        liste_median+=med
        liste_max+=max
        liste_area+=area
        liste_type+=type
        liste_id += id
        liste_nb_partipant += nb_part
        liste_pourcentage += pourcentage

        all_moy += moy
    donnees_zone_saillante = pd.DataFrame({'name': liste_name,
                                           'id':liste_id, 
                                           'moyenne': liste_moyenne,
                                           'median': liste_median,
                                           'max':liste_max,
                                           'area':liste_area,
                                           "type" : liste_type,
                                           'nb_part':liste_nb_partipant,
                                           'pourcentage':liste_pourcentage})
    donnees_zone_saillante.to_csv('donnees_zone_saillante_heatmap.csv', index = False, header = True)

    # plt.hist(all_moy, bins=50, edgecolor='k')
    # plt.show()