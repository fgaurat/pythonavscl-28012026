"""
Classes Abstraites (ABC)
========================

Utilisation du module abc pour définir des interfaces et des classes abstraites.
"""

from abc import ABC, abstractmethod
import math

# =============================================================================
# 1. Le problème sans ABC
# =============================================================================

print("=" * 60)
print("1. LE PROBLÈME SANS ABC")
print("=" * 60)


class AnimalSansABC:
    def parler(self):
        pass  # Pas d'implémentation


class ChienSansABC(AnimalSansABC):
    pass  # Oubli d'implémenter parler()


chien = ChienSansABC()
chien.parler()  # Aucune erreur, mais ne fait rien !
print("ChienSansABC.parler() n'a pas levé d'erreur (problème !)")


# =============================================================================
# 2. La solution avec ABC
# =============================================================================

print("\n" + "=" * 60)
print("2. LA SOLUTION AVEC ABC")
print("=" * 60)


class Animal(ABC):
    @abstractmethod
    def parler(self):
        """Doit être implémenté par les sous-classes."""
        pass


class Chien(Animal):
    def parler(self):
        return "Wouf !"


class Chat(Animal):
    def parler(self):
        return "Miaou !"


# Tentative d'instancier la classe abstraite
try:
    animal = Animal()
except TypeError as e:
    print(f"Animal() : TypeError - {e}")

# Tentative d'instancier une sous-classe incomplète
try:
    class ChienIncomplet(Animal):
        pass

    chien = ChienIncomplet()
except TypeError as e:
    print(f"ChienIncomplet() : TypeError")

# Les sous-classes complètes fonctionnent
chien = Chien()
chat = Chat()
print(f"\nChien().parler() = '{chien.parler()}'")
print(f"Chat().parler() = '{chat.parler()}'")


# =============================================================================
# 3. Classe abstraite complète
# =============================================================================

print("\n" + "=" * 60)
print("3. CLASSE ABSTRAITE COMPLÈTE")
print("=" * 60)


class Forme(ABC):
    """Classe abstraite définissant l'interface d'une forme."""

    @abstractmethod
    def aire(self):
        """Calcule l'aire de la forme."""
        pass

    @abstractmethod
    def perimetre(self):
        """Calcule le périmètre de la forme."""
        pass

    def description(self):
        """Méthode concrète (implémentation par défaut)."""
        return f"{self.__class__.__name__} avec aire={self.aire():.2f}"


class Rectangle(Forme):
    def __init__(self, largeur, hauteur):
        self.largeur = largeur
        self.hauteur = hauteur

    def aire(self):
        return self.largeur * self.hauteur

    def perimetre(self):
        return 2 * (self.largeur + self.hauteur)


class Cercle(Forme):
    def __init__(self, rayon):
        self.rayon = rayon

    def aire(self):
        return math.pi * self.rayon ** 2

    def perimetre(self):
        return 2 * math.pi * self.rayon


class Triangle(Forme):
    def __init__(self, base, hauteur, cote1, cote2, cote3):
        self.base = base
        self.hauteur = hauteur
        self.cotes = (cote1, cote2, cote3)

    def aire(self):
        return 0.5 * self.base * self.hauteur

    def perimetre(self):
        return sum(self.cotes)


# Utilisation polymorphique
formes = [Rectangle(4, 5), Cercle(3), Triangle(3, 4, 3, 4, 5)]

for forme in formes:
    print(f"  {forme.description()}, périmètre={forme.perimetre():.2f}")


# =============================================================================
# 4. Propriétés abstraites
# =============================================================================

print("\n" + "=" * 60)
print("4. PROPRIÉTÉS ABSTRAITES")
print("=" * 60)


class Vehicule(ABC):
    @property
    @abstractmethod
    def vitesse_max(self):
        """Vitesse maximale en km/h."""
        pass

    @property
    @abstractmethod
    def carburant(self):
        """Type de carburant."""
        pass

    def description(self):
        return f"{self.__class__.__name__}: {self.vitesse_max}km/h, {self.carburant}"


class Voiture(Vehicule):
    @property
    def vitesse_max(self):
        return 200

    @property
    def carburant(self):
        return "essence"


class VoitureElectrique(Vehicule):
    @property
    def vitesse_max(self):
        return 180

    @property
    def carburant(self):
        return "électricité"


class Velo(Vehicule):
    @property
    def vitesse_max(self):
        return 40

    @property
    def carburant(self):
        return "effort humain"


vehicules = [Voiture(), VoitureElectrique(), Velo()]
for v in vehicules:
    print(f"  {v.description()}")


# =============================================================================
# 5. Méthodes de classe abstraites
# =============================================================================

print("\n" + "=" * 60)
print("5. MÉTHODES DE CLASSE ABSTRAITES")
print("=" * 60)


class Serializable(ABC):
    @classmethod
    @abstractmethod
    def from_dict(cls, data: dict):
        """Crée une instance depuis un dictionnaire."""
        pass

    @abstractmethod
    def to_dict(self) -> dict:
        """Convertit l'instance en dictionnaire."""
        pass


class Utilisateur(Serializable):
    def __init__(self, nom, email):
        self.nom = nom
        self.email = email

    @classmethod
    def from_dict(cls, data):
        return cls(data["nom"], data["email"])

    def to_dict(self):
        return {"nom": self.nom, "email": self.email}

    def __repr__(self):
        return f"Utilisateur({self.nom!r}, {self.email!r})"


