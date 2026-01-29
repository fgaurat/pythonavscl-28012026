"""
Patterns Pythoniques
====================

Duck typing, EAFP vs LBYL, et Protocoles typing.
"""

from typing import Protocol, runtime_checkable, List, Any

# =============================================================================
# 1. Duck Typing
# =============================================================================

print("=" * 60)
print("1. DUCK TYPING")
print("=" * 60)

print('"If it walks like a duck and quacks like a duck..."')


class Canard:
    def nager(self):
        return "Le canard nage"

    def voler(self):
        return "Le canard vole"


class Bateau:
    def nager(self):
        return "Le bateau flotte"


class Avion:
    def voler(self):
        return "L'avion vole"


class Pierre:
    pass


def aller_sur_eau(obj):
    """Fonctionne avec tout objet ayant une méthode nager()."""
    return obj.nager()


def aller_dans_les_airs(obj):
    """Fonctionne avec tout objet ayant une méthode voler()."""
    return obj.voler()


print("\nDuck typing en action :")
print(f"  Canard sur l'eau : {aller_sur_eau(Canard())}")
print(f"  Bateau sur l'eau : {aller_sur_eau(Bateau())}")
print(f"  Canard dans les airs : {aller_dans_les_airs(Canard())}")
print(f"  Avion dans les airs : {aller_dans_les_airs(Avion())}")

try:
    aller_sur_eau(Pierre())
except AttributeError as e:
    print(f"  Pierre sur l'eau : AttributeError (n'a pas nager())")


# =============================================================================
# 2. EAFP vs LBYL
# =============================================================================

print("\n" + "=" * 60)
print("2. EAFP VS LBYL")
print("=" * 60)


# LBYL : Look Before You Leap
def get_value_lbyl(data: dict, key: str, default=None):
    """Style LBYL : vérifier avant d'agir."""
    if key in data:
        return data[key]
    else:
        return default


# EAFP : Easier to Ask Forgiveness than Permission
def get_value_eafp(data: dict, key: str, default=None):
    """Style EAFP : essayer et gérer l'erreur."""
    try:
        return data[key]
    except KeyError:
        return default


data = {"name": "Alice", "age": 30}

print("Comparaison LBYL vs EAFP :")
print(f"  LBYL - name: {get_value_lbyl(data, 'name')}")
print(f"  EAFP - name: {get_value_eafp(data, 'name')}")
print(f"  LBYL - email: {get_value_lbyl(data, 'email', 'N/A')}")
print(f"  EAFP - email: {get_value_eafp(data, 'email', 'N/A')}")


# Exemple avec fichiers
def read_file_lbyl(path: str) -> str:
    """LBYL : vérifie l'existence avant d'ouvrir."""
    import os
    if os.path.exists(path):
        with open(path, "r") as f:
            return f.read()
    return ""


def read_file_eafp(path: str) -> str:
    """EAFP : essaie d'ouvrir et gère l'erreur."""
    try:
        with open(path, "r") as f:
            return f.read()
    except FileNotFoundError:
        return ""


print("\nLecture de fichier :")
print(f"  LBYL - fichier inexistant: '{read_file_lbyl('/tmp/inexistant.txt')}'")
print(f"  EAFP - fichier inexistant: '{read_file_eafp('/tmp/inexistant.txt')}'")


# Exemple avec conversion
def parse_int_lbyl(value: str) -> int:
    """LBYL : vérifie si c'est un nombre."""
    if value.isdigit():
        return int(value)
    return 0


def parse_int_eafp(value: str) -> int:
    """EAFP : essaie de convertir."""
    try:
        return int(value)
    except ValueError:
        return 0


print("\nConversion en entier :")
print(f"  LBYL '42': {parse_int_lbyl('42')}")
print(f"  EAFP '42': {parse_int_eafp('42')}")
print(f"  LBYL 'abc': {parse_int_lbyl('abc')}")
print(f"  EAFP 'abc': {parse_int_eafp('abc')}")
print(f"  LBYL '-5': {parse_int_lbyl('-5')}")  # Problème : isdigit() échoue sur négatifs !
print(f"  EAFP '-5': {parse_int_eafp('-5')}")  # Fonctionne !

print("\n→ Python favorise EAFP : plus performant et évite les race conditions")


# =============================================================================
# 3. Protocoles typing (Python 3.8+)
# =============================================================================

print("\n" + "=" * 60)
print("3. PROTOCOLES TYPING")
print("=" * 60)


@runtime_checkable
class Drawable(Protocol):
    """Protocole définissant l'interface d'un objet dessinable."""

    def draw(self) -> str:
        ...


@runtime_checkable
class Resizable(Protocol):
    """Protocole pour les objets redimensionnables."""

    def resize(self, factor: float) -> None:
        ...


class Circle:
    def __init__(self, radius: float):
        self.radius = radius

    def draw(self) -> str:
        return f"Drawing circle with radius {self.radius}"

    def resize(self, factor: float) -> None:
        self.radius *= factor


class Square:
    def __init__(self, side: float):
        self.side = side

    def draw(self) -> str:
        return f"Drawing square with side {self.side}"

    def resize(self, factor: float) -> None:
        self.side *= factor


