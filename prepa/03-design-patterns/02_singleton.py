"""
Pattern Singleton
=================

Garantir qu'une classe n'a qu'une seule instance.
"""

from functools import wraps

# =============================================================================
# 1. Singleton avec décorateur (recommandé)
# =============================================================================

print("=" * 60)
print("1. SINGLETON AVEC DÉCORATEUR")
print("=" * 60)


def singleton(cls):
    """Décorateur transformant une classe en singleton."""
    instances = {}

    @wraps(cls)
    def get_instance(*args, **kwargs):
        if cls not in instances:
            print(f"  Création de l'instance unique de {cls.__name__}")
            instances[cls] = cls(*args, **kwargs)
        else:
            print(f"  Retour de l'instance existante de {cls.__name__}")
        return instances[cls]

    return get_instance


@singleton
class Configuration:
    def __init__(self):
        self.settings = {}

    def set(self, key, value):
        self.settings[key] = value

    def get(self, key, default=None):
        return self.settings.get(key, default)


print("Première instanciation :")
config1 = Configuration()
config1.set("debug", True)

print("\nDeuxième instanciation :")
config2 = Configuration()

print(f"\nconfig1 is config2 : {config1 is config2}")
print(f"config2.get('debug') : {config2.get('debug')}")


# =============================================================================
# 2. Singleton avec métaclasse
# =============================================================================

print("\n" + "=" * 60)
print("2. SINGLETON AVEC MÉTACLASSE")
print("=" * 60)


class SingletonMeta(type):
    """Métaclasse implémentant le pattern Singleton."""
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            print(f"  Création de l'instance unique de {cls.__name__}")
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        else:
            print(f"  Retour de l'instance existante de {cls.__name__}")
        return cls._instances[cls]


class Database(metaclass=SingletonMeta):
    def __init__(self, connection_string):
        self.connection_string = connection_string
        self.connected = False

    def connect(self):
        self.connected = True
        return f"Connecté à {self.connection_string}"

    def disconnect(self):
        self.connected = False


print("Première instanciation :")
db1 = Database("postgresql://localhost/mydb")

print("\nDeuxième instanciation :")
db2 = Database("mysql://localhost/otherdb")  # Ignoré !

print(f"\ndb1 is db2 : {db1 is db2}")
print(f"Connection string : {db2.connection_string}")  # postgresql


# =============================================================================
# 3. Module comme Singleton (pythonique)
# =============================================================================

print("\n" + "=" * 60)
print("3. MODULE COMME SINGLETON (PYTHONIQUE)")
print("=" * 60)

# Simulation d'un module config.py
# En Python, un module est naturellement un singleton


class _ConfigModule:
    """Simule un module de configuration."""

    def __init__(self):
        self._settings = {}
        self._loaded = False

    def get(self, key, default=None):
        return self._settings.get(key, default)

    def set(self, key, value):
        self._settings[key] = value

    def load_from_dict(self, data):
        self._settings.update(data)
        self._loaded = True
        print(f"  Configuration chargée : {list(data.keys())}")

    def is_loaded(self):
        return self._loaded


# Instance unique au niveau module
config = _ConfigModule()


# Utilisation
config.load_from_dict({
    "debug": True,
    "database_url": "postgresql://localhost/db",
    "api_key": "secret123"
})

print(f"debug = {config.get('debug')}")
print(f"database_url = {config.get('database_url')}")


# =============================================================================
# 4. Singleton thread-safe
# =============================================================================

print("\n" + "=" * 60)
print("4. SINGLETON THREAD-SAFE")
print("=" * 60)

import threading


class ThreadSafeSingleton:
    """Singleton thread-safe avec double-checked locking."""
    _instance = None
    _lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            with cls._lock:
                # Double-check après acquisition du verrou
                if cls._instance is None:
                    print(f"  Création thread-safe de {cls.__name__}")
                    cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, value=None):
        # __init__ est appelé à chaque fois, protéger les attributs
        if not hasattr(self, '_initialized'):
            self.value = value
            self._initialized = True


# Test thread-safe
instances = []


def create_instance():
    instance = ThreadSafeSingleton("test")
    instances.append(instance)


threads = [threading.Thread(target=create_instance) for _ in range(5)]
for t in threads:
    t.start()
for t in threads:
    t.join()

print(f"Nombre d'instances créées : {len(set(id(i) for i in instances))}")
print(f"Toutes identiques : {all(i is instances[0] for i in instances)}")


# =============================================================================
# 5. Singleton avec reset (pour les tests)
# =============================================================================

print("\n" + "=" * 60)
print("5. SINGLETON AVEC RESET (POUR LES TESTS)")
print("=" * 60)


class ResettableSingleton:
    """Singleton qui peut être réinitialisé (utile pour les tests)."""
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, name="default"):
        if not hasattr(self, '_initialized'):
            self.name = name
            self._initialized = True
            print(f"  Initialisation avec name='{name}'")

    @classmethod
    def reset(cls):
        """Réinitialise le singleton (pour les tests)."""
        cls._instance = None
        print("  Singleton réinitialisé")

    @classmethod
    def get_instance(cls):
        """Retourne l'instance ou None si pas encore créée."""
        return cls._instance


# Utilisation normale
s1 = ResettableSingleton("production")
print(f"s1.name = '{s1.name}'")

s2 = ResettableSingleton("autre")  # Ignoré
print(f"s2.name = '{s2.name}'")

# Reset pour les tests
print("\nReset :")
ResettableSingleton.reset()

s3 = ResettableSingleton("test")
print(f"s3.name = '{s3.name}'")


# =============================================================================
# 6. Quand utiliser le Singleton ?
# =============================================================================

print("\n" + "=" * 60)
print("6. QUAND UTILISER LE SINGLETON ?")
print("=" * 60)

print("""
CAS D'USAGE LÉGITIMES :
✅ Configuration globale de l'application
✅ Pool de connexions à une base de données
✅ Logger centralisé
✅ Cache partagé
✅ Gestionnaire de ressources (thread pool, etc.)

À ÉVITER :
❌ Utiliser comme variable globale déguisée
❌ Rendre le code difficile à tester
❌ Créer des dépendances cachées

ALTERNATIVES :
• Module Python (naturellement singleton)
• Injection de dépendances
• Contexte applicatif (Flask, FastAPI)

CONSEIL : Préférez le module-singleton ou l'injection de dépendances
""")
