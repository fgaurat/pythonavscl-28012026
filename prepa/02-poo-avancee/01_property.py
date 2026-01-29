"""
Propriétés et @property
=======================

Utilisation de @property pour créer des attributs avec getter, setter et deleter.
"""

import math

# =============================================================================
# 1. Le problème des attributs publics
# =============================================================================

print("=" * 60)
print("1. LE PROBLÈME DES ATTRIBUTS PUBLICS")
print("=" * 60)


class CercleSansValidation:
    def __init__(self, rayon):
        self.rayon = rayon  # Attribut public direct


cercle = CercleSansValidation(5)
cercle.rayon = -10  # Aucune validation !
print(f"Rayon négatif accepté : {cercle.rayon}")  # -10


# =============================================================================
# 2. La solution avec @property
# =============================================================================

print("\n" + "=" * 60)
print("2. LA SOLUTION AVEC @property")
print("=" * 60)


class Cercle:
    def __init__(self, rayon):
        self._rayon = None
        self.rayon = rayon  # Utilise le setter

    @property
    def rayon(self):
        """Getter : accès à l'attribut."""
        return self._rayon

    @rayon.setter
    def rayon(self, valeur):
        """Setter : modification avec validation."""
        if valeur < 0:
            raise ValueError("Le rayon doit être positif")
        self._rayon = valeur


cercle = Cercle(5)
print(f"Rayon initial : {cercle.rayon}")

cercle.rayon = 10
print(f"Rayon après modification : {cercle.rayon}")

try:
    cercle.rayon = -1
except ValueError as e:
    print(f"Tentative de rayon négatif : {e}")


# =============================================================================
# 3. Propriétés calculées (lecture seule)
# =============================================================================

print("\n" + "=" * 60)
print("3. PROPRIÉTÉS CALCULÉES (LECTURE SEULE)")
print("=" * 60)


class CercleComplet:
    def __init__(self, rayon):
        self._rayon = rayon

    @property
    def rayon(self):
        return self._rayon

    @rayon.setter
    def rayon(self, valeur):
        if valeur < 0:
            raise ValueError("Le rayon doit être positif")
        self._rayon = valeur

    @property
    def aire(self):
        """Propriété calculée, lecture seule."""
        return math.pi * self._rayon ** 2

    @property
    def perimetre(self):
        """Propriété calculée, lecture seule."""
        return 2 * math.pi * self._rayon

    @property
    def diametre(self):
        """Propriété calculée avec setter."""
        return self._rayon * 2

    @diametre.setter
    def diametre(self, valeur):
        self.rayon = valeur / 2


cercle = CercleComplet(5)
print(f"Rayon : {cercle.rayon}")
print(f"Diamètre : {cercle.diametre}")
print(f"Aire : {cercle.aire:.2f}")
print(f"Périmètre : {cercle.perimetre:.2f}")

# Modifier via le diamètre
cercle.diametre = 20
print(f"\nAprès cercle.diametre = 20 :")
print(f"  Rayon : {cercle.rayon}")
print(f"  Diamètre : {cercle.diametre}")

# Tentative de modification d'une propriété en lecture seule
try:
    cercle.aire = 100
except AttributeError as e:
    print(f"\nTentative de modifier l'aire : AttributeError")


# =============================================================================
# 4. Propriété avec deleter
# =============================================================================

print("\n" + "=" * 60)
print("4. PROPRIÉTÉ AVEC DELETER")
print("=" * 60)


class Utilisateur:
    def __init__(self, email):
        self._email = email

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, valeur):
        if "@" not in valeur:
            raise ValueError("Email invalide")
        self._email = valeur

    @email.deleter
    def email(self):
        print("  Suppression de l'email...")
        self._email = None


user = Utilisateur("alice@example.com")
print(f"Email : {user.email}")

del user.email
print(f"Email après suppression : {user.email}")


# =============================================================================
# 5. Propriété avec cache manuel (lazy evaluation)
# =============================================================================

print("\n" + "=" * 60)
print("5. PROPRIÉTÉ AVEC CACHE MANUEL")
print("=" * 60)