# Sérialisation / désérialisation
data = {"nom": "Alice", "email": "alice@example.com"}
user = Utilisateur.from_dict(data)
print(f"from_dict({data}) = {user}")
print(f"to_dict() = {user.to_dict()}")


# =============================================================================
# 6. Méthode abstraite avec implémentation par défaut
# =============================================================================

print("\n" + "=" * 60)
print("6. MÉTHODE ABSTRAITE AVEC IMPLÉMENTATION PAR DÉFAUT")
print("=" * 60)


class Logger(ABC):
    @abstractmethod
    def log(self, message):
        """Les sous-classes DOIVENT appeler super().log()"""
        # Implémentation par défaut : ajouter un timestamp
        from datetime import datetime
        return f"[{datetime.now().strftime('%H:%M:%S')}] {message}"


class ConsoleLogger(Logger):
    def log(self, message):
        # Appelle l'implémentation par défaut
        formatted = super().log(message)
        print(f"  CONSOLE: {formatted}")


class FileLogger(Logger):
    def __init__(self, filename):
        self.filename = filename

    def log(self, message):
        formatted = super().log(message)
        # Simulation d'écriture fichier
        print(f"  FILE ({self.filename}): {formatted}")


console = ConsoleLogger()
file = FileLogger("app.log")

console.log("Message de test")
file.log("Autre message")


# =============================================================================
# 7. Enregistrement virtuel avec ABC
# =============================================================================

print("\n" + "=" * 60)
print("7. ENREGISTREMENT VIRTUEL")
print("=" * 60)


class Printable(ABC):
    @abstractmethod
    def __str__(self):
        pass


# Enregistrer des classes existantes comme "virtuelles"
Printable.register(int)
Printable.register(str)
Printable.register(list)

print("Vérification isinstance avec register() :")
print(f"  isinstance(42, Printable) = {isinstance(42, Printable)}")
print(f"  isinstance('hello', Printable) = {isinstance('hello', Printable)}")
print(f"  isinstance([1,2,3], Printable) = {isinstance([1,2,3], Printable)}")


# Classe personnalisée
class MonObjet:
    def __str__(self):
        return "MonObjet"


Printable.register(MonObjet)
print(f"  isinstance(MonObjet(), Printable) = {isinstance(MonObjet(), Printable)}")


# =============================================================================
# 8. ABC vs Duck Typing
# =============================================================================

print("\n" + "=" * 60)
print("8. ABC VS DUCK TYPING")
print("=" * 60)


# Duck typing : pas de vérification, erreur tardive
def traiter_duck(obj):
    """Suppose que obj a une méthode process()"""
    return obj.process()


class ProcesseurA:
    def process(self):
        return "A traité"


class ProcesseurB:
    pass  # Oubli de process()


print("Duck typing :")
print(f"  traiter_duck(ProcesseurA()) = {traiter_duck(ProcesseurA())}")
try:
    traiter_duck(ProcesseurB())
except AttributeError as e:
    print(f"  traiter_duck(ProcesseurB()) : AttributeError (erreur tardive)")


# ABC : vérification précoce
class Processeur(ABC):
    @abstractmethod
    def process(self):
        pass


class ProcesseurC(Processeur):
    def process(self):
        return "C traité"


print("\nABC :")
try:
    class ProcesseurD(Processeur):
        pass  # Oubli de process()

    ProcesseurD()
except TypeError:
    print("  ProcesseurD() : TypeError (erreur précoce, à l'instanciation)")


# =============================================================================
# 9. Exemple pratique : Repository pattern
# =============================================================================

print("\n" + "=" * 60)
print("9. EXEMPLE PRATIQUE : REPOSITORY PATTERN")
print("=" * 60)


class Repository(ABC):
    """Interface abstraite pour les repositories."""

    @abstractmethod
    def get(self, id):
        """Récupère une entité par son ID."""
        pass

    @abstractmethod
    def save(self, entity):
        """Sauvegarde une entité."""
        pass

    @abstractmethod
    def delete(self, id):
        """Supprime une entité."""
        pass

    @abstractmethod
    def find_all(self):
        """Récupère toutes les entités."""
        pass


class InMemoryUserRepository(Repository):
    """Implémentation en mémoire pour les tests."""

    def __init__(self):
        self._storage = {}
        self._next_id = 1

    def get(self, id):
        return self._storage.get(id)

    def save(self, entity):
        if not hasattr(entity, 'id') or entity.id is None:
            entity.id = self._next_id
            self._next_id += 1
        self._storage[entity.id] = entity
        return entity

    def delete(self, id):
        if id in self._storage:
            del self._storage[id]

    def find_all(self):
        return list(self._storage.values())


class User:
    def __init__(self, name, email):
        self.id = None
        self.name = name
        self.email = email

    def __repr__(self):
        return f"User(id={self.id}, name={self.name!r})"


# Utilisation
repo = InMemoryUserRepository()

user1 = repo.save(User("Alice", "alice@example.com"))
user2 = repo.save(User("Bob", "bob@example.com"))

print(f"Tous les users : {repo.find_all()}")
print(f"User 1 : {repo.get(1)}")

repo.delete(1)
print(f"Après suppression : {repo.find_all()}")
