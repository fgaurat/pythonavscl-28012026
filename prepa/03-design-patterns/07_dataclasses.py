"""
Dataclasses
===========

Génération automatique du boilerplate pour les classes de données.
"""

from dataclasses import dataclass, field, asdict, astuple, fields, replace
from typing import List, Optional
from datetime import datetime

# =============================================================================
# 1. Le problème du boilerplate
# =============================================================================

print("=" * 60)
print("1. LE PROBLÈME DU BOILERPLATE")
print("=" * 60)


# Classe traditionnelle : beaucoup de code répétitif
class PointClassique:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"PointClassique(x={self.x}, y={self.y})"

    def __eq__(self, other):
        if not isinstance(other, PointClassique):
            return NotImplemented
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash((self.x, self.y))


p1 = PointClassique(1.0, 2.0)
p2 = PointClassique(1.0, 2.0)
print(f"Classe traditionnelle :")
print(f"  {p1}")
print(f"  p1 == p2 : {p1 == p2}")


# =============================================================================
# 2. Dataclass : syntaxe de base
# =============================================================================

print("\n" + "=" * 60)
print("2. DATACLASS : SYNTAXE DE BASE")
print("=" * 60)


@dataclass
class Point:
    x: float
    y: float


p1 = Point(1.0, 2.0)
p2 = Point(1.0, 2.0)
p3 = Point(3.0, 4.0)

print("Dataclass :")
print(f"  {p1}")
print(f"  p1 == p2 : {p1 == p2}")
print(f"  p1 == p3 : {p1 == p3}")
print(f"  p1.x : {p1.x}")


# =============================================================================
# 3. Options du décorateur
# =============================================================================

print("\n" + "=" * 60)
print("3. OPTIONS DU DÉCORATEUR")
print("=" * 60)


# frozen=True : instance immutable
@dataclass(frozen=True)
class Coordonnees:
    latitude: float
    longitude: float


coord = Coordonnees(48.8566, 2.3522)
print(f"Coordonnées (frozen) : {coord}")

try:
    coord.latitude = 0
except Exception as e:
    print(f"  Modification interdite : {type(e).__name__}")

# Peut être utilisé comme clé de dictionnaire
locations = {coord: "Paris"}
print(f"  Utilisable comme clé : {locations[coord]}")


# order=True : comparaisons automatiques
@dataclass(order=True)
class Version:
    major: int
    minor: int
    patch: int


versions = [Version(2, 0, 0), Version(1, 9, 5), Version(2, 1, 0), Version(1, 0, 0)]
print(f"\nVersions triées : {sorted(versions)}")


# =============================================================================
# 4. Valeurs par défaut et field()
# =============================================================================

print("\n" + "=" * 60)
print("4. VALEURS PAR DÉFAUT ET FIELD()")
print("=" * 60)


@dataclass
class Utilisateur:
    nom: str
    email: str
    age: int = 0  # Valeur par défaut simple

    # Utiliser field() avec default_factory pour les mutables
    tags: List[str] = field(default_factory=list)

    # Champ exclu de __init__ mais calculé
    nom_complet: str = field(init=False)

    # Champ exclu de repr
    _password_hash: str = field(default="", repr=False)

    def __post_init__(self):
        """Appelé après __init__ pour des initialisations complexes."""
        self.nom_complet = f"{self.nom} <{self.email}>"


user = Utilisateur("Alice", "alice@example.com", tags=["admin", "vip"])
print(f"Utilisateur : {user}")
print(f"  nom_complet : {user.nom_complet}")
print(f"  tags : {user.tags}")


# Démonstration du problème des mutables
@dataclass
class MauvaisExemple:
    # NE PAS FAIRE : liste = []  # Partagée entre instances !
    pass


@dataclass
class BonExemple:
    items: List[str] = field(default_factory=list)  # Nouvelle liste par instance


b1 = BonExemple()
b2 = BonExemple()
b1.items.append("test")
print(f"\nBonExemple - b1.items: {b1.items}, b2.items: {b2.items}")


# =============================================================================
# 5. Options de field()
# =============================================================================

print("\n" + "=" * 60)
print("5. OPTIONS DE FIELD()")
print("=" * 60)


