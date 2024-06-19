from ajout_cercle import calcul_stat_centre 
import glob
import os 
from PIL import Image
import csv

import pandas as pd
from dist_center import calcul_dist_centre 
from statsmodels.stats.multicomp import pairwise_tukeyhsd
import matplotlib.pyplot as plt

import statsmodels.api as sm
from statsmodels.formula.api import ols

if __name__ == '__main__':

    liste_resultat = glob.glob('resultat/*')
    liste_heatmap = glob.glob('heatmap/*')
    liste_heatmap_paint = glob.glob('paint/saliencyMaps/*')
    name_google = pd.read_csv('autre/name_im_google.csv')
    heatmap = []
    heatmap_paint = []
    for i in range(len(liste_heatmap)):
        assert os.path.exists(liste_heatmap[i])
        
        heatmap.append(Image.open(liste_heatmap[i]))
    for i in range(len(liste_heatmap_paint)):
        assert os.path.exists(liste_heatmap_paint[i])
        
        heatmap_paint.append(Image.open(liste_heatmap_paint[i]))

    fixation = []
    for i in range(len(liste_resultat)):
        assert os.path.exists(liste_resultat[i])
        
        fixation.append(pd.read_csv(liste_resultat[i]))

    # donnée distance avec le centre

    donnees_globales = pd.DataFrame(columns=['distance', 'participant', 'type_map', 'fdc'])
    for k in range(len(fixation)):
        donnees_calculées, _ = calcul_dist_centre(fixation[k], liste_resultat[k],name_google)
        donnees_globales = pd.concat([donnees_globales, donnees_calculées], ignore_index=True)
    donnees_globales.to_csv('donnee_distance_centre.csv', index = False, header = True)


    # plt.figure(figsize=(8, 6))
    # plt.boxplot([donnees_globales[donnees_globales['fdc'] == 'autre']['mean_distance'],
    #              donnees_globales[donnees_globales['fdc'] == 'gm']['mean_distance'],
    #              donnees_globales[donnees_globales['fdc'] == 'ign']['mean_distance'],
    #              donnees_globales[donnees_globales['fdc'] == 'osm']['mean_distance']],
    #             labels=['autre', 'gm', 'ign', 'osm'])
    # plt.xlabel('FDC')
    # plt.ylabel('mean_distance')
    # plt.grid(True)
    # plt.show()

    # Modèle d'ANOVA à mesures répétées
    # modele_anova = ols('mean_distance ~ C(type_map) + C(fdc) + C(participant) + C(type_map):C(fdc) + C(type_map):C(participant) + C(fdc):C(participant)', data=donnees_globales).fit()

    # # Afficher les résultats de l'ANOVA
    # table_anova = sm.stats.anova_lm(modele_anova, typ=2)
    # print(table_anova)
    print("tukey_results_fdc :")

    tukey_results_fdc = pairwise_tukeyhsd(donnees_globales['mean_distance'], donnees_globales['fdc'])
    print(tukey_results_fdc)




    liste_moyenne = []
    liste_ecart_type = []
    liste_median = []
    liste_name = []
    liste_type_map = []
    liste_fdc = []
    #heatmap_benchmark
    # for k in range(len(heatmap)):
    #     name = liste_heatmap[k].split('\\')[1]
    #     moyenne,ecart_type, median = calcul_stat_centre(heatmap[k],50)
    #     liste_moyenne.append(moyenne)
    #     liste_ecart_type.append(ecart_type)
    #     liste_median.append(median)
    #     liste_name.append(name)
    #     type_map = name.split('_')[1]
    #     if type_map == "ecran" or type_map =="portable" or type_map =="postable":
    #         if type_map =="postable":
    #             liste_type_map.append("portable")
    #         else :
    #             liste_type_map.append(type_map)
    #         liste_fdc.append(name.split('_')[2])
    #     else :
    #         liste_type_map.append("autre")
    #         name_image = name.split('_')[1]
    #         if name_image.startswith("SYNC"):
    #             liste_fdc.append("gm")
    #         else:
    #             liste_fdc.append("autre")
        
    # for k in range(len(heatmap_paint)):
    #     moyenne,ecart_type, median = calcul_stat_centre(heatmap_paint[k],50)
    #     liste_moyenne.append(moyenne)
    #     liste_ecart_type.append(ecart_type)
    #     liste_median.append(median)
    #     liste_name.append(name)
    #     liste_type_map.append("paint")
    #     liste_fdc.append("paint")
        

    # donnees_biais_centrale = pd.DataFrame({'name': liste_name,'moyenne': liste_moyenne,'ecart_type': liste_ecart_type,'median': liste_median, 'fdc':liste_fdc, 'type_map':liste_type_map})
    # donnees_biais_centrale.to_csv('donnee_biais_centrale.csv', index = False, header = True)

    # plt.figure(figsize=(8, 6))
    # plt.boxplot([donnees_biais_centrale[donnees_biais_centrale['type_map'] == 'autre']['moyenne'],
    #             donnees_biais_centrale[donnees_biais_centrale['type_map'] == 'portable']['moyenne'],
    #             donnees_biais_centrale[donnees_biais_centrale['type_map'] == 'paint']['moyenne'],
    #             donnees_biais_centrale[donnees_biais_centrale['type_map'] == 'ecran']['moyenne']],
    #             labels=['autre', 'portable', 'ecran','paint'])
    # plt.xlabel('type_map')
    # plt.ylabel('moyenne')
    # plt.grid(True)
    # plt.show()



    # modele_anova = ols('median ~ C(type_map) + C(fdc) ', data=donnees_biais_centrale).fit()

    # table_anova = sm.stats.anova_lm(modele_anova, typ=2)

    # print("anova :")
    # print(table_anova)

    # print("tukey_results_type_map :")

    # tukey_results_type_map = pairwise_tukeyhsd(donnees_biais_centrale['median'], donnees_biais_centrale['type_map'])
    # print(tukey_results_type_map)

    # print("tukey_results_fdc :")

    # tukey_results_fdc = pairwise_tukeyhsd(donnees_biais_centrale['median'], donnees_biais_centrale['fdc'])
    # print(tukey_results_fdc)