"""
Décorateurs - Bases
===================

Introduction aux décorateurs Python : syntaxe, mécanisme et exemples simples.
"""

from functools import wraps
import time

# =============================================================================
# 1. Qu'est-ce qu'un décorateur ?
# =============================================================================

print("=" * 60)
print("1. QU'EST-CE QU'UN DÉCORATEUR ?")
print("=" * 60)


def mon_decorateur(func):
    def wrapper(*args, **kwargs):
        print("  Avant l'appel")
        resultat = func(*args, **kwargs)
        print("  Après l'appel")
        return resultat
    return wrapper


@mon_decorateur
def dire_bonjour(nom):
    print(f"  Bonjour, {nom} !")


print("Appel de dire_bonjour('Alice') :")
dire_bonjour("Alice")


# =============================================================================
# 2. Équivalence avec/sans sucre syntaxique
# =============================================================================

print("\n" + "=" * 60)
print("2. ÉQUIVALENCE SYNTAXIQUE")
print("=" * 60)


# Avec @ (recommandé)
@mon_decorateur
def fonction_decoree():
    print("  Je suis décorée")


# Sans @ (équivalent)
def fonction_originale():
    print("  Je suis originale")


fonction_manuelle = mon_decorateur(fonction_originale)

print("Avec @mon_decorateur :")
fonction_decoree()

print("\nSans @ (manuellement) :")
fonction_manuelle()


# =============================================================================
# 3. Décorateur de mesure de temps
# =============================================================================

print("\n" + "=" * 60)
print("3. DÉCORATEUR DE MESURE DE TEMPS")
print("=" * 60)


def mesurer_temps(func):
    """Mesure et affiche le temps d'exécution."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        debut = time.perf_counter()
        resultat = func(*args, **kwargs)
        fin = time.perf_counter()
        print(f"  {func.__name__} a pris {fin - debut:.4f} secondes")
        return resultat
    return wrapper


@mesurer_temps
def calcul_long():
    """Simule un calcul long."""
    time.sleep(0.5)
    return "Terminé"


@mesurer_temps
def somme_nombres(n):
    """Calcule la somme de 0 à n."""
    return sum(range(n + 1))


print("calcul_long() :")
resultat = calcul_long()
print(f"  Résultat : {resultat}")

print("\nsomme_nombres(1000000) :")
resultat = somme_nombres(1000000)
print(f"  Résultat : {resultat}")


# =============================================================================
# 4. L'importance de @wraps
# =============================================================================

print("\n" + "=" * 60)
print("4. L'IMPORTANCE DE @wraps")
print("=" * 60)


def sans_wraps(func):
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper


def avec_wraps(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper


@sans_wraps
def fonction_a():
    """Documentation de A"""
    pass


@avec_wraps
def fonction_b():
    """Documentation de B"""
    pass


print("Sans @wraps :")
print(f"  __name__ : {fonction_a.__name__}")  # 'wrapper'
print(f"  __doc__  : {fonction_a.__doc__}")   # None

print("\nAvec @wraps :")
print(f"  __name__ : {fonction_b.__name__}")  # 'fonction_b'
print(f"  __doc__  : {fonction_b.__doc__}")   # 'Documentation de B'


# =============================================================================
# 5. Chaînage de décorateurs
# =============================================================================

print("\n" + "=" * 60)
print("5. CHAÎNAGE DE DÉCORATEURS")
print("=" * 60)


def gras(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        return f"<b>{func(*args, **kwargs)}</b>"
    return wrapper


def italique(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        return f"<i>{func(*args, **kwargs)}</i>"
    return wrapper


def souligne(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        return f"<u>{func(*args, **kwargs)}</u>"
    return wrapper


@gras
@italique
def message():
    return "Bonjour"


@souligne
@gras
@italique
def message_complet():
    return "Important"


print(f"message() = {message()}")
# <b><i>Bonjour</i></b>

print(f"message_complet() = {message_complet()}")
# <u><b><i>Important</i></b></u>

print("\nOrdre d'application : de bas en haut")
print("Équivalent à : gras(italique(message))")


# =============================================================================
# 6. Décorateurs de méthodes de classe
# =============================================================================

print("\n" + "=" * 60)
print("6. DÉCORATEURS DE MÉTHODES")
print("=" * 60)


def log_method(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        print(f"  Appel de {func.__name__} sur {self.__class__.__name__}")
        return func(self, *args, **kwargs)
    return wrapper


class Calculatrice:
    @log_method
    def additionner(self, a, b):
        return a + b

    @log_method
    def multiplier(self, a, b):
        return a * b


calc = Calculatrice()

print("calc.additionner(2, 3) :")
resultat = calc.additionner(2, 3)
print(f"  Résultat : {resultat}")

print("\ncalc.multiplier(4, 5) :")
resultat = calc.multiplier(4, 5)
print(f"  Résultat : {resultat}")
