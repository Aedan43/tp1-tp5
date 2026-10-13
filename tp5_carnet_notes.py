# TP 5 — Projet de synthèse : carnet de notes

from functools import wraps
from datetime import datetime
import json

# Structure des données imposée
etudiants = {
    "L3-001": {
        "nom": "Rakoto",
        "prenom": "Soa",
        "notes": {
            "Python": [15, 14],
            "Réseaux": [12],
        },
    },
    "L3-002": {
        "nom": "Rabe",
        "prenom": "Andry",
        "notes": {
            "Python": [9, 13],
            "Réseaux": [11, 10],
        },
    },
}

historique = []

# Décorateur : journaliser les modifications
def journaliser(fonction):
    @wraps(fonction)
    def enveloppe(*args, **kwargs):
        date_heure = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        historique.append((date_heure, fonction.__name__, args))
        return fonction(*args, **kwargs)

    return enveloppe

# Décorateur : vérifier la note
def note_valide(fonction):
    @wraps(fonction)
    def enveloppe(*args, **kwargs):
        note = args[2]

        if note < 0 or note > 20:
            print("Erreur : la note doit être comprise entre 0 et 20.")
            return None

        return fonction(*args, **kwargs)

    return enveloppe

# Décorateur : vérifier que l'étudiant existe
def etudiant_existe(fonction):
    @wraps(fonction)
    def enveloppe(*args, **kwargs):
        matricule = args[0]

        if matricule not in etudiants:
            print("Erreur : étudiant introuvable.")
            return None

        return fonction(*args, **kwargs)

    return enveloppe

# Ajouter un étudiant
@journaliser
def ajouter_etudiant(matricule, nom, prenom):
    if matricule in etudiants:
        print("Erreur : ce matricule existe déjà.")
        return False

    etudiants[matricule] = {
        "nom": nom,
        "prenom": prenom,
        "notes": {},
    }

    print("Étudiant ajouté.")
    return True

# Ajouter une note
@journaliser
@note_valide
@etudiant_existe
def ajouter_note(matricule, matiere, note):
    etudiants[matricule]["notes"].setdefault(matiere, [])
    etudiants[matricule]["notes"][matiere].append(note)
    print("Note ajoutée.")
    return True

# Moyenne d'une matière
@etudiant_existe
def moyenne_matiere(matricule, matiere):
    notes = etudiants[matricule]["notes"].get(matiere, [])

    if not notes:
        return 0.0

    return sum(notes) / len(notes)

# Moyenne générale
@etudiant_existe
def moyenne_generale(matricule):
    notes_par_matiere = etudiants[matricule]["notes"]

    moyennes = [
        sum(notes) / len(notes)
        for notes in notes_par_matiere.values()
        if notes
    ]

    if not moyennes:
        return 0.0

    return sum(moyennes) / len(moyennes)

# Classement
def classement():
    resultat = []

    for matricule, etudiant in etudiants.items():
        moyenne = moyenne_generale(matricule)
        nom_complet = f"{etudiant['prenom']} {etudiant['nom']}"
        resultat.append((nom_complet, moyenne))

    return sorted(
        resultat,
        key=lambda etudiant: etudiant[1],
        reverse=True
    )

# Majors par matière
def majors():
    matieres = set()

    for etudiant in etudiants.values():
        for matiere in etudiant["notes"]:
            matieres.add(matiere)

    resultat = {}

    for matiere in matieres:
        meilleur_nom = None
        meilleure_moyenne = -1

        for matricule, etudiant in etudiants.items():
            notes = etudiant["notes"].get(matiere, [])

            if notes:
                moyenne = sum(notes) / len(notes)

                if moyenne > meilleure_moyenne:
                    meilleure_moyenne = moyenne
                    meilleur_nom = f"{etudiant['prenom']} {etudiant['nom']}"

        resultat[matiere] = meilleur_nom

    return resultat

# Sauvegarder
def sauvegarder(fichier):
    with open(fichier, "w", encoding="utf-8") as f:
        json.dump(etudiants, f, ensure_ascii=False, indent=2)

    print("Carnet sauvegardé.")

# Charger
def charger(fichier):
    global etudiants

    with open(fichier, "r", encoding="utf-8") as f:
        etudiants = json.load(f)

    print("Carnet chargé.")

# Afficher le bulletin
def afficher_bulletin(matricule):
    if matricule not in etudiants:
        print("Étudiant introuvable.")
        return

    etudiant = etudiants[matricule]

    print()
    print("Bulletin de", etudiant["prenom"], etudiant["nom"])

    for matiere, notes in etudiant["notes"].items():
        moyenne = sum(notes) / len(notes)
        print(
            matiere,
            ":",
            notes,
            "- moyenne :",
            f"{moyenne:.2f}"
        )

    print(
        "Moyenne générale :",
        f"{moyenne_generale(matricule):.2f}"
    )

# Menu
while True:
    print()
    print("1. Ajouter un étudiant")
    print("2. Ajouter une note")
    print("3. Afficher un bulletin")
    print("4. Afficher le classement")
    print("5. Afficher les majors")
    print("6. Afficher l'historique")
    print("7. Sauvegarder")
    print("8. Quitter")

    choix = input("Choix : ")

    if choix == "1":
        matricule = input("Matricule : ")
        nom = input("Nom : ")
        prenom = input("Prénom : ")

        ajouter_etudiant(matricule, nom, prenom)

    elif choix == "2":
        matricule = input("Matricule : ")
        matiere = input("Matière : ")
        note = float(input("Note : "))

        ajouter_note(matricule, matiere, note)

    elif choix == "3":
        matricule = input("Matricule : ")
        afficher_bulletin(matricule)

    elif choix == "4":
        resultat = classement()

        for numero, (nom, moyenne) in enumerate(resultat, start=1):
            print(f"{numero}. {nom:<20} {moyenne:.2f}")

    elif choix == "5":
        resultat = majors()

        for matiere, nom in resultat.items():
            print(f"{matiere} : {nom}")

    elif choix == "6":
        for date_heure, fonction, arguments in historique:
            print(date_heure, fonction, arguments)

    elif choix == "7":
        sauvegarder("carnet_notes.json")

    elif choix == "8":
        print("Au revoir.")
        break

    else:
        print("Choix invalide.")
