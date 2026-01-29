"""
Générateurs
===========

Création de générateurs avec yield, expressions génératrices et yield from.
"""

import sys

# =============================================================================
# 1. Générateurs basiques
# =============================================================================

print("=" * 60)
print("1. GÉNÉRATEURS BASIQUES")
print("=" * 60)


def compteur(debut, fin):
    """Générateur équivalent à la classe Compteur."""
    courant = debut
    while courant < fin:
        yield courant
        courant += 1


print("compteur(1, 5) :")
for n in compteur(1, 5):
    print(f"  {n}")

# Le type est 'generator'
gen = compteur(1, 5)
print(f"\ntype(compteur(1, 5)) = {type(gen)}")


# =============================================================================
# 2. Évaluation paresseuse (lazy evaluation)
# =============================================================================

print("\n" + "=" * 60)
print("2. ÉVALUATION PARESSEUSE")
print("=" * 60)


# Version avec liste (tout en mémoire)
def carres_liste(n):
    resultat = []
    for i in range(n):
        resultat.append(i ** 2)
    return resultat


# Version avec générateur (un élément à la fois)
def carres_generateur(n):
    for i in range(n):
        yield i ** 2


# Comparaison mémoire
n = 1_000_000

liste = carres_liste(n)
print(f"Liste de {n} carrés : {sys.getsizeof(liste):,} octets")

gen = carres_generateur(n)
print(f"Générateur de {n} carrés : {sys.getsizeof(gen)} octets")


# =============================================================================
# 3. Expressions génératrices
# =============================================================================

print("\n" + "=" * 60)
print("3. EXPRESSIONS GÉNÉRATRICES")
print("=" * 60)

# List comprehension (crée une liste)
carres_liste = [x ** 2 for x in range(10)]
print(f"List comprehension : {carres_liste}")
print(f"  Type : {type(carres_liste)}")

# Generator expression (crée un générateur)
carres_gen = (x ** 2 for x in range(10))
print(f"\nGenerator expression : {carres_gen}")
print(f"  Type : {type(carres_gen)}")
print(f"  Converti en liste : {list(carres_gen)}")

# Utilisation directe dans les fonctions (économie de mémoire)
somme = sum(x ** 2 for x in range(1000))
print(f"\nSomme des carrés de 0 à 999 : {somme}")

# Avec filtrage
pairs_carres = sum(x ** 2 for x in range(100) if x % 2 == 0)
print(f"Somme des carrés des pairs de 0 à 99 : {pairs_carres}")


# =============================================================================
# 4. yield from : délégation de générateurs
# =============================================================================

print("\n" + "=" * 60)
print("4. YIELD FROM : DÉLÉGATION")
print("=" * 60)


# Sans yield from
def aplatir_v1(liste_imbriquee):
    for sous_liste in liste_imbriquee:
        for element in sous_liste:
            yield element


# Avec yield from (plus élégant)
def aplatir_v2(liste_imbriquee):
    for sous_liste in liste_imbriquee:
        yield from sous_liste


donnees = [[1, 2, 3], [4, 5], [6, 7, 8, 9]]
print(f"Données imbriquées : {donnees}")
print(f"Aplatissement v1 : {list(aplatir_v1(donnees))}")
print(f"Aplatissement v2 : {list(aplatir_v2(donnees))}")


# Récursif avec yield from
def aplatir_recursif(structure):
    """Aplatit une structure imbriquée de profondeur quelconque."""
    for element in structure:
        if isinstance(element, (list, tuple)):
            yield from aplatir_recursif(element)
        else:
            yield element


structure_complexe = [1, [2, [3, 4]], 5, [[6, 7], 8, [9, [10]]]]
print(f"\nStructure complexe : {structure_complexe}")
print(f"Aplatie : {list(aplatir_recursif(structure_complexe))}")


# =============================================================================
# 5. Générateurs bidirectionnels : send()
# =============================================================================

print("\n" + "=" * 60)
print("5. GÉNÉRATEURS BIDIRECTIONNELS : send()")
print("=" * 60)


def accumulateur():
    """Générateur qui accumule les valeurs reçues."""
    total = 0
    while True:
        valeur = yield total  # Reçoit et retourne
        if valeur is None:
            break
        total += valeur


gen = accumulateur()
next(gen)  # Initialisation (premier yield)

