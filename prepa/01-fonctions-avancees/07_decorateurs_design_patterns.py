"""
Décorateurs et Design Patterns
==============================

Implémentation de patterns classiques avec des décorateurs.
"""

from functools import wraps

# =============================================================================
# 1. Pattern Singleton
# =============================================================================

print("=" * 60)
print("1. PATTERN SINGLETON")
print("=" * 60)


def singleton(cls):
    """Décorateur qui transforme une classe en singleton."""
    instances = {}

    @wraps(cls)
    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return get_instance


@singleton
class Configuration:
    def __init__(self):
        print("  Chargement de la configuration...")
        self.settings = {"debug": True, "database": "postgresql"}

    def get(self, key):
        return self.settings.get(key)


print("Première création :")
config1 = Configuration()

print("\nDeuxième création (pas de nouveau chargement) :")
config2 = Configuration()

print(f"\nconfig1 is config2 : {config1 is config2}")
print(f"config1.get('debug') : {config1.get('debug')}")


# =============================================================================
# 2. Pattern Observer avec décorateur
# =============================================================================

print("\n" + "=" * 60)
print("2. PATTERN OBSERVER")
print("=" * 60)


class EventManager:
    """Gestionnaire d'événements avec décorateur."""
    _handlers = {}

    @classmethod
    def on(cls, event_name):
        """Décorateur pour enregistrer un handler."""
        def decorator(func):
            if event_name not in cls._handlers:
                cls._handlers[event_name] = []
            cls._handlers[event_name].append(func)
            return func
        return decorator

    @classmethod
    def emit(cls, event_name, *args, **kwargs):
        """Émet un événement vers tous les handlers."""
        for handler in cls._handlers.get(event_name, []):
            handler(*args, **kwargs)

    @classmethod
    def clear(cls):
        """Nettoie tous les handlers."""
        cls._handlers = {}


# Enregistrement des handlers avec décorateurs
@EventManager.on("user_created")
def envoyer_email(user):
    print(f"  📧 Email de bienvenue envoyé à {user['email']}")


@EventManager.on("user_created")
def logger_creation(user):
    print(f"  📝 Log : Utilisateur '{user['nom']}' créé")


@EventManager.on("user_created")
def notifier_admin(user):
    print(f"  🔔 Admin notifié de la création de {user['nom']}")


@EventManager.on("order_placed")
def traiter_commande(order):
    print(f"  📦 Commande #{order['id']} en cours de traitement")


print("Émission de l'événement 'user_created' :")
EventManager.emit("user_created", {"nom": "Alice", "email": "alice@example.com"})

print("\nÉmission de l'événement 'order_placed' :")
EventManager.emit("order_placed", {"id": 12345, "total": 99.99})

EventManager.clear()  # Nettoyage pour les autres exemples


# =============================================================================
# 3. Pattern Registry
# =============================================================================

print("\n" + "=" * 60)
print("3. PATTERN REGISTRY")
print("=" * 60)


class CommandRegistry:
    """Registre de commandes avec décorateur."""
    _commands = {}

    @classmethod
    def register(cls, name):
        """Décorateur pour enregistrer une commande."""
        def decorator(func):
            cls._commands[name] = func
            return func
        return decorator

    @classmethod
    def execute(cls, name, *args, **kwargs):
        """Exécute une commande par son nom."""
        if name in cls._commands:
            return cls._commands[name](*args, **kwargs)
        raise ValueError(f"Commande inconnue : {name}")

    @classmethod
    def list_commands(cls):
        """Liste toutes les commandes disponibles."""
        return list(cls._commands.keys())


@CommandRegistry.register("help")
def show_help():
    return "Affiche l'aide"


@CommandRegistry.register("version")
def show_version():
    return "Version 1.0.0"


@CommandRegistry.register("greet")
def greet(name):
    return f"Bonjour, {name} !"


