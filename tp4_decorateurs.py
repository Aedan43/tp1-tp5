# TP 4 — Atelier décorateurs

from functools import wraps, lru_cache
import time

# 1. @chronometrer
def chronometrer_secondes(fonction):
    @wraps(fonction)
    def enveloppe(*args, **kwargs):
        debut = time.perf_counter()
        resultat = fonction(*args, **kwargs)
        fin = time.perf_counter()

        print(f"{fonction.__name__} a pris {fin - debut:.2f} s")
        return resultat

    return enveloppe

@chronometrer_secondes
def lente():
    time.sleep(1)

lente()

# 2. @majuscules
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

# 3. @compter_appels
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

# 4. @verifier_positifs
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

# 5. @chronometrer(unite="ms")
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

# 6. @memoriser
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

@chronometrer()
def fibonacci_sans_memoire(n):
    def fibonacci(n):
        if n < 2:
            return n
        return fibonacci(n - 1) + fibonacci(n - 2)

    return fibonacci(n)

print("Sans mémorisation :", fibonacci_sans_memoire(30))

@chronometrer()
def fibonacci_avec_memoire(n):
    @memoriser
    def fibonacci(n):
        if n < 2:
            return n
        return fibonacci(n - 1) + fibonacci(n - 2)

    return fibonacci(n)

print("Avec @memoriser :", fibonacci_avec_memoire(30))

@chronometrer()
def fibonacci_avec_lru_cache(n):
    @lru_cache
    def fibonacci(n):
        if n < 2:
            return n
        return fibonacci(n - 1) + fibonacci(n - 2)

    return fibonacci(n)

print("Avec @lru_cache :", fibonacci_avec_lru_cache(30))

# 7. Empilement de décorateurs
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
# L'ordre change donc quelle enveloppe se trouve autour de l'autre.

# 8. MiniFlask
class MiniFlask:
    def __init__(self):
        self.routes = {}
        self.fonction_404 = None

    def route(self, chemin):
        def enregistrer(fonction):
            if chemin in self.routes:
                raise ValueError("Cette URL est déjà enregistrée.")

            self.routes[chemin] = fonction
            return fonction

        return enregistrer

    def traiter(self, chemin):
        fonction = self.routes.get(chemin)

        if fonction:
            return fonction()

        if self.fonction_404:
            return self.fonction_404()

        return "404 : page introuvable"

    def lister_routes(self):
        for chemin in self.routes:
            print(chemin)

    def erreur_404(self, fonction):
        self.fonction_404 = fonction
        return fonction

app = MiniFlask()

@app.route("/")
def accueil():
    return "Bonjour !"

@app.route("/contact")
def contact():
    return "Contact"

@app.erreur_404
def page_introuvable():
    return "404 : page introuvable"

print(app.traiter("/"))
print(app.traiter("/contact"))
print(app.traiter("/inconnue"))

print("Routes :")
app.lister_routes()
