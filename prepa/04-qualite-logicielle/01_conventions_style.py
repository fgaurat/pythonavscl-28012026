"""
Conventions de style Python
===========================

PEP8, PEP20 (Zen de Python) et bonnes pratiques de formatage.
"""

# =============================================================================
# 1. Le Zen de Python (PEP20)
# =============================================================================

print("=" * 60)
print("1. LE ZEN DE PYTHON (PEP20)")
print("=" * 60)

# Exécutez : import this
# Pour voir les 19 principes du Zen de Python

print("""
Principes clés :

1. Beautiful is better than ugly.
   → Code lisible, bien formaté

2. Explicit is better than implicit.
   → Noms clairs, pas de magie cachée

3. Simple is better than complex.
   → Solution la plus simple possible

4. Flat is better than nested.
   → Éviter l'imbrication excessive

5. Readability counts.
   → Le code est lu plus souvent qu'il n'est écrit

6. Errors should never pass silently.
   → Gestion explicite des erreurs

7. There should be one obvious way to do it.
   → Éviter les alternatives confuses
""")


# =============================================================================
# 2. PEP8 : Indentation et longueur de ligne
# =============================================================================

print("\n" + "=" * 60)
print("2. PEP8 : INDENTATION ET LONGUEUR DE LIGNE")
print("=" * 60)

# Règle : 4 espaces pour l'indentation (pas de tabs)


def fonction_bien_indentee():
    """Exemple d'indentation correcte."""
    if True:
        faire_quelque_chose = "ok"
        print(f"  Indentation correcte : {faire_quelque_chose}")


fonction_bien_indentee()


# Règle : 79-88 caractères max par ligne (selon les équipes)
# Continuation avec parenthèses (préféré)
resultat = (
    "une très longue chaîne "
    "qui continue sur plusieurs lignes "
    "pour rester lisible"
)
print(f"  Continuation avec parenthèses : {resultat[:30]}...")

# Continuation pour les appels de fonction


def fonction_avec_parametres_longs(
    premier_argument,
    second_argument,
    troisieme_argument,
):
    """Paramètres sur plusieurs lignes."""
    return premier_argument + second_argument + troisieme_argument


print(f"  Résultat : {fonction_avec_parametres_longs(1, 2, 3)}")


# =============================================================================
# 3. PEP8 : Imports
# =============================================================================

print("\n" + "=" * 60)
print("3. PEP8 : IMPORTS")
print("=" * 60)

print("""
Ordre des imports (isort les trie automatiquement) :

1. Bibliothèque standard
   import os
   import sys

2. Bibliothèques tierces
   import requests
   import pandas as pd

3. Imports locaux
   from mon_projet import mon_module
   from mon_projet.utils import helper

Règles :
- Un import par ligne
- Éviter : from module import *
""")

# Exemple correct
import os
import sys
from typing import List, Optional

print(f"  os.name : {os.name}")
print(f"  sys.version : {sys.version[:20]}...")


# =============================================================================
# 4. PEP8 : Conventions de nommage
# =============================================================================

print("\n" + "=" * 60)
print("4. PEP8 : CONVENTIONS DE NOMMAGE")
print("=" * 60)

# Constantes : SCREAMING_SNAKE_CASE
MAX_CONNECTIONS = 100
DEFAULT_TIMEOUT = 30

# Variables et fonctions : snake_case
ma_variable = 42


def ma_fonction():
    """Fonction en snake_case."""
    pass


# Classes : PascalCase
class MaClasse:
    """Classe en PascalCase."""

    def __init__(self):
        # Attributs "privés" : préfixe underscore
        self._attribut_interne = "interne"

        # Attributs "très privés" : double underscore (name mangling)
        self.__attribut_prive = "privé"

    def _methode_interne(self):
        """Méthode interne (convention, pas vraiment privée)."""
        pass


print(f"  Constante MAX_CONNECTIONS : {MAX_CONNECTIONS}")
print(f"  Variable ma_variable : {ma_variable}")
print(f"  Classe MaClasse : {MaClasse.__name__}")


# =============================================================================
# 5. PEP8 : Espaces et formatage
# =============================================================================

print("\n" + "=" * 60)
print("5. PEP8 : ESPACES ET FORMATAGE")
print("=" * 60)

# Espaces autour des opérateurs
x = 1 + 2
y = x * 3

# Pas d'espace avant les parenthèses d'appel
print(f"  x = {x}, y = {y}")