@dataclass
class Article:
    titre: str
    contenu: str

    # Exclu de repr pour la lisibilité
    contenu_html: str = field(repr=False, default="")

    # Exclu de la comparaison
    vues: int = field(compare=False, default=0)

    # Métadonnées personnalisées
    auteur: str = field(
        metadata={"description": "Auteur de l'article", "required": True},
        default="Anonyme"
    )

    # Champ calculé, pas dans __init__
    slug: str = field(init=False)

    def __post_init__(self):
        self.slug = self.titre.lower().replace(" ", "-")


article = Article("Mon Article", "Contenu...", auteur="Alice")
print(f"Article : {article}")
print(f"  slug : {article.slug}")

# Accès aux métadonnées
for f in fields(article):
    if f.metadata:
        print(f"  {f.name} metadata : {f.metadata}")


# =============================================================================
# 6. Héritage de dataclasses
# =============================================================================

print("\n" + "=" * 60)
print("6. HÉRITAGE DE DATACLASSES")
print("=" * 60)


@dataclass
class Entity:
    id: int
    created_at: datetime = field(default_factory=datetime.now)


@dataclass
class User(Entity):
    username: str = ""
    email: str = ""
    is_active: bool = True


@dataclass
class Admin(User):
    permissions: List[str] = field(default_factory=list)


admin = Admin(
    id=1,
    username="admin",
    email="admin@example.com",
    permissions=["read", "write", "delete"]
)
print(f"Admin : {admin}")
print(f"  Héritage : Admin -> User -> Entity")


# =============================================================================
# 7. Fonctions utilitaires
# =============================================================================

print("\n" + "=" * 60)
print("7. FONCTIONS UTILITAIRES")
print("=" * 60)


@dataclass
class Produit:
    nom: str
    prix: float
    stock: int = 0


p = Produit("Widget", 29.99, 100)

# Conversion en dictionnaire
print(f"asdict : {asdict(p)}")

# Conversion en tuple
print(f"astuple : {astuple(p)}")

# Introspection des champs
print("fields :")
for f in fields(p):
    print(f"  {f.name}: {f.type.__name__}, default={f.default}")

# Copie avec modification (immutabilité fonctionnelle)
p2 = replace(p, prix=24.99, stock=50)
print(f"\nOriginal : {p}")
print(f"Modifié : {p2}")


# =============================================================================
# 8. Dataclass avec slots (Python 3.10+)
# =============================================================================

print("\n" + "=" * 60)
print("8. DATACLASS AVEC SLOTS (PYTHON 3.10+)")
print("=" * 60)

import sys

if sys.version_info >= (3, 10):
    @dataclass(slots=True)
    class PointSlots:
        x: float
        y: float

    p_slots = PointSlots(1.0, 2.0)
    print(f"Point avec slots : {p_slots}")
    print(f"  Utilise moins de mémoire")
else:
    print("  slots=True nécessite Python 3.10+")


# =============================================================================
# 9. Cas d'usage : configuration
# =============================================================================

print("\n" + "=" * 60)
print("9. CAS D'USAGE : CONFIGURATION")
print("=" * 60)


@dataclass(frozen=True)
class DatabaseConfig:
    host: str
    port: int = 5432
    database: str = "default"
    username: str = "postgres"
    password: str = field(repr=False, default="")

    @property
    def connection_string(self) -> str:
        return f"postgresql://{self.username}:{self.password}@{self.host}:{self.port}/{self.database}"


@dataclass(frozen=True)
class AppConfig:
    debug: bool = False
    log_level: str = "INFO"
    database: DatabaseConfig = field(default_factory=lambda: DatabaseConfig("localhost"))


config = AppConfig(
    debug=True,
    database=DatabaseConfig(
        host="db.example.com",
        database="myapp",
        password="secret"
    )
)

print(f"Config : {config}")
print(f"  Connection : {config.database.connection_string}")


# =============================================================================
# 10. Quand utiliser dataclass ?
# =============================================================================

print("\n" + "=" * 60)
print("10. QUAND UTILISER DATACLASS ?")
print("=" * 60)

print("""
✅ CAS D'USAGE IDÉAUX :
• Structures de données internes simples
• DTOs (Data Transfer Objects) sans validation externe
• Configuration interne de l'application
• Objets immuables (frozen=True)
• Value Objects du Domain-Driven Design

❌ À ÉVITER QUAND :
• Validation de données externes requise → Pydantic
• Sérialisation JSON complexe requise → Pydantic
• Données provenant d'API/utilisateurs → Pydantic

💡 CONSEIL :
Dataclass = données internes de confiance
Pydantic = données externes à valider
""")
