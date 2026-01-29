"""
Module itertools
================

Outils essentiels du module itertools pour manipuler les itérables.
"""

from itertools import (
    chain, islice, groupby, cycle, repeat, count,
    takewhile, dropwhile, filterfalse, accumulate,
    product, permutations, combinations, zip_longest
)

# =============================================================================
# 1. chain : concaténer des itérables
# =============================================================================

print("=" * 60)
print("1. CHAIN : CONCATÉNER DES ITÉRABLES")
print("=" * 60)

liste1 = [1, 2, 3]
liste2 = [4, 5]
liste3 = [6, 7, 8]

combined = chain(liste1, liste2, liste3)
print(f"chain({liste1}, {liste2}, {liste3}) = {list(combined)}")

# chain.from_iterable pour une liste de listes
listes = [[1, 2], [3, 4], [5, 6]]
aplati = chain.from_iterable(listes)
print(f"chain.from_iterable({listes}) = {list(aplati)}")


# =============================================================================
# 2. islice : découper un itérateur
# =============================================================================

print("\n" + "=" * 60)
print("2. ISLICE : DÉCOUPER UN ITÉRATEUR")
print("=" * 60)

# Prendre les n premiers
premiers_10 = list(islice(count(), 10))
print(f"islice(count(), 10) = {premiers_10}")

# Sauter et prendre
# islice(iterable, start, stop, step)
de_5_a_15_par_2 = list(islice(count(), 5, 15, 2))
print(f"islice(count(), 5, 15, 2) = {de_5_a_15_par_2}")

# Prendre les 5 premiers d'une liste
lettres = "ABCDEFGHIJ"
print(f"islice('{lettres}', 5) = {list(islice(lettres, 5))}")


# =============================================================================
# 3. groupby : grouper par clé
# =============================================================================

print("\n" + "=" * 60)
print("3. GROUPBY : GROUPER PAR CLÉ")
print("=" * 60)

# IMPORTANT : les données doivent être triées par la clé !
data = [
    ("fruit", "pomme"),
    ("fruit", "banane"),
    ("légume", "carotte"),
    ("légume", "poireau"),
    ("fruit", "orange"),  # Attention : nouveau groupe "fruit" !
]

print("Données non triées :")
for key, group in groupby(data, key=lambda x: x[0]):
    print(f"  {key}: {list(group)}")

# Avec données triées
data_sorted = sorted(data, key=lambda x: x[0])
print("\nDonnées triées :")
for key, group in groupby(data_sorted, key=lambda x: x[0]):
    print(f"  {key}: {[item[1] for item in group]}")