class Document:
    def __init__(self, contenu):
        self._contenu = contenu
        self._statistiques = None  # Cache

    @property
    def contenu(self):
        return self._contenu

    @contenu.setter
    def contenu(self, valeur):
        self._contenu = valeur
        self._statistiques = None  # Invalide le cache

    @property
    def statistiques(self):
        """Calcul coûteux mis en cache."""
        if self._statistiques is None:
            print("  Calcul des statistiques...")
            self._statistiques = {
                "mots": len(self._contenu.split()),
                "caracteres": len(self._contenu),
                "lignes": self._contenu.count("\n") + 1
            }
        return self._statistiques


doc = Document("Hello World\nPython est génial\nTroisième ligne")

print("Premier accès aux statistiques :")
print(f"  {doc.statistiques}")

print("\nDeuxième accès (cache) :")
print(f"  {doc.statistiques}")

print("\nModification du contenu :")
doc.contenu = "Nouveau contenu"

print("\nAccès après modification (recalcul) :")
print(f"  {doc.statistiques}")


# =============================================================================
# 6. @cached_property (Python 3.8+)
# =============================================================================

print("\n" + "=" * 60)
print("6. @cached_property (PYTHON 3.8+)")
print("=" * 60)

from functools import cached_property
import time


class AnalyseurDonnees:
    def __init__(self, donnees):
        self.donnees = donnees

    @cached_property
    def analyse_complete(self):
        """Analyse coûteuse calculée une seule fois."""
        print("  Analyse en cours...")
        time.sleep(0.5)  # Simulation calcul long
        return {
            "moyenne": sum(self.donnees) / len(self.donnees),
            "total": sum(self.donnees),
            "min": min(self.donnees),
            "max": max(self.donnees),
            "count": len(self.donnees)
        }


analyseur = AnalyseurDonnees([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])

print("Premier accès :")
debut = time.perf_counter()
print(f"  {analyseur.analyse_complete}")
print(f"  Temps : {time.perf_counter() - debut:.2f}s")

print("\nDeuxième accès (cache) :")
debut = time.perf_counter()
print(f"  {analyseur.analyse_complete}")
print(f"  Temps : {time.perf_counter() - debut:.4f}s")

# Pour invalider le cache
print("\nInvalidation du cache :")
del analyseur.__dict__["analyse_complete"]

print("\nTroisième accès (recalcul) :")
debut = time.perf_counter()
print(f"  {analyseur.analyse_complete}")
print(f"  Temps : {time.perf_counter() - debut:.2f}s")


# =============================================================================
# 7. Exemple pratique : classe Température
# =============================================================================

print("\n" + "=" * 60)
print("7. EXEMPLE PRATIQUE : CLASSE TEMPÉRATURE")
print("=" * 60)


class Temperature:
    """Classe avec conversion automatique entre Celsius et Fahrenheit."""

    def __init__(self, celsius=0):
        self._celsius = celsius

    @property
    def celsius(self):
        return self._celsius

    @celsius.setter
    def celsius(self, valeur):
        if valeur < -273.15:
            raise ValueError("Température impossible (< zéro absolu)")
        self._celsius = valeur

    @property
    def fahrenheit(self):
        return self._celsius * 9/5 + 32

    @fahrenheit.setter
    def fahrenheit(self, valeur):
        self.celsius = (valeur - 32) * 5/9

    @property
    def kelvin(self):
        return self._celsius + 273.15

    @kelvin.setter
    def kelvin(self, valeur):
        self.celsius = valeur - 273.15

    def __repr__(self):
        return f"Temperature({self._celsius}°C)"


temp = Temperature(25)
print(f"Température : {temp}")
print(f"  Celsius : {temp.celsius}°C")
print(f"  Fahrenheit : {temp.fahrenheit}°F")
print(f"  Kelvin : {temp.kelvin}K")

print("\nModification via Fahrenheit (100°F) :")
temp.fahrenheit = 100
print(f"  {temp}")
print(f"  Celsius : {temp.celsius:.2f}°C")

print("\nModification via Kelvin (300K) :")
temp.kelvin = 300
print(f"  {temp}")
print(f"  Celsius : {temp.celsius:.2f}°C")
