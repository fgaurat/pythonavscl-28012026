"""
Pattern Factory
===============

Création d'objets sans exposer la logique de création au client.
"""

from abc import ABC, abstractmethod

# =============================================================================
# 1. Classes de base
# =============================================================================

print("=" * 60)
print("1. CLASSES DE BASE")
print("=" * 60)


class Animal(ABC):
    @abstractmethod
    def parler(self):
        pass

    @abstractmethod
    def deplacer(self):
        pass


class Chien(Animal):
    def parler(self):
        return "Wouf !"

    def deplacer(self):
        return "Le chien court"


class Chat(Animal):
    def parler(self):
        return "Miaou !"

    def deplacer(self):
        return "Le chat marche silencieusement"


class Oiseau(Animal):
    def parler(self):
        return "Cui cui !"

    def deplacer(self):
        return "L'oiseau vole"


# =============================================================================
# 2. Factory Method classique
# =============================================================================

print("\n" + "=" * 60)
print("2. FACTORY METHOD CLASSIQUE")
print("=" * 60)


class AnimalFactory:
    """Factory qui crée des animaux selon le type demandé."""

    @staticmethod
    def creer(type_animal: str) -> Animal:
        factories = {
            "chien": Chien,
            "chat": Chat,
            "oiseau": Oiseau,
        }

        if type_animal not in factories:
            raise ValueError(f"Type inconnu : {type_animal}")

        return factories[type_animal]()


# Utilisation
for animal_type in ["chien", "chat", "oiseau"]:
    animal = AnimalFactory.creer(animal_type)
    print(f"  {animal_type}: {animal.parler()}")

try:
    AnimalFactory.creer("serpent")
except ValueError as e:
    print(f"  Erreur : {e}")


# =============================================================================
# 3. Factory avec décorateur (Registry pattern)
# =============================================================================

print("\n" + "=" * 60)
print("3. FACTORY AVEC DÉCORATEUR (REGISTRY)")
print("=" * 60)


class AnimalRegistry:
    """Registry avec enregistrement automatique via décorateur."""
    _animals = {}

    @classmethod
    def register(cls, name):
        def decorator(animal_class):
            cls._animals[name] = animal_class
            print(f"    Enregistré : {name} -> {animal_class.__name__}")
            return animal_class
        return decorator

    @classmethod
    def create(cls, name: str) -> Animal:
        if name not in cls._animals:
            raise ValueError(f"Animal inconnu : {name}")
        return cls._animals[name]()

    @classmethod
    def list_animals(cls):
        return list(cls._animals.keys())


print("Enregistrement des animaux :")


@AnimalRegistry.register("chien")
class ChienV2(Animal):
    def parler(self):
        return "Wouf wouf !"

    def deplacer(self):
        return "Le chien court"


@AnimalRegistry.register("chat")
class ChatV2(Animal):
    def parler(self):
        return "Miaou miaou !"

    def deplacer(self):
        return "Le chat se faufile"


@AnimalRegistry.register("perroquet")
class Perroquet(Animal):
    def parler(self):
        return "Coco veut un gâteau !"

    def deplacer(self):
        return "Le perroquet vole"


print(f"\nAnimaux disponibles : {AnimalRegistry.list_animals()}")
print("\nUtilisation :")
for name in AnimalRegistry.list_animals():
    animal = AnimalRegistry.create(name)
    print(f"  {name}: {animal.parler()}")


# =============================================================================
# 4. Abstract Factory
# =============================================================================

print("\n" + "=" * 60)
print("4. ABSTRACT FACTORY")
print("=" * 60)


# Produits abstraits
class Button(ABC):
    @abstractmethod
    def render(self):
        pass


class Input(ABC):
    @abstractmethod
    def render(self):
        pass


# Produits concrets - Dark Theme
class DarkButton(Button):
    def render(self):
        return "[Dark Button]"


class DarkInput(Input):
    def render(self):
        return "[Dark Input ____]"


# Produits concrets - Light Theme
class LightButton(Button):
    def render(self):
        return "(Light Button)"


class LightInput(Input):
    def render(self):
        return "(Light Input ____)"


# Abstract Factory
class UIFactory(ABC):
    @abstractmethod
    def creer_bouton(self) -> Button:
        pass

    @abstractmethod
    def creer_input(self) -> Input:
        pass


class DarkThemeFactory(UIFactory):
    def creer_bouton(self):
        return DarkButton()

    def creer_input(self):
        return DarkInput()


class LightThemeFactory(UIFactory):
    def creer_bouton(self):
        return LightButton()

    def creer_input(self):
        return LightInput()


def creer_interface(factory: UIFactory):
    """Crée une interface cohérente avec le thème choisi."""
    bouton = factory.creer_bouton()
    input_field = factory.creer_input()
    return f"Interface : {bouton.render()} {input_field.render()}"


print("Dark Theme :")
print(f"  {creer_interface(DarkThemeFactory())}")

print("\nLight Theme :")
print(f"  {creer_interface(LightThemeFactory())}")


# =============================================================================
# 5. Factory avec configuration
# =============================================================================

print("\n" + "=" * 60)
print("5. FACTORY AVEC CONFIGURATION")
print("=" * 60)


class DatabaseConnection(ABC):
    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def execute(self, query: str):
        pass


class PostgreSQLConnection(DatabaseConnection):
    def __init__(self, host, port, database):
        self.host = host
        self.port = port
        self.database = database

    def connect(self):
        return f"Connecté à PostgreSQL {self.host}:{self.port}/{self.database}"

    def execute(self, query):
        return f"PostgreSQL exécute : {query}"


class MySQLConnection(DatabaseConnection):
    def __init__(self, host, port, database):
        self.host = host
        self.port = port
        self.database = database

    def connect(self):
        return f"Connecté à MySQL {self.host}:{self.port}/{self.database}"

    def execute(self, query):
        return f"MySQL exécute : {query}"


class SQLiteConnection(DatabaseConnection):
    def __init__(self, filepath):
        self.filepath = filepath

    def connect(self):
        return f"Connecté à SQLite {self.filepath}"

    def execute(self, query):
        return f"SQLite exécute : {query}"


class DatabaseFactory:
    """Factory créant des connexions selon la configuration."""

    @staticmethod
    def create(config: dict) -> DatabaseConnection:
        db_type = config.get("type", "sqlite")

        if db_type == "postgresql":
            return PostgreSQLConnection(
                host=config.get("host", "localhost"),
                port=config.get("port", 5432),
                database=config.get("database", "default")
            )
        elif db_type == "mysql":
            return MySQLConnection(
                host=config.get("host", "localhost"),
                port=config.get("port", 3306),
                database=config.get("database", "default")
            )
        elif db_type == "sqlite":
            return SQLiteConnection(
                filepath=config.get("filepath", ":memory:")
            )
        else:
            raise ValueError(f"Type de base inconnu : {db_type}")


# Configurations
configs = [
    {"type": "postgresql", "host": "db.example.com", "port": 5432, "database": "myapp"},
    {"type": "mysql", "host": "localhost", "database": "test"},
    {"type": "sqlite", "filepath": "data.db"},
]

for config in configs:
    db = DatabaseFactory.create(config)
    print(f"  {db.connect()}")