# Exemple : grouper des nombres par dizaine
nombres = [3, 5, 12, 15, 18, 23, 25, 31]
print(f"\nNombres : {nombres}")
print("Groupés par dizaine :")
for dizaine, group in groupby(sorted(nombres), key=lambda x: x // 10):
    print(f"  {dizaine}0s: {list(group)}")


# =============================================================================
# 4. cycle et repeat : répétition
# =============================================================================

print("\n" + "=" * 60)
print("4. CYCLE ET REPEAT : RÉPÉTITION")
print("=" * 60)

# cycle : répète indéfiniment
couleurs = cycle(["rouge", "vert", "bleu"])
print("cycle(['rouge', 'vert', 'bleu']) - 7 premiers :")
print(f"  {list(islice(couleurs, 7))}")

# repeat : répète un élément
print(f"\nrepeat('X', 5) = {list(repeat('X', 5))}")

# repeat infini (avec limit)
print(f"repeat(42) - 3 premiers = {list(islice(repeat(42), 3))}")


# =============================================================================
# 5. count : compteur infini
# =============================================================================

print("\n" + "=" * 60)
print("5. COUNT : COMPTEUR INFINI")
print("=" * 60)

# Compte à partir de 0
print(f"count() - 5 premiers = {list(islice(count(), 5))}")

# Compte à partir de 10
print(f"count(10) - 5 premiers = {list(islice(count(10), 5))}")

# Compte avec pas de 0.5
print(f"count(0, 0.5) - 6 premiers = {list(islice(count(0, 0.5), 6))}")


# =============================================================================
# 6. takewhile et dropwhile
# =============================================================================

print("\n" + "=" * 60)
print("6. TAKEWHILE ET DROPWHILE")
print("=" * 60)

nombres = [1, 3, 5, 7, 2, 4, 6, 8]
print(f"Nombres : {nombres}")

# takewhile : prend tant que la condition est vraie
impairs = list(takewhile(lambda x: x % 2 == 1, nombres))
print(f"takewhile(impair) = {impairs}")

# dropwhile : saute tant que la condition est vraie
apres_impairs = list(dropwhile(lambda x: x % 2 == 1, nombres))
print(f"dropwhile(impair) = {apres_impairs}")


# =============================================================================
# 7. filterfalse : inverse de filter
# =============================================================================

print("\n" + "=" * 60)
print("7. FILTERFALSE : INVERSE DE FILTER")
print("=" * 60)

nombres = range(10)

pairs = list(filter(lambda x: x % 2 == 0, nombres))
impairs = list(filterfalse(lambda x: x % 2 == 0, nombres))

print(f"filter(pair, range(10)) = {pairs}")
print(f"filterfalse(pair, range(10)) = {impairs}")


# =============================================================================
# 8. accumulate : sommes cumulées
# =============================================================================

print("\n" + "=" * 60)
print("8. ACCUMULATE : SOMMES CUMULÉES")
print("=" * 60)

nombres = [1, 2, 3, 4, 5]
print(f"Nombres : {nombres}")

# Somme cumulative (par défaut)
cumsum = list(accumulate(nombres))
print(f"accumulate (somme) = {cumsum}")

# Produit cumulatif
import operator

cumprod = list(accumulate(nombres, operator.mul))
print(f"accumulate (produit) = {cumprod}")

# Maximum cumulatif
data = [3, 1, 4, 1, 5, 9, 2, 6]
cummax = list(accumulate(data, max))
print(f"\nDonnées : {data}")
print(f"accumulate (max) = {cummax}")


# =============================================================================
# 9. product, permutations, combinations
# =============================================================================

print("\n" + "=" * 60)
print("9. PRODUCT, PERMUTATIONS, COMBINATIONS")
print("=" * 60)

# product : produit cartésien
print("product([1,2], ['a','b']) :")
print(f"  {list(product([1, 2], ['a', 'b']))}")

# Équivalent à des boucles imbriquées
print("\nproduct('AB', repeat=2) :")
print(f"  {list(product('AB', repeat=2))}")

# permutations : arrangements
print("\npermutations('ABC', 2) :")
print(f"  {list(permutations('ABC', 2))}")

# combinations : combinaisons (sans répétition, ordre non important)
print("\ncombinations('ABCD', 2) :")
print(f"  {list(combinations('ABCD', 2))}")


# =============================================================================
# 10. zip_longest : zip avec remplissage
# =============================================================================

print("\n" + "=" * 60)
print("10. ZIP_LONGEST")
print("=" * 60)

liste1 = [1, 2, 3, 4, 5]
liste2 = ['a', 'b', 'c']

print(f"Liste 1 : {liste1}")
print(f"Liste 2 : {liste2}")

# zip standard (s'arrête au plus court)
print(f"\nzip : {list(zip(liste1, liste2))}")

# zip_longest (remplit avec fillvalue)
print(f"zip_longest (fillvalue='-') : {list(zip_longest(liste1, liste2, fillvalue='-'))}")


# =============================================================================
# 11. Exemple pratique : pipeline de données
# =============================================================================

print("\n" + "=" * 60)
print("11. EXEMPLE PRATIQUE : PIPELINE DE DONNÉES")
print("=" * 60)

# Données brutes (simulées)
ventes = [
    {"produit": "A", "region": "Nord", "montant": 100},
    {"produit": "B", "region": "Sud", "montant": 150},
    {"produit": "A", "region": "Nord", "montant": 200},
    {"produit": "C", "region": "Sud", "montant": 75},
    {"produit": "B", "region": "Nord", "montant": 300},
    {"produit": "A", "region": "Sud", "montant": 125},
]

# Grouper par région et calculer le total
ventes_triees = sorted(ventes, key=lambda x: x["region"])

print("Ventes par région :")
for region, groupe in groupby(ventes_triees, key=lambda x: x["region"]):
    ventes_region = list(groupe)
    total = sum(v["montant"] for v in ventes_region)
    print(f"  {region}: {total}€ ({len(ventes_region)} ventes)")

# Top 3 des ventes
top3 = list(islice(sorted(ventes, key=lambda x: x["montant"], reverse=True), 3))
print(f"\nTop 3 des ventes :")
for v in top3:
    print(f"  {v['produit']} ({v['region']}): {v['montant']}€")
