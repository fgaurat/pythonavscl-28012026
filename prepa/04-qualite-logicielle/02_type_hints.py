"""
Type Hints (PEP484, PEP526)
===========================

Annotations de type pour la documentation et les outils statiques.
"""

from typing import (
    List, Dict, Optional, Union, Callable, Tuple,
    TypeVar, Generic, Protocol, Any
)
from dataclasses import dataclass
import sys

# =============================================================================
# 1. Types de base
# =============================================================================

print("=" * 60)
print("1. TYPES DE BASE")
print("=" * 60)

# Variables avec annotations
nom: str = "Alice"
age: int = 30
actif: bool = True
solde: float = 1234.56

print(f"  nom: str = {nom}")
print(f"  age: int = {age}")
print(f"  actif: bool = {actif}")
print(f"  solde: float = {solde}")


# Fonctions avec annotations
def saluer(nom: str, fois: int = 1) -> str:
    """Salue une personne plusieurs fois."""
    return f"Bonjour, {nom}! " * fois


resultat = saluer("Alice", 2)
print(f"\n  saluer('Alice', 2) = {resultat}")


# =============================================================================
# 2. Collections
# =============================================================================

print("\n" + "=" * 60)
print("2. COLLECTIONS")
print("=" * 60)

# Listes typées
nombres: List[int] = [1, 2, 3, 4, 5]
noms: List[str] = ["Alice", "Bob", "Charlie"]

# Dictionnaires typés
config: Dict[str, str] = {"host": "localhost", "port": "8080"}
scores: Dict[str, int] = {"Alice": 100, "Bob": 85}

# Tuples
point: Tuple[float, float] = (3.14, 2.71)
record: Tuple[str, int, bool] = ("Alice", 30, True)

print(f"  nombres: List[int] = {nombres}")
print(f"  config: Dict[str, str] = {config}")
print(f"  point: Tuple[float, float] = {point}")


# Python 3.9+ : utilisation directe des types built-in
# (pas besoin d'importer List, Dict de typing)
if sys.version_info >= (3, 9):
    nombres_new: list[int] = [1, 2, 3]
    config_new: dict[str, str] = {"key": "value"}
    print(f"\n  Python 3.9+ syntax: list[int] = {nombres_new}")


# =============================================================================
# 3. Optional et Union
# =============================================================================

print("\n" + "=" * 60)
print("3. OPTIONAL ET UNION")
print("=" * 60)


# Optional : peut être None
def trouver_utilisateur(user_id: int) -> Optional[str]:
    """Retourne le nom de l'utilisateur ou None si non trouvé."""
    users = {1: "Alice", 2: "Bob"}
    return users.get(user_id)


user1 = trouver_utilisateur(1)
user99 = trouver_utilisateur(99)
print(f"  trouver_utilisateur(1) = {user1}")
print(f"  trouver_utilisateur(99) = {user99}")


# Union : plusieurs types possibles
def formater_valeur(valeur: Union[int, str, float]) -> str:
    """Formate une valeur en string."""
    if isinstance(valeur, float):
        return f"{valeur:.2f}"
    return str(valeur)


print(f"\n  formater_valeur(42) = {formater_valeur(42)}")
print(f"  formater_valeur(3.14159) = {formater_valeur(3.14159)}")
print(f"  formater_valeur('hello') = {formater_valeur('hello')}")


# Python 3.10+ : syntaxe simplifiée avec |
if sys.version_info >= (3, 10):
    def process(value: int | str | None) -> str:
        """Syntaxe Python 3.10+ avec |."""
        return str(value) if value else "N/A"

    print(f"\n  Python 3.10+ : int | str | None")


# =============================================================================
# 4. Callable
# =============================================================================

print("\n" + "=" * 60)
print("4. CALLABLE")
print("=" * 60)


# Type pour les fonctions
def appliquer_operation(
    nombres: List[int],
    operation: Callable[[int], int]
) -> List[int]:
    """Applique une opération à chaque élément."""
    return [operation(n) for n in nombres]


def doubler(x: int) -> int:
    return x * 2


def carrer(x: int) -> int:
    return x ** 2


nombres = [1, 2, 3, 4, 5]
print(f"  nombres = {nombres}")
print(f"  appliquer_operation(nombres, doubler) = {appliquer_operation(nombres, doubler)}")
print(f"  appliquer_operation(nombres, carrer) = {appliquer_operation(nombres, carrer)}")


# Callable avec plusieurs arguments
Handler = Callable[[str, int], bool]


def traiter(data: str, count: int) -> bool:
    """Handler de type Callable[[str, int], bool]."""
    return len(data) > count


mon_handler: Handler = traiter
print(f"\n  mon_handler('hello', 3) = {mon_handler('hello', 3)}")


# =============================================================================
# 5. TypeVar et génériques
# =============================================================================

print("\n" + "=" * 60)
print("5. TYPEVAR ET GÉNÉRIQUES")
print("=" * 60)

# TypeVar pour les fonctions génériques
T = TypeVar("T")


def premier(items: List[T]) -> T:
    """Retourne le premier élément d'une liste."""
    return items[0]


print(f"  premier([1, 2, 3]) = {premier([1, 2, 3])}")
print(f"  premier(['a', 'b', 'c']) = {premier(['a', 'b', 'c'])}")