# Espaces après les virgules
liste = [1, 2, 3]
dico = {"a": 1, "b": 2}

# Pas d'espace à l'intérieur des parenthèses/crochets
# liste = [ 1, 2, 3 ]  # Mauvais
# fonction( argument )  # Mauvais

print(f"  Liste : {liste}")
print(f"  Dict : {dico}")

# Deux lignes vides entre les fonctions de niveau module
# (non démontré ici pour la compacité)


# =============================================================================
# 6. Comparaison : code mal formaté vs bien formaté
# =============================================================================

print("\n" + "=" * 60)
print("6. COMPARAISON : MAL VS BIEN FORMATÉ")
print("=" * 60)

print("""
AVANT (mal formaté) :
─────────────────────
def fonction( a,b,c ):
    return {'resultat':a+b+c,'status':"ok",'data':[1,2,3,4,5]}

x=1+2+3+4+5+6+7+8+9+10+11+12+13+14+15

liste = [1,2,3,
4,5,6]

APRÈS (Black) :
───────────────
def fonction(a, b, c):
    return {
        "resultat": a + b + c,
        "status": "ok",
        "data": [1, 2, 3, 4, 5],
    }


x = (
    1 + 2 + 3 + 4 + 5
    + 6 + 7 + 8 + 9 + 10
    + 11 + 12 + 13 + 14 + 15
)

liste = [1, 2, 3, 4, 5, 6]
""")


# =============================================================================
# 7. Exemple : code Pythonique vs non-Pythonique
# =============================================================================

print("\n" + "=" * 60)
print("7. CODE PYTHONIQUE VS NON-PYTHONIQUE")
print("=" * 60)

# Comparaison de nombres
numbers = [1, 2, 3, 4, 5]

# Non-Pythonique (style C/Java)
result_non_pythonic = []
for i in range(len(numbers)):
    if numbers[i] % 2 == 0:
        result_non_pythonic.append(numbers[i] ** 2)

# Pythonique (list comprehension)
result_pythonic = [n ** 2 for n in numbers if n % 2 == 0]

print(f"  Non-Pythonique : {result_non_pythonic}")
print(f"  Pythonique     : {result_pythonic}")

# Vérification de présence
# Non-Pythonique
found = False
for n in numbers:
    if n == 3:
        found = True
        break

# Pythonique
found_pythonic = 3 in numbers

print(f"  found (loop)   : {found}")
print(f"  found (in)     : {found_pythonic}")

# Échange de variables
a, b = 1, 2
# Non-Pythonique : temp = a; a = b; b = temp
# Pythonique :
a, b = b, a
print(f"  Échange : a={a}, b={b}")


# =============================================================================
# 8. Docstrings (PEP257)
# =============================================================================

print("\n" + "=" * 60)
print("8. DOCSTRINGS (PEP257)")
print("=" * 60)


def calculer_moyenne(nombres: List[float]) -> float:
    """
    Calcule la moyenne d'une liste de nombres.

    Args:
        nombres: Liste de nombres à moyenner.

    Returns:
        La moyenne arithmétique des nombres.

    Raises:
        ValueError: Si la liste est vide.

    Examples:
        >>> calculer_moyenne([1, 2, 3])
        2.0
        >>> calculer_moyenne([10, 20])
        15.0
    """
    if not nombres:
        raise ValueError("La liste ne peut pas être vide")
    return sum(nombres) / len(nombres)


print(f"  Docstring de calculer_moyenne :")
print(f"  {calculer_moyenne.__doc__[:100]}...")
print(f"  Résultat : {calculer_moyenne([1, 2, 3, 4, 5])}")


# =============================================================================
# 9. Résumé des outils de formatage
# =============================================================================

print("\n" + "=" * 60)
print("9. RÉSUMÉ DES OUTILS DE FORMATAGE")
print("=" * 60)

print("""
Outils recommandés :

| Outil   | Rôle                          | Commande              |
|---------|-------------------------------|-----------------------|
| black   | Formatage automatique         | black fichier.py      |
| isort   | Tri des imports               | isort fichier.py      |
| ruff    | Linter + formatter (tout-en-un)| ruff check --fix .   |

Configuration dans pyproject.toml :

[tool.black]
line-length = 88

[tool.isort]
profile = "black"

[tool.ruff]
line-length = 88
select = ["E", "F", "I", "N", "W", "UP"]
""")

print("\n--- Fin des exemples de conventions de style ---")
