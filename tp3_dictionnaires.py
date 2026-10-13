# TP 3 — Le stock d'une épicerie (dictionnaires)

from collections import Counter
import json

stock = {
    "riz":   {"prix": 3200, "quantite": 50},
    "huile": {"prix": 9500, "quantite": 12},
    "sucre": {"prix": 4000, "quantite": 30},
    "savon": {"prix": 1500, "quantite": 0},
}

# 1. Afficher chaque produit avec son prix et sa quantité
for produit, informations in stock.items():
    print(
        produit,
        "- prix :", informations["prix"],
        "Ar - quantité :", informations["quantite"]
    )

# 2. Valeur totale du stock
valeur_totale = 0

for informations in stock.values():
    valeur_totale += informations["prix"] * informations["quantite"]

print("Valeur totale :", valeur_totale, "Ar")

# 3. Produits en rupture de stock (par compréhension)
ruptures = [
    produit
    for produit, informations in stock.items()
    if informations["quantite"] == 0
]

print("Produits en rupture :", ruptures)

# 4. Vendre un produit
def vendre(stock, produit, quantite):
    """Vend une quantité d'un produit. Renvoie le tuple (succes, message)."""
    informations = stock.get(produit)

    if informations is None:
        return False, "Produit inconnu"

    if quantite <= 0:
        return False, "La quantité doit être positive"

    if informations["quantite"] < quantite:
        return False, "Quantité insuffisante"

    informations["quantite"] -= quantite
    return True, "Vente effectuée"

print(vendre(stock, "riz", 5))
print(vendre(stock, "cafe", 2))
print(vendre(stock, "huile", 100))
print(vendre(stock, "sucre", -3))

# 5. Ajouter un produit (refusé s'il existe déjà)
def ajouter_produit(stock, nom, prix, quantite):
    """Ajoute un produit absent du stock. Renvoie le tuple (succes, message)."""
    if nom in stock:
        return False, "Produit déjà présent"

    stock[nom] = {
        "prix": prix,
        "quantite": quantite,
    }

    return True, "Produit ajouté"

print(ajouter_produit(stock, "sel", 1000, 20))
print(ajouter_produit(stock, "riz", 3500, 10))

# 6. Prix augmentés de 10 %, arrondis à l'ariary (compréhension de dictionnaire)
prix_hausse = {
    produit: round(informations["prix"] * 1.10)
    for produit, informations in stock.items()
}

print("Prix après hausse :", prix_hausse)

# 7. Compter les ventes : d'abord avec get, puis avec Counter
ventes = ["riz", "sucre", "riz", "huile", "riz"]

compteur = {}

for produit in ventes:
    compteur[produit] = compteur.get(produit, 0) + 1

print("Avec get :", compteur)
print("Avec Counter :", dict(Counter(ventes)))

# 8. Sauvegarder dans stock.json, recharger et comparer
with open("stock.json", "w", encoding="utf-8") as fichier:
    json.dump(stock, fichier, ensure_ascii=False, indent=2)

with open("stock.json", "r", encoding="utf-8") as fichier:
    stock_recharge = json.load(fichier)

print("Les dictionnaires sont égaux :", stock == stock_recharge)
