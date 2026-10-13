# TP 2 — Les villes de Madagascar (tuples)

import math
from collections import namedtuple

villes = [
    ("Antananarivo", -18.88, 47.51),
    ("Toamasina", -18.15, 49.40),
    ("Mahajanga", -15.72, 46.32),
    ("Fianarantsoa", -21.45, 47.09),
]

# 1. Parcourir et déballer les tuples
for nom, latitude, longitude in villes:
    print(f"{nom} : {latitude}, {longitude}")

# 2. Ville la plus au nord
ville_nord = max(villes, key=lambda ville: ville[1])
print("Ville la plus au nord :", ville_nord[0])

# 3. Bornes
def bornes(villes):
    latitudes = [ville[1] for ville in villes]
    longitudes = [ville[2] for ville in villes]

    return min(latitudes), max(latitudes), min(longitudes), max(longitudes)

lat_min, lat_max, lon_min, lon_max = bornes(villes)

print("Latitude minimale :", lat_min)
print("Latitude maximale :", lat_max)
print("Longitude minimale :", lon_min)
print("Longitude maximale :", lon_max)

# 4. Distance euclidienne en degrés
def distance(p1, p2):
    return math.dist(p1, p2)

p1 = (villes[0][1], villes[0][2])
p2 = (villes[1][1], villes[1][2])

print("Distance Antananarivo - Toamasina :", distance(p1, p2))

# 5. Dictionnaire de toutes les paires possibles
distances = {}

for i in range(len(villes)):
    for j in range(i + 1, len(villes)):
        nom1, lat1, lon1 = villes[i]
        nom2, lat2, lon2 = villes[j]

        distances[(nom1, nom2)] = distance(
            (lat1, lon1),
            (lat2, lon2)
        )

for paire, valeur in distances.items():
    print(paire, ":", valeur)

print("Nombre de paires :", len(distances))

# 6. Un tuple n'est pas modifiable
try:
    villes[0][1] = -19.00
except TypeError:
    print("Erreur : un tuple ne peut pas être modifié.")

# Pour corriger une ville, on crée un nouveau tuple
ville_corrigee = ("Antananarivo", -19.00, 47.51)
print("Nouveau tuple :", ville_corrigee)

# 7. Bonus : namedtuple
# Le PDF demande ensuite la formule de haversine mais ne donne pas cette
# formule dans la leçon. Pour ne pas ajouter une leçon extérieure au PDF,
# on se limite ici à la partie namedtuple enseignée dans le cours.

Ville = namedtuple("Ville", ["nom", "latitude", "longitude"])

villes_nommees = [
    Ville("Antananarivo", -18.88, 47.51),
    Ville("Toamasina", -18.15, 49.40),
    Ville("Mahajanga", -15.72, 46.32),
    Ville("Fianarantsoa", -21.45, 47.09),
]

for ville in villes_nommees:
    print(ville.nom, ville.latitude, ville.longitude)
