# TP 1 — Les notes d'une classe (listes)

notes = [12, 8, 15, 17, 9, 11, 14, 6, 13, 16]

# 1. Nombre de notes, moyenne, minimum et maximum
print("Nombre de notes :", len(notes))
print(f"Moyenne : {sum(notes) / len(notes):.2f}")
print("Note minimale :", min(notes))
print("Note maximale :", max(notes))

# 2. Notes >= 10 (par compréhension) et nombre d'ajournés
admis = [note for note in notes if note >= 10]
nombre_ajournes = len(notes) - len(admis)

print("Notes >= 10 :", admis)
print("Nombre d'ajournés :", nombre_ajournes)

# 3. Tri sans modifier la liste d'origine, puis trois meilleures notes
notes_triees = sorted(notes)
print("Notes triées :", notes_triees)
print("Liste d'origine :", notes)

trois_meilleures = sorted(notes, reverse=True)[:3]
print("Trois meilleures notes :", trois_meilleures)

# 4. Délibération : +2 points aux notes < 10, sans dépasser 10
notes_deliberees = [
    min(note + 2, 10) if note < 10 else note
    for note in notes
]
print("Notes après délibération :", notes_deliberees)

# 5. Histogramme : une étoile par note, par tranche
def histogramme(notes):
    """Affiche une étoile par note pour chaque tranche de notes."""
    tranche_0_4 = 0
    tranche_5_9 = 0
    tranche_10_14 = 0
    tranche_15_20 = 0

    for note in notes:
        if note <= 4:
            tranche_0_4 += 1
        elif note <= 9:
            tranche_5_9 += 1
        elif note <= 14:
            tranche_10_14 += 1
        else:
            tranche_15_20 += 1

    print("0-4   |", "*" * tranche_0_4)
    print("5-9   |", "*" * tranche_5_9)
    print("10-14 |", "*" * tranche_10_14)
    print("15-20 |", "*" * tranche_15_20)

histogramme(notes)

# 6. Rang d'une note dans le classement décroissant
def rang(notes, note):
    """Renvoie la position de la note dans le classement décroissant (1 = meilleure)."""
    classement = sorted(notes, reverse=True)
    return classement.index(note) + 1

print("Rang de 14 :", rang(notes, 14))

# 7. Bonus : fusion sans doublons, en gardant l'ordre de première apparition
autres_notes = [15, 6, 18]
fusion = notes + autres_notes
sans_doublons = []

for note in fusion:
    if note not in sans_doublons:
        sans_doublons.append(note)

print("Fusion sans doublons :", sans_doublons)
