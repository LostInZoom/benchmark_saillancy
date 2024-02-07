import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image
import numpy as np


image_path = "image/ecran_ign_monument_16_c.png"  
image = Image.open(image_path)
plt.imshow(image)


trajets_df = pd.read_csv("resultat/coord_fixation_ecran_ign_monument_16_c.png.csv")  # Remplacez par le nom de votre fichier CSV
image_width, image_height = image.size
participants = trajets_df["participant"].unique()[:3]
couleurs = ['blue', 'green', 'red',  'magenta', 'yellow', 'black',
            'orange', 'purple', 'brown', 'pink', 'gray', 'olive', 'lime',
            'teal', 'lavender', 'coral', 'navy', 'gold', 'maroon',
            'darkcyan','cyan', 'darkgreen']
print(participants)
for i, participant_id in enumerate(participants):
    
    trajet_participant = trajets_df[trajets_df["participant"] == participant_id]
    x = trajet_participant["x"] * image_width
    y = trajet_participant["y"] * image_height
    
    # Tracer les points de départ
    plt.scatter(x, y, color=couleurs[i], marker='o')
    
    # Tracer une ligne reliant chaque paire de points dans le trajet
    plt.plot(x, y, color=couleurs[i])

plt.axis('off')
plt.show()
plt.save