# TypeVar avec contraintes
Number = TypeVar("Number", int, float)


def additionner(a: Number, b: Number) -> Number:
    """Additionne deux nombres de même type."""
    return a + b


print(f"\n  additionner(1, 2) = {additionner(1, 2)}")
print(f"  additionner(1.5, 2.5) = {additionner(1.5, 2.5)}")


# Classe générique
ItemType = TypeVar("ItemType")


class Boite(Generic[ItemType]):
    """Boîte générique pouvant contenir n'importe quel type."""

    def __init__(self, contenu: ItemType):
        self.contenu = contenu

    def obtenir(self) -> ItemType:
        return self.contenu


boite_int: Boite[int] = Boite(42)
boite_str: Boite[str] = Boite("hello")

print(f"\n  Boite[int].obtenir() = {boite_int.obtenir()}")
print(f"  Boite[str].obtenir() = {boite_str.obtenir()}")


# =============================================================================
# 6. Protocol (structural typing)
# =============================================================================

print("\n" + "=" * 60)
print("6. PROTOCOL (STRUCTURAL TYPING)")
print("=" * 60)


class Readable(Protocol):
    """Protocol pour les objets lisibles."""

    def read(self) -> str:
        ...


class FichierTexte:
    """Implémente implicitement Readable."""

    def __init__(self, contenu: str):
        self._contenu = contenu

    def read(self) -> str:
        return self._contenu


class APIClient:
    """Implémente aussi Readable (sans héritage explicite)."""

    def __init__(self, data: str):
        self._data = data

    def read(self) -> str:
        return f"API: {self._data}"


def afficher_contenu(source: Readable) -> None:
    """Accepte tout objet avec une méthode read()."""
    print(f"  Contenu : {source.read()}")


fichier = FichierTexte("Hello from file")
api = APIClient("Hello from API")

print("  Avec FichierTexte :")
afficher_contenu(fichier)
print("  Avec APIClient :")
afficher_contenu(api)


# =============================================================================
# 7. Type aliases
# =============================================================================

print("\n" + "=" * 60)
print("7. TYPE ALIASES")
print("=" * 60)

# Aliases pour types complexes
UserId = int
UserName = str
UserMap = Dict[UserId, UserName]
Coordinates = Tuple[float, float]


def get_user(users: UserMap, user_id: UserId) -> Optional[UserName]:
    """Utilise des aliases pour plus de clarté."""
    return users.get(user_id)


users: UserMap = {1: "Alice", 2: "Bob", 3: "Charlie"}
print(f"  users: UserMap = {users}")
print(f"  get_user(users, 1) = {get_user(users, 1)}")


# Python 3.12+ : type statement
if sys.version_info >= (3, 12):
    # type Point = Tuple[float, float]
    # type Callback[T] = Callable[[T], None]
    print("\n  Python 3.12+ : type aliases avec 'type' statement")


# =============================================================================
# 8. Annotations avec dataclass
# =============================================================================

print("\n" + "=" * 60)
print("8. ANNOTATIONS AVEC DATACLASS")
print("=" * 60)


@dataclass
class Utilisateur:
    """Dataclass avec annotations de type."""
    id: int
    nom: str
    email: str
    age: Optional[int] = None
    tags: List[str] = None

    def __post_init__(self):
        if self.tags is None:
            self.tags = []


user = Utilisateur(
    id=1,
    nom="Alice",
    email="alice@example.com",
    age=30,
    tags=["admin", "vip"]
)

print(f"  {user}")
print(f"  Annotations : {Utilisateur.__annotations__}")


# =============================================================================
# 9. Mypy : vérification statique
# =============================================================================

print("\n" + "=" * 60)
print("9. MYPY : VÉRIFICATION STATIQUE")
print("=" * 60)

print("""
Mypy vérifie les types sans exécuter le code.

Installation :
  pip install mypy

Utilisation :
  mypy mon_fichier.py

Exemple d'erreur détectée :

  def addition(a: int, b: int) -> int:
      return a + b

  result = addition("1", "2")  # Erreur mypy !
  # error: Argument 1 has incompatible type "str"; expected "int"

Configuration (pyproject.toml) :

  [tool.mypy]
  python_version = "3.11"
  strict = true
  warn_return_any = true
  disallow_untyped_defs = true
""")


# =============================================================================
# 10. Bonnes pratiques
# =============================================================================

print("\n" + "=" * 60)
print("10. BONNES PRATIQUES")
print("=" * 60)

print("""
Conseils pour les type hints :

1. Annoter les signatures de fonction publiques
   def fetch_user(user_id: int) -> Optional[User]:

2. Utiliser Optional pour les valeurs qui peuvent être None
   def get_config(key: str) -> Optional[str]:

3. Préférer les types génériques (List, Dict) aux types concrets
   def process(items: List[T]) -> List[T]:  # Flexible
   def process(items: list) -> list:        # Moins précis

4. Utiliser des aliases pour les types complexes
   UserMap = Dict[int, User]
   Callback = Callable[[str], None]

5. Les annotations ne sont pas vérifiées à l'exécution
   → Utiliser mypy pour la vérification statique

6. Éviter Any sauf si vraiment nécessaire
   → Any désactive la vérification de type
""")

print("\n--- Fin des exemples de type hints ---")
