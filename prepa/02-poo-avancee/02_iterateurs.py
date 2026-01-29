"""
Itérateurs et protocole d'itération
===================================

Implémentation du protocole d'itération avec __iter__ et __next__.
"""

# =============================================================================
# 1. Le protocole d'itération
# =============================================================================

print("=" * 60)
print("1. LE PROTOCOLE D'ITÉRATION")
print("=" * 60)


class Compteur:
    """Itérateur personnalisé."""

    def __init__(self, debut, fin):
        self.debut = debut
        self.fin = fin
        self.courant = debut

    def __iter__(self):
        """Retourne l'itérateur (lui-même)."""
        return self

    def __next__(self):
        """Retourne le prochain élément."""
        if self.courant >= self.fin:
            raise StopIteration
        valeur = self.courant
        self.courant += 1
        return valeur


print("Compteur(1, 5) :")
for n in Compteur(1, 5):
    print(f"  {n}")


# =============================================================================
# 2. Itérable vs Itérateur
# =============================================================================

print("\n" + "=" * 60)
print("2. ITÉRABLE VS ITÉRATEUR")
print("=" * 60)


class MonIterable:
    """
    Un itérable peut créer plusieurs itérateurs indépendants.
    """

    def __init__(self, data):
        self.data = data

    def __iter__(self):
        # Retourne un nouvel itérateur à chaque fois
        return iter(self.data)


class MonIterateur:
    """
    Un itérateur maintient un état et est consommé après parcours.
    """

    def __init__(self, data):
        self.data = data
        self.index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.index >= len(self.data):
            raise StopIteration
        valeur = self.data[self.index]
        self.index += 1
        return valeur


# Démonstration : itérable permet plusieurs parcours
print("--- Itérable (plusieurs parcours possibles) ---")
iterable = MonIterable([1, 2, 3])

print("Premier parcours :", list(iterable))
print("Deuxième parcours :", list(iterable))

# Démonstration : itérateur est consommé
print("\n--- Itérateur (un seul parcours) ---")
iterateur = MonIterateur([1, 2, 3])

print("Premier parcours :", list(iterateur))
print("Deuxième parcours :", list(iterateur))  # Vide !


# =============================================================================
# 3. Exemple : itérateur de plage inverse
# =============================================================================

print("\n" + "=" * 60)
print("3. ITÉRATEUR DE PLAGE INVERSE")
print("=" * 60)


class PlageInverse:
    """Itère sur une plage de nombres en ordre inverse."""

    def __init__(self, debut, fin):
        self.debut = debut
        self.fin = fin

    def __iter__(self):
        """Retourne un nouvel itérateur."""
        return PlageInverseIterator(self.debut, self.fin)


class PlageInverseIterator:
    """L'itérateur pour PlageInverse."""

    def __init__(self, debut, fin):
        self.courant = fin - 1
        self.debut = debut

    def __iter__(self):
        return self

    def __next__(self):
        if self.courant < self.debut:
            raise StopIteration
        valeur = self.courant
        self.courant -= 1
        return valeur


plage = PlageInverse(1, 6)
print("PlageInverse(1, 6) :")
print(f"  Premier parcours : {list(plage)}")
print(f"  Deuxième parcours : {list(plage)}")


# =============================================================================
# 4. Exemple : itérateur infini
# =============================================================================

print("\n" + "=" * 60)
print("4. ITÉRATEUR INFINI")
print("=" * 60)


class CycleInfini:
    """Répète indéfiniment les éléments d'une séquence."""

    def __init__(self, sequence):
        self.sequence = list(sequence)

    def __iter__(self):
        return CycleIterator(self.sequence)


class CycleIterator:
    def __init__(self, sequence):
        self.sequence = sequence
        self.index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if not self.sequence:
            raise StopIteration
        valeur = self.sequence[self.index]
        self.index = (self.index + 1) % len(self.sequence)
        return valeur


# Prendre les 10 premiers éléments d'un cycle infini
cycle = CycleInfini(["A", "B", "C"])
resultat = []
iterateur = iter(cycle)
for _ in range(10):
    resultat.append(next(iterateur))

print(f"Cycle infini (10 premiers) : {resultat}")


# =============================================================================
# 5. Itérateur avec filtrage
# =============================================================================

print("\n" + "=" * 60)
print("5. ITÉRATEUR AVEC FILTRAGE")
print("=" * 60)


class FiltreIterateur:
    """Itère sur les éléments qui satisfont une condition."""

    def __init__(self, iterable, condition):
        self.iterable = iter(iterable)
        self.condition = condition

    def __iter__(self):
        return self

    def __next__(self):
        while True:
            element = next(self.iterable)  # Propage StopIteration
            if self.condition(element):
                return element


nombres = range(1, 20)
pairs = FiltreIterateur(nombres, lambda x: x % 2 == 0)
print(f"Nombres pairs de 1 à 19 : {list(pairs)}")

mots = ["Python", "est", "un", "langage", "puissant"]
longs = FiltreIterateur(mots, lambda x: len(x) > 3)
print(f"Mots de plus de 3 lettres : {list(longs)}")


# =============================================================================
# 6. Itérateur de transformation (map-like)
# =============================================================================

print("\n" + "=" * 60)
print("6. ITÉRATEUR DE TRANSFORMATION")
print("=" * 60)


class TransformIterateur:
    """Applique une transformation à chaque élément."""

    def __init__(self, iterable, transform):
        self.iterable = iter(iterable)
        self.transform = transform

    def __iter__(self):
        return self

    def __next__(self):
        element = next(self.iterable)
        return self.transform(element)


nombres = [1, 2, 3, 4, 5]
carres = TransformIterateur(nombres, lambda x: x ** 2)
print(f"Carrés de {nombres} : {list(carres)}")

mots = ["hello", "world"]
majuscules = TransformIterateur(mots, str.upper)
print(f"En majuscules : {list(majuscules)}")


# =============================================================================
# 7. Exemple pratique : pagination de résultats
# =============================================================================

print("\n" + "=" * 60)
print("7. PAGINATION DE RÉSULTATS")
print("=" * 60)


class Paginateur:
    """Itère sur des données par pages."""

    def __init__(self, donnees, taille_page=3):
        self.donnees = donnees
        self.taille_page = taille_page

    def __iter__(self):
        return PaginateurIterator(self.donnees, self.taille_page)

    def __len__(self):
        """Nombre total de pages."""
        import math
        return math.ceil(len(self.donnees) / self.taille_page)


class PaginateurIterator:
    def __init__(self, donnees, taille_page):
        self.donnees = donnees
        self.taille_page = taille_page
        self.page_courante = 0

    def __iter__(self):
        return self

    def __next__(self):
        debut = self.page_courante * self.taille_page
        if debut >= len(self.donnees):
            raise StopIteration

        fin = debut + self.taille_page
        page = self.donnees[debut:fin]
        self.page_courante += 1
        return page


# Simuler des résultats de base de données
resultats = list(range(1, 12))  # [1, 2, ..., 11]
pages = Paginateur(resultats, taille_page=3)

print(f"Données : {resultats}")
print(f"Nombre de pages : {len(pages)}")
print("\nParcours des pages :")
for i, page in enumerate(pages, 1):
    print(f"  Page {i} : {page}")