class Text:
    """Dessinable mais pas redimensionnable."""

    def __init__(self, content: str):
        self.content = content

    def draw(self) -> str:
        return f"Drawing text: {self.content}"


def render(shape: Drawable) -> None:
    """Accepte tout objet avec une méthode draw()."""
    print(f"  {shape.draw()}")


def scale_all(shapes: List[Resizable], factor: float) -> None:
    """Redimensionne tous les objets."""
    for shape in shapes:
        shape.resize(factor)


# Vérification à l'exécution
print("Vérification isinstance avec Protocol :")
circle = Circle(5.0)
square = Square(10.0)
text = Text("Hello")

print(f"  Circle is Drawable: {isinstance(circle, Drawable)}")
print(f"  Square is Drawable: {isinstance(square, Drawable)}")
print(f"  Text is Drawable: {isinstance(text, Drawable)}")
print(f"  Circle is Resizable: {isinstance(circle, Resizable)}")
print(f"  Text is Resizable: {isinstance(text, Resizable)}")

print("\nRendu polymorphique :")
shapes = [circle, square, text]
for shape in shapes:
    render(shape)


# =============================================================================
# 4. Protocoles vs ABC
# =============================================================================

print("\n" + "=" * 60)
print("4. PROTOCOLES VS ABC")
print("=" * 60)

from abc import ABC, abstractmethod


# Avec ABC : héritage requis
class DrawableABC(ABC):
    @abstractmethod
    def draw(self) -> str:
        pass


class CircleABC(DrawableABC):
    def __init__(self, radius: float):
        self.radius = radius

    def draw(self) -> str:
        return f"ABC Circle with radius {self.radius}"


# Avec Protocol : pas d'héritage requis
class CircleProtocol:
    def __init__(self, radius: float):
        self.radius = radius

    def draw(self) -> str:
        return f"Protocol Circle with radius {self.radius}"


print("ABC vs Protocol :")
print(f"  CircleABC bases: {CircleABC.__bases__}")
print(f"  CircleProtocol bases: {CircleProtocol.__bases__}")

# Le Protocol fonctionne même sans héritage
print(f"  CircleProtocol is Drawable: {isinstance(CircleProtocol(5), Drawable)}")


# =============================================================================
# 5. Protocoles avancés
# =============================================================================

print("\n" + "=" * 60)
print("5. PROTOCOLES AVANCÉS")
print("=" * 60)


@runtime_checkable
class Comparable(Protocol):
    """Protocole pour les objets comparables."""

    def __lt__(self, other: Any) -> bool:
        ...

    def __eq__(self, other: Any) -> bool:
        ...


@runtime_checkable
class Serializable(Protocol):
    """Protocole pour les objets sérialisables."""

    def to_dict(self) -> dict:
        ...

    @classmethod
    def from_dict(cls, data: dict) -> "Serializable":
        ...


class Product:
    def __init__(self, name: str, price: float):
        self.name = name
        self.price = price

    def __lt__(self, other: "Product") -> bool:
        return self.price < other.price

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Product):
            return NotImplemented
        return self.name == other.name and self.price == other.price

    def to_dict(self) -> dict:
        return {"name": self.name, "price": self.price}

    @classmethod
    def from_dict(cls, data: dict) -> "Product":
        return cls(data["name"], data["price"])


print("Product implémente les protocoles :")
p = Product("Widget", 29.99)
print(f"  is Comparable: {isinstance(p, Comparable)}")
print(f"  is Serializable: {isinstance(p, Serializable)}")

products = [
    Product("C", 30),
    Product("A", 10),
    Product("B", 20),
]
print(f"\nTri de produits : {[p.name for p in sorted(products)]}")


# =============================================================================
# 6. Pattern avec Protocol : Repository
# =============================================================================

print("\n" + "=" * 60)
print("6. PATTERN REPOSITORY AVEC PROTOCOL")
print("=" * 60)


@runtime_checkable
class Repository(Protocol[Any]):
    """Protocole générique pour les repositories."""

    def get(self, id: int) -> Any:
        ...

    def save(self, entity: Any) -> Any:
        ...

    def delete(self, id: int) -> bool:
        ...

    def find_all(self) -> List[Any]:
        ...


class InMemoryUserRepository:
    """Implémente le protocole sans hériter."""

    def __init__(self):
        self._storage = {}
        self._next_id = 1

    def get(self, id: int):
        return self._storage.get(id)

    def save(self, entity):
        if not hasattr(entity, 'id') or entity.id is None:
            entity.id = self._next_id
            self._next_id += 1
        self._storage[entity.id] = entity
        return entity

    def delete(self, id: int) -> bool:
        if id in self._storage:
            del self._storage[id]
            return True
        return False

    def find_all(self):
        return list(self._storage.values())


class User:
    def __init__(self, name: str):
        self.id = None
        self.name = name

    def __repr__(self):
        return f"User(id={self.id}, name={self.name!r})"


def process_users(repo: Repository):
    """Fonction qui utilise n'importe quel repository."""
    users = repo.find_all()
    print(f"  {len(users)} utilisateur(s) trouvé(s)")
    return users


repo = InMemoryUserRepository()
print(f"InMemoryUserRepository is Repository: {isinstance(repo, Repository)}")

repo.save(User("Alice"))
repo.save(User("Bob"))
process_users(repo)
