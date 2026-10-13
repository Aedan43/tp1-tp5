# TP 3 — Le stock d'une épicerie (dictionnaires)

from collections import Counter
import json

stock = {
    "riz":   {"prix": 3200, "quantite": 50},
    "huile": {"prix": 9500, "quantite": 12},
    "sucre": {"prix": 4000, "quantite": 30},
    "savon": {"prix": 1500, "quantite": 0},
}

# 1. Afficher chaque produit
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

# 3. Produits en rupture
ruptures = [
    produit
    for produit, informations in stock.items()
    if informations["quantite"] == 0
]

print("Produits en rupture :", ruptures)

# 4. Vendre
def vendre(stock, produit, quantite):
    informations = stock.get(produit)

    if informations is None:
        return False, "Produit inconnu"

    if informations["quantite"] < quantite:
        return False, "Quantité insuffisante"

    informations["quantite"] -= quantite
    return True, "Vente effectuée"

print(vendre(stock, "riz", 5))
print(vendre(stock, "cafe", 2))
print(vendre(stock, "huile", 100))

# 5. Ajouter un produit
def ajouter_produit(stock, nom, prix, quantite):
    if nom in stock:
        return False, "Produit déjà présent"

    stock[nom] = {
        "prix": prix,
        "quantite": quantite,
    }

    return True, "Produit ajouté"

print(ajouter_produit(stock, "sel", 1000, 20))
print(ajouter_produit(stock, "riz", 3500, 10))

# 6. Prix augmentés de 10 %
prix_hausse = {
    produit: round(informations["prix"] * 1.10)
    for produit, informations in stock.items()
}

print("Prix après hausse :", prix_hausse)

# 7. Compter les ventes avec get
ventes = ["riz", "sucre", "riz", "huile", "riz"]

compteur = {}

for produit in ventes:
    compteur[produit] = compteur.get(produit, 0) + 1

print("Avec get :", compteur)

# Avec Counter
print("Avec Counter :", dict(Counter(ventes)))

# 8. Sauvegarder puis recharger en JSON
with open("stock.json", "w", encoding="utf-8") as fichier:
    json.dump(stock, fichier, ensure_ascii=False, indent=2)

with open("stock.json", "r", encoding="utf-8") as fichier:
    stock_recharge = json.load(fichier)

print("Les dictionnaires sont égaux :", stock == stock_recharge)