print("Accumulateur avec send() :")
print(f"  send(10) -> {gen.send(10)}")
print(f"  send(5)  -> {gen.send(5)}")
print(f"  send(20) -> {gen.send(20)}")
print(f"  send(15) -> {gen.send(15)}")

try:
    gen.send(None)  # Termine le générateur
except StopIteration:
    print("  Générateur terminé")


# =============================================================================
# 6. Générateur avec état
# =============================================================================

print("\n" + "=" * 60)
print("6. GÉNÉRATEUR AVEC ÉTAT")
print("=" * 60)


def moyenne_mobile(taille_fenetre):
    """Calcule une moyenne mobile sur les valeurs reçues."""
    fenetre = []
    moyenne = None

    while True:
        valeur = yield moyenne
        if valeur is None:
            break

        fenetre.append(valeur)
        if len(fenetre) > taille_fenetre:
            fenetre.pop(0)

        moyenne = sum(fenetre) / len(fenetre)


gen = moyenne_mobile(3)
next(gen)  # Initialisation

valeurs = [10, 20, 30, 40, 50, 60]
print(f"Valeurs : {valeurs}")
print(f"Moyenne mobile (fenêtre=3) :")
for v in valeurs:
    result = gen.send(v)
    print(f"  Après {v:2d} : moyenne = {result:.2f}")


# =============================================================================
# 7. Cas d'usage : lecture de fichiers volumineux
# =============================================================================

print("\n" + "=" * 60)
print("7. CAS D'USAGE : TRAITEMENT DE FICHIERS")
print("=" * 60)


def lire_par_blocs(contenu, taille_bloc=50):
    """Simule la lecture par blocs (pour fichiers volumineux)."""
    position = 0
    while position < len(contenu):
        yield contenu[position:position + taille_bloc]
        position += taille_bloc


def rechercher_pattern(lignes, pattern):
    """Générateur qui yield les lignes contenant le pattern."""
    for numero, ligne in enumerate(lignes, 1):
        if pattern in ligne:
            yield numero, ligne


# Simulation avec du texte
texte = """Ligne 1 : Python est génial
Ligne 2 : Java est aussi utilisé
Ligne 3 : Python pour le data science
Ligne 4 : JavaScript pour le web
Ligne 5 : Python pour l'IA"""

print("Recherche de 'Python' dans le texte :")
lignes = texte.split("\n")
for numero, ligne in rechercher_pattern(lignes, "Python"):
    print(f"  Ligne {numero} : {ligne}")


# Pipeline de générateurs
def lignes_fichier(texte):
    """Générateur de lignes."""
    yield from texte.split("\n")


def filtrer_vides(lignes):
    """Filtre les lignes vides."""
    for ligne in lignes:
        if ligne.strip():
            yield ligne


def majuscules(lignes):
    """Transforme en majuscules."""
    for ligne in lignes:
        yield ligne.upper()


# Chaînage de générateurs (pipeline)
print("\nPipeline : lignes -> filtrer vides -> majuscules")
texte2 = "hello\n\nworld\n\npython"
pipeline = majuscules(filtrer_vides(lignes_fichier(texte2)))
for ligne in pipeline:
    print(f"  {ligne}")


# =============================================================================
# 8. Générateurs infinis
# =============================================================================

print("\n" + "=" * 60)
print("8. GÉNÉRATEURS INFINIS")
print("=" * 60)


def nombres_naturels():
    """Génère les nombres naturels à l'infini."""
    n = 0
    while True:
        yield n
        n += 1


def prendre(iterable, n):
    """Prend les n premiers éléments d'un itérable."""
    for i, element in enumerate(iterable):
        if i >= n:
            break
        yield element


print("10 premiers nombres naturels :", list(prendre(nombres_naturels(), 10)))


def fibonacci():
    """Génère la suite de Fibonacci à l'infini."""
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b


print("15 premiers Fibonacci :", list(prendre(fibonacci(), 15)))


def premiers():
    """Génère les nombres premiers à l'infini (crible)."""

    def est_premier(n, premiers_connus):
        for p in premiers_connus:
            if p * p > n:
                break
            if n % p == 0:
                return False
        return True

    yield 2
    premiers_connus = [2]
    candidat = 3

    while True:
        if est_premier(candidat, premiers_connus):
            premiers_connus.append(candidat)
            yield candidat
        candidat += 2


print("20 premiers nombres premiers :", list(prendre(premiers(), 20)))
