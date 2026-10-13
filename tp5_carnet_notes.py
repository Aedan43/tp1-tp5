# TP 5 — Projet de synthèse : carnet de notes

import json
from datetime import datetime
from functools import wraps

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


# ----- Décorateurs -----

def journaliser(fonction):
    """Ajoute (date et heure, nom de la fonction, arguments) à historique à chaque appel."""
    @wraps(fonction)
    def enveloppe(*args, **kwargs):
        date_heure = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        arguments = args + tuple(kwargs.values())
        historique.append((date_heure, fonction.__name__, arguments))
        return fonction(*args, **kwargs)

    return enveloppe


def note_valide(fonction):
    """Refuse toute note qui n'est pas un nombre compris entre 0 et 20."""
    @wraps(fonction)
    def enveloppe(matricule, matiere, note, *args, **kwargs):
        if not isinstance(note, (int, float)) or not 0 <= note <= 20:
            print("Erreur : la note doit être comprise entre 0 et 20.")
            return False

        return fonction(matricule, matiere, note, *args, **kwargs)

    return enveloppe


def etudiant_existe(fonction):
    """Vérifie que le matricule (premier argument) existe avant d'exécuter la fonction."""
    @wraps(fonction)
    def enveloppe(matricule, *args, **kwargs):
        if matricule not in etudiants:
            print("Erreur : étudiant introuvable.")
            return None

        return fonction(matricule, *args, **kwargs)

    return enveloppe


# ----- Fonctions du carnet -----

@journaliser
def ajouter_etudiant(matricule, nom, prenom):
    """Crée un étudiant ; refuse un matricule déjà existant."""
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


@journaliser
@etudiant_existe
@note_valide
def ajouter_note(matricule, matiere, note):
    """Ajoute une note dans une matière, en créant la matière si besoin."""
    etudiants[matricule]["notes"].setdefault(matiere, [])
    etudiants[matricule]["notes"][matiere].append(note)

    print("Note ajoutée.")
    return True


@etudiant_existe
def moyenne_matiere(matricule, matiere):
    """Renvoie la moyenne d'un étudiant dans une matière, ou None s'il n'a pas de note."""
    notes = etudiants[matricule]["notes"].get(matiere, [])

    if not notes:
        return None

    return sum(notes) / len(notes)


@etudiant_existe
def moyenne_generale(matricule):
    """Renvoie la moyenne des moyennes de matières, ou None s'il n'a aucune note."""
    notes_par_matiere = etudiants[matricule]["notes"]

    moyennes = [
        sum(notes) / len(notes)
        for notes in notes_par_matiere.values()
        if notes
    ]

    if not moyennes:
        return None

    return sum(moyennes) / len(moyennes)


def classement():
    """Renvoie la liste de tuples (nom complet, moyenne), triée par moyenne décroissante."""
    resultat = []

    for matricule, etudiant in etudiants.items():
        moyenne = moyenne_generale(matricule)

        if moyenne is not None:
            nom_complet = f"{etudiant['prenom']} {etudiant['nom']}"
            resultat.append((nom_complet, moyenne))

    return sorted(
        resultat,
        key=lambda element: element[1],
        reverse=True
    )


def majors():
    """Renvoie un dictionnaire matière -> nom complet du meilleur étudiant."""
    matieres = set()

    for etudiant in etudiants.values():
        for matiere in etudiant["notes"]:
            matieres.add(matiere)

    resultat = {}

    for matiere in matieres:
        meilleur_nom = None
        meilleure_moyenne = -1

        for etudiant in etudiants.values():
            notes = etudiant["notes"].get(matiere, [])

            if notes:
                moyenne = sum(notes) / len(notes)

                if moyenne > meilleure_moyenne:
                    meilleure_moyenne = moyenne
                    meilleur_nom = f"{etudiant['prenom']} {etudiant['nom']}"

        if meilleur_nom is not None:
            resultat[matiere] = meilleur_nom

    return resultat


def sauvegarder(fichier):
    """Enregistre le carnet dans un fichier JSON."""
    with open(fichier, "w", encoding="utf-8") as f:
        json.dump(etudiants, f, ensure_ascii=False, indent=2)

    print("Carnet sauvegardé.")


@journaliser
def charger(fichier):
    """Relit le carnet depuis un fichier JSON."""
    global etudiants

    try:
        with open(fichier, "r", encoding="utf-8") as f:
            etudiants = json.load(f)
    except (OSError, json.JSONDecodeError):
        print("Erreur : impossible de charger ce fichier.")
        return False

    print("Carnet chargé.")
    return True


def afficher_bulletin(matricule):
    """Affiche les notes et les moyennes d'un étudiant."""
    if matricule not in etudiants:
        print("Étudiant introuvable.")
        return

    etudiant = etudiants[matricule]

    print()
    print("Bulletin de", etudiant["prenom"], etudiant["nom"])

    for matiere, notes in etudiant["notes"].items():
        if notes:
            moyenne = sum(notes) / len(notes)
            print(matiere, ":", notes, "- moyenne :", f"{moyenne:.2f}")

    moyenne = moyenne_generale(matricule)

    if moyenne is None:
        print("Aucune note pour le moment.")
    else:
        print("Moyenne générale :", f"{moyenne:.2f}")


# ----- Menu -----

def menu():
    """Affiche le menu en boucle et appelle la fonction choisie."""
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

            try:
                note = float(input("Note : "))
            except ValueError:
                print("Erreur : veuillez saisir un nombre.")
                continue

            ajouter_note(matricule, matiere, note)

        elif choix == "3":
            matricule = input("Matricule : ")
            afficher_bulletin(matricule)

        elif choix == "4":
            for numero, (nom, moyenne) in enumerate(classement(), start=1):
                print(f"{numero}. {nom} {moyenne:.2f}")

        elif choix == "5":
            for matiere, nom in majors().items():
                print(f"{matiere} : {nom}")

        elif choix == "6":
            if not historique:
                print("Historique vide.")

            for date_heure, fonction, arguments in historique:
                print(date_heure, fonction, arguments)

        elif choix == "7":
            sauvegarder("carnet_notes.json")

        elif choix == "8":
            print("Au revoir.")
            break

        else:
            print("Choix invalide.")


if __name__ == "__main__":
    menu()
