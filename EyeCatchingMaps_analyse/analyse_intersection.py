
import pandas as pd
import matplotlib.pyplot as plt
donnee_zone_saillante = pd.read_csv('export_analyse/donnees_zone_saillante_heatmap.csv')
donnee_dist_hist = pd.read_csv('export_analyse/donnees_distance_hist.csv')
donnee_homogene_objet = pd.read_csv('export_analyse/donnees_homogene_objet.csv')
donnee_dist_hist_objet = pd.read_csv('export_analyse/donnees_distance_hist_objet.csv')
donnee_homogene_image = pd.read_csv('export_analyse/donnees_zone_homogene_image.csv')
donnee_dist_hist_hotspot_map = pd.read_csv('export_analyse/donnees_distance_hist_hotspot_map.csv')
donnee_dist_hist_hotspot_buffer  = pd.read_csv('export_analyse/donnees_distance_hist_hotspot_buffer.csv')
donne_stat_fixation = pd.read_csv('export_analyse/donnees_stat_fixation.csv')

donne_edge = pd.read_csv('export_analyse/donnees_edges.csv')

donne_segmentation_20 = pd.read_csv('export_analyse/donnees_segmentation_20.csv')
donne_segmentation_50 = pd.read_csv('export_analyse/donnees_segmentation_50.csv')
donne_segmentation_100 = pd.read_csv('export_analyse/donnees_segmentation_100.csv')
donne_segmentation_200 = pd.read_csv('export_analyse/donnees_segmentation_200.csv')


# donnee_zone_saillante.boxplot(column='moyenne', by='area')
# plt.hist(donnee_zone_saillante["max"], bins=30,edgecolor='k')
# plt.hist(donnee_zone_saillante["area"], bins=50, edgecolor='k')
# type_counts = donnee_zone_saillante['type'].value_counts()
# type_counts.plot(kind='bar', color='skyblue')

# df_hotspot = donnee_homogene_objet[donnee_homogene_objet['name'] == 'ecran_ign_8_2']
# plt.hist(df_hotspot["max"], bins=50, edgecolor='k')
# plt.show()
# plt.hist(donnee_zone_saillante["area"], bins=50, edgecolor='k')

# df_high = donnee_zone_saillante[donnee_zone_saillante["area"]>50000]
# export = pd.DataFrame({'name': df_high_ho['name'],
#                         'id':df_high_ho['id'], })
# export.to_csv('donnees_hotspot_area.csv', index = False, header = True)
# df_hotspot_max = df_hotspot[df_hotspot['max_heatmap'] >175]

# df_hotspot_high.boxplot(column='max', by='type')
# plt.hist(df_hotspot['densite_edge'], bins=50, edgecolor='k')
# plt.hist(df_high_ho["nb_part"], bins=50, edgecolor='k')
# hotspot_counts = df_hotspot['type'].value_counts()
# hotspot_percentages = (hotspot_counts / type_counts) 

# hotspot_percentages.plot(kind='bar', color='skyblue')

 
# plt.hist(donnee_dist_hist_hotspot_map["distance"], bins=30, edgecolor='k')


# plt.hist(donnee_dist_hist_objet["distance"], bins=50, edgecolor='k')
# plt.hist(donnee_homogene_objet["moyenne"], bins=50, edgecolor='k')
# plt.hist(donnee_homogene_objet["moyenne_heatmap"], bins=50, edgecolor='k')
# df_topo = donnee_dist_hist_objet[donnee_dist_hist_objet["name"] == "ecran_gm_12_2"] 
# plt.hist(df_topo["distance"], bins=50, edgecolor='k')



fig, axs = plt.subplots(3, 1, figsize=(10, 15))
axs[0].hist(donne_edge["densite"], bins=50, edgecolor='k')
axs[1].hist(donne_edge["densite_buffer"], bins=50, edgecolor='k')
axs[2].hist(donne_edge["densite_map"], bins=50, edgecolor='k')

plt.show()