print(f"Commandes disponibles : {CommandRegistry.list_commands()}")
print(f"Exécution 'help' : {CommandRegistry.execute('help')}")
print(f"Exécution 'version' : {CommandRegistry.execute('version')}")
print(f"Exécution 'greet' : {CommandRegistry.execute('greet', 'Alice')}")


# =============================================================================
# 4. Pattern Validation
# =============================================================================

print("\n" + "=" * 60)
print("4. PATTERN VALIDATION")
print("=" * 60)


def valider_types(**types_attendus):
    """Valide les types des arguments."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Vérifier les arguments nommés
            for nom, type_attendu in types_attendus.items():
                if nom in kwargs:
                    if not isinstance(kwargs[nom], type_attendu):
                        raise TypeError(
                            f"{nom} doit être {type_attendu.__name__}, "
                            f"pas {type(kwargs[nom]).__name__}"
                        )
            return func(*args, **kwargs)
        return wrapper
    return decorator


@valider_types(nom=str, age=int)
def creer_utilisateur(nom, age):
    return {"nom": nom, "age": age}


print("creer_utilisateur(nom='Alice', age=30) :")
print(f"  {creer_utilisateur(nom='Alice', age=30)}")

print("\ncreer_utilisateur(nom='Bob', age='25') - TypeError attendu :")
try:
    creer_utilisateur(nom="Bob", age="25")
except TypeError as e:
    print(f"  Erreur : {e}")


# =============================================================================
# 5. Pattern Memoization
# =============================================================================

print("\n" + "=" * 60)
print("5. PATTERN MEMOIZATION")
print("=" * 60)


def memoize(func):
    """Cache les résultats des appels précédents."""
    cache = {}

    @wraps(func)
    def wrapper(*args):
        if args not in cache:
            print(f"  Calcul pour {args}")
            cache[args] = func(*args)
        else:
            print(f"  Cache hit pour {args}")
        return cache[args]

    wrapper.cache = cache
    wrapper.clear_cache = lambda: cache.clear()
    return wrapper


@memoize
def fibonacci(n):
    """Calcul de Fibonacci avec memoization."""
    if n < 2:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)


print("fibonacci(10) :")
resultat = fibonacci(10)
print(f"  Résultat : {resultat}")

print(f"\nContenu du cache : {len(fibonacci.cache)} entrées")


# =============================================================================
# 6. Pattern Decorator Stack (Pipeline)
# =============================================================================

print("\n" + "=" * 60)
print("6. PATTERN DECORATOR STACK (PIPELINE)")
print("=" * 60)


def uppercase(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        return result.upper()
    return wrapper


def add_greeting(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        return f"Bonjour, {result} !"
    return wrapper


def add_timestamp(func):
    from datetime import datetime

    @wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        return f"[{datetime.now().strftime('%H:%M:%S')}] {result}"
    return wrapper


@add_timestamp
@add_greeting
@uppercase
def get_name(name):
    return name


print(f"get_name('alice') = {get_name('alice')}")
print("\nOrdre d'application : uppercase -> add_greeting -> add_timestamp")


# =============================================================================
# 7. Décorateurs built-in : @functools.lru_cache
# =============================================================================

print("\n" + "=" * 60)
print("7. DÉCORATEUR BUILT-IN : @lru_cache")
print("=" * 60)

from functools import lru_cache
import time


@lru_cache(maxsize=128)
def fibonacci_lru(n):
    """Calcul de Fibonacci avec cache automatique."""
    if n < 2:
        return n
    return fibonacci_lru(n - 1) + fibonacci_lru(n - 2)


# Mesure du temps
debut = time.perf_counter()
resultat = fibonacci_lru(35)
duree = time.perf_counter() - debut

print(f"fibonacci_lru(35) = {resultat}")
print(f"Temps : {duree:.6f}s")

# Statistiques du cache
print(f"\nStatistiques du cache :")
print(f"  {fibonacci_lru.cache_info()}")

# Vider le cache
fibonacci_lru.cache_clear()
print(f"\nAprès cache_clear() :")
print(f"  {fibonacci_lru.cache_info()}")
