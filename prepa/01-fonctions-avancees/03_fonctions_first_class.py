"""
Fonctions comme objets de première classe
=========================================

Démonstration que les fonctions Python peuvent être assignées,
passées en argument, retournées et stockées.
"""

# =============================================================================
# 1. Assigner une fonction à une variable
# =============================================================================

print("=" * 60)
print("1. ASSIGNER UNE FONCTION À UNE VARIABLE")
print("=" * 60)


def saluer(nom):
    return f"Bonjour, {nom} !"


# Assigner la fonction à une autre variable
ma_fonction = saluer

print(f"saluer('Alice') = {saluer('Alice')}")
print(f"ma_fonction('Alice') = {ma_fonction('Alice')}")

# La fonction est un objet
print(f"\ntype(saluer) = {type(saluer)}")
print(f"saluer is ma_fonction : {saluer is ma_fonction}")


# =============================================================================
# 2. Passer une fonction en argument
# =============================================================================

print("\n" + "=" * 60)
print("2. PASSER UNE FONCTION EN ARGUMENT")
print("=" * 60)


def appliquer_operation(valeurs, operation):
    """Applique une opération à chaque élément."""
    return [operation(v) for v in valeurs]


nombres = [1, 2, 3, 4, 5]

# Avec une lambda
carres = appliquer_operation(nombres, lambda x: x ** 2)
print(f"Carrés : {carres}")


# Avec une fonction nommée
def doubler(x):
    return x * 2


doubles = appliquer_operation(nombres, doubler)
print(f"Doubles : {doubles}")


# =============================================================================
# 3. Fonctions built-in utilisant ce pattern
# =============================================================================

print("\n" + "=" * 60)
print("3. FONCTIONS BUILT-IN AVEC CALLBACKS")
print("=" * 60)

# --- sorted() avec key ---
utilisateurs = [
    {"nom": "Alice", "age": 30},
    {"nom": "Bob", "age": 25},
    {"nom": "Charlie", "age": 35}
]

tries_par_age = sorted(utilisateurs, key=lambda u: u["age"])
print("Triés par âge :")
for u in tries_par_age:
    print(f"  {u['nom']} ({u['age']} ans)")

# --- filter() ---
nombres = range(1, 11)
pairs = list(filter(lambda x: x % 2 == 0, nombres))
print(f"\nNombres pairs (filter) : {pairs}")

# --- map() ---
carres = list(map(lambda x: x ** 2, nombres))
print(f"Carrés (map) : {carres}")

# --- reduce() ---
from functools import reduce

somme = reduce(lambda a, b: a + b, nombres)
print(f"Somme (reduce) : {somme}")

produit = reduce(lambda a, b: a * b, range(1, 6))
print(f"Factorielle de 5 (reduce) : {produit}")


# =============================================================================
# 4. Retourner une fonction (Factory pattern)
# =============================================================================

print("\n" + "=" * 60)
print("4. RETOURNER UNE FONCTION (FACTORY)")
print("=" * 60)


def creer_multiplicateur(facteur):
    """Retourne une fonction qui multiplie par le facteur donné."""
    def multiplier(nombre):
        return nombre * facteur
    return multiplier


# Création de fonctions spécialisées
doubler = creer_multiplicateur(2)
tripler = creer_multiplicateur(3)
fois_dix = creer_multiplicateur(10)

print(f"doubler(5) = {doubler(5)}")
print(f"tripler(5) = {tripler(5)}")
print(f"fois_dix(5) = {fois_dix(5)}")

# Chaîner les appels
print(f"\ncreer_multiplicateur(7)(6) = {creer_multiplicateur(7)(6)}")


# =============================================================================
# 5. Stocker des fonctions dans des structures de données
# =============================================================================

print("\n" + "=" * 60)
print("5. STOCKER DES FONCTIONS")
print("=" * 60)


def ajouter(a, b):
    return a + b


def soustraire(a, b):
    return a - b


def multiplier(a, b):
    return a * b


def diviser(a, b):
    return a / b if b != 0 else "Erreur : division par zéro"


# Dictionnaire de fonctions
operations = {
    "+": ajouter,
    "-": soustraire,
    "*": multiplier,
    "/": diviser
}


def calculer(a, operateur, b):
    """Calculatrice simple utilisant un dictionnaire de fonctions."""
    if operateur in operations:
        return operations[operateur](a, b)
    return "Opérateur inconnu"


print(f"10 + 5 = {calculer(10, '+', 5)}")
print(f"10 - 5 = {calculer(10, '-', 5)}")
print(f"10 * 5 = {calculer(10, '*', 5)}")
print(f"10 / 5 = {calculer(10, '/', 5)}")


# =============================================================================
# 6. Attributs des fonctions
# =============================================================================

print("\n" + "=" * 60)
print("6. ATTRIBUTS DES FONCTIONS")
print("=" * 60)


def ma_fonction(a, b, c=10):
    """Documentation de la fonction.

    Cette fonction additionne trois nombres.
    """
    return a + b + c


print(f"__name__ : {ma_fonction.__name__}")
print(f"__doc__ : {ma_fonction.__doc__}")
print(f"__defaults__ : {ma_fonction.__defaults__}")
print(f"__code__.co_varnames : {ma_fonction.__code__.co_varnames}")
print(f"__code__.co_argcount : {ma_fonction.__code__.co_argcount}")

# On peut ajouter des attributs personnalisés !
ma_fonction.version = "1.0"
ma_fonction.auteur = "Formation Python"
print(f"\nAttributs personnalisés :")
print(f"  version : {ma_fonction.version}")
print(f"  auteur : {ma_fonction.auteur}")
