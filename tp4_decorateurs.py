# TP 4 — Atelier décorateurs

import time
from functools import wraps, lru_cache

# 1. @chronometrer : affiche le temps d'exécution
def chronometrer(fonction):
    @wraps(fonction)
    def enveloppe(*args, **kwargs):
        debut = time.perf_counter()
        resultat = fonction(*args, **kwargs)
        fin = time.perf_counter()

        print(f"{fonction.__name__} a pris {fin - debut:.2f} s")
        return resultat

    return enveloppe

@chronometrer
def lente():
    time.sleep(1)

lente()

# 2. @majuscules : met en majuscules le texte renvoyé
def majuscules(fonction):
    @wraps(fonction)
    def enveloppe(*args, **kwargs):
        resultat = fonction(*args, **kwargs)
        return resultat.upper()

    return enveloppe

@majuscules
def bonjour():
    return "bonjour"

print(bonjour())

# 3. @compter_appels : compte les appels dans l'attribut appels
def compter_appels(fonction):
    @wraps(fonction)
    def enveloppe(*args, **kwargs):
        enveloppe.appels += 1
        return fonction(*args, **kwargs)

    enveloppe.appels = 0
    return enveloppe

@compter_appels
def saluer(nom):
    return f"Bonjour {nom}"

print(saluer("Soa"))
print(saluer("Rabe"))
print(saluer("Andry"))
print("Nombre d'appels :", saluer.appels)

# 4. @verifier_positifs : refuse les arguments numériques négatifs
def verifier_positifs(fonction):
    @wraps(fonction)
    def enveloppe(*args, **kwargs):
        for valeur in args:
            if isinstance(valeur, (int, float)) and valeur < 0:
                raise ValueError("Les valeurs numériques doivent être positives.")

        for valeur in kwargs.values():
            if isinstance(valeur, (int, float)) and valeur < 0:
                raise ValueError("Les valeurs numériques doivent être positives.")

        return fonction(*args, **kwargs)

    return enveloppe

@verifier_positifs
def surface(longueur, largeur):
    return longueur * largeur

print("Surface :", surface(5, 4))

try:
    print(surface(-5, 4))
except ValueError as erreur:
    print(erreur)

# 5. @chronometrer(unite="ms") : le décorateur de la question 1 avec un paramètre
# À partir d'ici, chronometrer prend un paramètre : on l'écrit
# @chronometrer() (secondes) ou @chronometrer(unite="ms") (millisecondes).
def chronometrer(unite="s"):
    def decorateur(fonction):
        @wraps(fonction)
        def enveloppe(*args, **kwargs):
            debut = time.perf_counter()
            resultat = fonction(*args, **kwargs)
            fin = time.perf_counter()

            duree = fin - debut

            if unite == "ms":
                print(f"{fonction.__name__} a pris {duree * 1000:.2f} ms")
            else:
                print(f"{fonction.__name__} a pris {duree:.2f} s")

            return resultat

        return enveloppe

    return decorateur

@chronometrer(unite="ms")
def attente():
    time.sleep(1)

attente()

# 6. @memoriser : mémorise les résultats, avec les arguments (un tuple) comme clé
def memoriser(fonction):
    cache = {}

    @wraps(fonction)
    def enveloppe(*args):
        if args in cache:
            return cache[args]

        resultat = fonction(*args)
        cache[args] = resultat
        return resultat

    return enveloppe

# Fonction récursive de l'énoncé
def fibonacci(n):
    if n < 2:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)

# Même fonction, avec @memoriser puis avec @lru_cache
@memoriser
def fibonacci_memo(n):
    if n < 2:
        return n
    return fibonacci_memo(n - 1) + fibonacci_memo(n - 2)

@lru_cache(maxsize=None)
def fibonacci_lru(n):
    if n < 2:
        return n
    return fibonacci_lru(n - 1) + fibonacci_lru(n - 2)

# On chronomètre l'appel de fibonacci(30), pas chaque appel récursif :
# décorer la fonction elle-même afficherait un temps à chaque appel récursif.
print("Sans mémorisation :", chronometrer(unite="ms")(fibonacci)(30))
print("Avec @memoriser :", chronometrer(unite="ms")(fibonacci_memo)(30))
print("Avec @lru_cache :", chronometrer(unite="ms")(fibonacci_lru)(30))

# 7. Empilement de @chronometrer et @compter_appels, dans les deux ordres
@chronometrer()
@compter_appels
def fonction_a():
    return "Fonction A"

@compter_appels
@chronometrer()
def fonction_b():
    return "Fonction B"

print(fonction_a())
print(fonction_a())
print("Appels de fonction_a :", fonction_a.appels)

print(fonction_b())
print(fonction_b())
print("Appels de fonction_b :", fonction_b.appels)

# Les décorateurs s'appliquent de bas en haut.
# fonction_a = chronometrer()(compter_appels(f)) : le compteur est dans l'enveloppe
# intérieure. @wraps a copié appels (valeur 0) sur l'enveloppe extérieure, qui est
# la seule visible : fonction_a.appels reste donc à 0.
# fonction_b = compter_appels(chronometrer()(f)) : l'enveloppe extérieure est celle
# du compteur, donc fonction_b.appels vaut bien 2. La durée est mesurée dans les deux cas.

# 8. MiniFlask : doublons refusés, lister_routes et erreur 404 personnalisée
class MiniFlask:
    def __init__(self):
        self.routes = {}
        self.fonction_404 = None

    def route(self, chemin):
        if chemin in self.routes:
            raise ValueError("Cette URL est déjà enregistrée : " + chemin)

        def enregistrer(fonction):
            self.routes[chemin] = fonction
            return fonction

        return enregistrer

    def erreur_404(self, fonction):
        self.fonction_404 = fonction
        return fonction

    def lister_routes(self):
        for chemin in self.routes:
            print(chemin)

    def traiter(self, chemin):
        fonction = self.routes.get(chemin)

        if fonction:
            return fonction()

        if self.fonction_404:
            return self.fonction_404()

        return "404 : page introuvable"

app = MiniFlask()

@app.route("/")
def accueil():
    return "Bonjour !"

@app.route("/contact")
def contact():
    return "Contact"

@app.erreur_404
def page_introuvable():
    return "404 : page introuvable (personnalisée)"

try:
    @app.route("/")
    def autre_accueil():
        return "Doublon"
except ValueError as erreur:
    print(erreur)

print(app.traiter("/"))
print(app.traiter("/contact"))
print(app.traiter("/inconnue"))

print("Routes :")
app.lister_routes()
