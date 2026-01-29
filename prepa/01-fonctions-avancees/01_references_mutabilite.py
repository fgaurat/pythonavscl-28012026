"""
Références et mutabilité en Python
==================================

Démonstration des concepts de références, mutabilité et pièges courants.
"""

# =============================================================================
# 1. Références - Tout est objet
# =============================================================================

print("=" * 60)
print("1. RÉFÉRENCES - TOUT EST OBJET")
print("=" * 60)

# Chaque variable est une référence vers un objet
x = [1, 2, 3]
y = x  # y pointe vers le MÊME objet que x

y.append(4)
print(f"x = {x}")  # [1, 2, 3, 4] - x est aussi modifié !
print(f"y = {y}")  # [1, 2, 3, 4]

# Vérification avec id()
print(f"id(x) == id(y) : {id(x) == id(y)}")  # True - même adresse mémoire


# =============================================================================
# 2. Types immutables vs mutables
# =============================================================================

print("\n" + "=" * 60)
print("2. TYPES IMMUTABLES VS MUTABLES")
print("=" * 60)

# --- Immutables (int, float, bool, str, tuple, frozenset) ---
print("\n--- Types immutables ---")

a = 5
b = a
a = a + 1
print(f"a = {a}, b = {b}")  # a = 6, b = 5 (b inchangé)
print(f"id(a) == id(b) : {id(a) == id(b)}")  # False - objets différents

s1 = "hello"
s2 = s1
s1 = s1 + " world"
print(f"s1 = '{s1}', s2 = '{s2}'")  # s2 inchangé

# --- Mutables (list, dict, set, instances de classes) ---
print("\n--- Types mutables ---")

lst = [1, 2]
ref = lst
lst.append(3)
print(f"lst = {lst}, ref = {ref}")  # Les deux sont modifiés
print(f"id(lst) == id(ref) : {id(lst) == id(ref)}")  # True


# =============================================================================
# 3. Piège classique : argument mutable par défaut
# =============================================================================

print("\n" + "=" * 60)
print("3. PIÈGE : ARGUMENT MUTABLE PAR DÉFAUT")
print("=" * 60)


# DANGER : la liste est partagée entre tous les appels
def ajouter_element_danger(element, liste=[]):
    liste.append(element)
    return liste


print("\n--- Version dangereuse ---")
print(f"Appel 1 : {ajouter_element_danger(1)}")  # [1]
print(f"Appel 2 : {ajouter_element_danger(2)}")  # [1, 2] - Surprise !
print(f"Appel 3 : {ajouter_element_danger(3)}")  # [1, 2, 3] - Continue !


# Solution : utiliser None comme valeur par défaut
def ajouter_element_safe(element, liste=None):
    if liste is None:
        liste = []
    liste.append(element)
    return liste


print("\n--- Version sûre ---")
print(f"Appel 1 : {ajouter_element_safe(1)}")  # [1]
print(f"Appel 2 : {ajouter_element_safe(2)}")  # [2]
print(f"Appel 3 : {ajouter_element_safe(3)}")  # [3]


# =============================================================================
# 4. Copie superficielle vs copie profonde
# =============================================================================

print("\n" + "=" * 60)
print("4. COPIE SUPERFICIELLE VS PROFONDE")
print("=" * 60)

import copy

# Liste imbriquée
original = [[1, 2], [3, 4]]

# Copie superficielle (shallow copy)
shallow = original.copy()  # ou list(original) ou original[:]
shallow[0].append(999)
print(f"Après shallow copy et modification :")
print(f"  original = {original}")  # [[1, 2, 999], [3, 4]] - modifié !
print(f"  shallow  = {shallow}")   # [[1, 2, 999], [3, 4]]

# Copie profonde (deep copy)
original2 = [[1, 2], [3, 4]]
deep = copy.deepcopy(original2)
deep[0].append(999)
print(f"\nAprès deep copy et modification :")
print(f"  original2 = {original2}")  # [[1, 2], [3, 4]] - inchangé !
print(f"  deep      = {deep}")       # [[1, 2, 999], [3, 4]]
