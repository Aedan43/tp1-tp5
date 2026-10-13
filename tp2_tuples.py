# TP 2 — Les villes de Madagascar (tuples)

import math
from collections import namedtuple

villes = [
    ("Antananarivo", -18.88, 47.51),
    ("Toamasina", -18.15, 49.40),
    ("Mahajanga", -15.72, 46.32),
    ("Fianarantsoa", -21.45, 47.09),
]

# 1. Parcourir la liste en déballant chaque tuple
for nom, latitude, longitude in villes:
    print(f"{nom} : {latitude}, {longitude}")

# 2. Ville la plus au nord : la latitude la plus grande
ville_nord = max(villes, key=lambda ville: ville[1])
print("Ville la plus au nord :", ville_nord[0])

# 3. Bornes des latitudes et des longitudes
def bornes(villes):
    """Renvoie le tuple (lat_min, lat_max, lon_min, lon_max)."""
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
    """Renvoie la distance euclidienne en degrés entre deux tuples (latitude, longitude)."""
    return math.dist(p1, p2)

p1 = (villes[0][1], villes[0][2])
p2 = (villes[1][1], villes[1][2])
print("Distance Antananarivo - Toamasina :", distance(p1, p2))

# 5. Dictionnaire des distances pour toutes les paires de villes
distances = {}

for i in range(len(villes)):
    for j in range(i + 1, len(villes)):
        nom1, lat1, lon1 = villes[i]
        nom2, lat2, lon2 = villes[j]
        distances[(nom1, nom2)] = distance((lat1, lon1), (lat2, lon2))

for paire, valeur in distances.items():
    print(paire, ":", valeur)

print("Nombre de paires :", len(distances))

# 6. Un tuple n'est pas modifiable
try:
    villes[0][1] = -19.00
except TypeError:
    print("Erreur : un tuple ne peut pas être modifié.")

# Pour « corriger » une ville, on crée un nouveau tuple
ville_corrigee = (villes[0][0], -19.00, villes[0][2])
print("Nouveau tuple :", ville_corrigee)

# 7. Bonus : namedtuple et distance réelle en kilomètres (formule de haversine)
Ville = namedtuple("Ville", ["nom", "latitude", "longitude"])

villes_nommees = [Ville(*ville) for ville in villes]

for ville in villes_nommees:
    print(ville.nom, ville.latitude, ville.longitude)

def distance_km(ville1, ville2):
    """Renvoie la distance réelle approximative en km entre deux Ville (haversine)."""
    rayon_terre = 6371
    lat1 = math.radians(ville1.latitude)
    lat2 = math.radians(ville2.latitude)
    delta_lat = lat2 - lat1
    delta_lon = math.radians(ville2.longitude - ville1.longitude)

    a = (math.sin(delta_lat / 2) ** 2
         + math.cos(lat1) * math.cos(lat2) * math.sin(delta_lon / 2) ** 2)

    return 2 * rayon_terre * math.asin(math.sqrt(a))

print(
    "Distance Antananarivo - Toamasina (km) :",
    round(distance_km(villes_nommees[0], villes_nommees[1]), 2)
)
