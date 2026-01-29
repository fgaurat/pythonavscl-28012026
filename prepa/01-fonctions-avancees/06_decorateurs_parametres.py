"""
Décorateurs avec paramètres
===========================

Décorateurs acceptant des arguments et décorateurs polyvalents.
"""

from functools import wraps

# =============================================================================
# 1. Structure à trois niveaux
# =============================================================================

print("=" * 60)
print("1. DÉCORATEUR AVEC PARAMÈTRES")
print("=" * 60)


def repeter(fois):
    """Décorateur qui répète l'appel n fois."""
    def decorateur(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            resultat = None
            for i in range(fois):
                print(f"  Exécution {i + 1}/{fois}")
                resultat = func(*args, **kwargs)
            return resultat
        return wrapper
    return decorateur


@repeter(fois=3)
def saluer(nom):
    print(f"    Bonjour, {nom} !")


print("saluer('Alice') avec @repeter(fois=3) :")
saluer("Alice")


# =============================================================================
# 2. Explication du flux d'exécution
# =============================================================================

print("\n" + "=" * 60)
print("2. FLUX D'EXÉCUTION")
print("=" * 60)

print("""
@repeter(fois=3)
def saluer(nom):
    ...

Équivaut à :
1. repeter(fois=3) retourne `decorateur`
2. decorateur(saluer) retourne `wrapper`
3. saluer pointe maintenant vers `wrapper`

Schéma des niveaux :
┌─────────────────────────────────────────────────────┐
│ repeter(fois=3)     → Niveau 1 : paramètres         │
│     ↓                                               │
│ decorateur(func)    → Niveau 2 : fonction à décorer │
│     ↓                                               │
│ wrapper(*args)      → Niveau 3 : remplacement       │
└─────────────────────────────────────────────────────┘
""")


# =============================================================================
# 3. Décorateur de délai
# =============================================================================

print("=" * 60)
print("3. DÉCORATEUR DE DÉLAI")
print("=" * 60)

import time


def delay(seconds):
    """Ajoute un délai avant l'exécution."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            print(f"  Attente de {seconds}s...")
            time.sleep(seconds)
            return func(*args, **kwargs)
        return wrapper
    return decorator


@delay(seconds=0.5)
def action_lente():
    print("  Action exécutée !")
    return "OK"


print("action_lente() avec @delay(seconds=0.5) :")
resultat = action_lente()
print(f"  Résultat : {resultat}")


# =============================================================================
# 4. Décorateur polyvalent (avec ou sans paramètres)
# =============================================================================

print("\n" + "=" * 60)
print("4. DÉCORATEUR POLYVALENT")
print("=" * 60)


def log(func=None, *, niveau="INFO"):
    """Décorateur utilisable avec ou sans arguments."""
    def decorateur(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            print(f"  [{niveau}] Appel de {fn.__name__}")
            return fn(*args, **kwargs)
        return wrapper

    if func is not None:
        # Appelé sans parenthèses : @log
        return decorateur(func)
    # Appelé avec parenthèses : @log() ou @log(niveau="DEBUG")
    return decorateur


@log
def fonction_a():
    """Fonction sans paramètres de décorateur."""
    print("    Exécution de fonction_a")


@log()
def fonction_b():
    """Fonction avec parenthèses vides."""
    print("    Exécution de fonction_b")


@log(niveau="DEBUG")
def fonction_c():
    """Fonction avec niveau personnalisé."""
    print("    Exécution de fonction_c")


@log(niveau="ERROR")
def fonction_d():
    """Fonction avec niveau ERROR."""
    print("    Exécution de fonction_d")


print("@log (sans parenthèses) :")
fonction_a()

print("\n@log() (avec parenthèses) :")
fonction_b()

print("\n@log(niveau='DEBUG') :")
fonction_c()

print("\n@log(niveau='ERROR') :")
fonction_d()


# =============================================================================
# 5. Décorateur de retry avec paramètres
# =============================================================================

print("\n" + "=" * 60)
print("5. DÉCORATEUR DE RETRY")
print("=" * 60)

import random


def retry(max_attempts=3, delay=0.1, exceptions=(Exception,)):
    """Réessaie une fonction en cas d'échec."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None

            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    last_exception = e
                    print(f"  Tentative {attempt}/{max_attempts} échouée: {e}")
                    if attempt < max_attempts:
                        time.sleep(delay)

            raise last_exception
        return wrapper
    return decorator


@retry(max_attempts=5, delay=0.1, exceptions=(ConnectionError,))
def appel_api_instable():
    """Simule un appel API qui échoue parfois."""
    if random.random() < 0.7:
        raise ConnectionError("Échec connexion")
    return "Succès !"


print("appel_api_instable() avec @retry(max_attempts=5) :")
try:
    resultat = appel_api_instable()
    print(f"  Résultat final : {resultat}")
except ConnectionError as e:
    print(f"  Échec définitif : {e}")


# =============================================================================
# 6. Décorateur de cache avec TTL
# =============================================================================

print("\n" + "=" * 60)
print("6. DÉCORATEUR DE CACHE AVEC TTL")
print("=" * 60)

from datetime import datetime, timedelta


def cache_with_ttl(ttl_seconds=60):
    """Cache avec expiration temporelle."""
    def decorator(func):
        cache = {}

        @wraps(func)
        def wrapper(*args):
            now = datetime.now()

            if args in cache:
                result, timestamp = cache[args]
                if now - timestamp < timedelta(seconds=ttl_seconds):
                    print(f"  Cache hit pour {args}")
                    return result

            print(f"  Cache miss pour {args}")
            result = func(*args)
            cache[args] = (result, now)
            return result

        wrapper.clear_cache = lambda: cache.clear()
        wrapper.cache_info = lambda: dict(cache)
        return wrapper
    return decorator


@cache_with_ttl(ttl_seconds=2)
def calcul_couteux(n):
    """Simule un calcul coûteux."""
    time.sleep(0.1)  # Simulation
    return n ** 2


print("Premiers appels (cache miss) :")
print(f"  calcul_couteux(5) = {calcul_couteux(5)}")
print(f"  calcul_couteux(10) = {calcul_couteux(10)}")

print("\nAppels suivants (cache hit) :")
print(f"  calcul_couteux(5) = {calcul_couteux(5)}")
print(f"  calcul_couteux(10) = {calcul_couteux(10)}")

print("\nAttente de 2.5s pour expiration...")
time.sleep(2.5)

print("\nAprès expiration (cache miss) :")
print(f"  calcul_couteux(5) = {calcul_couteux(5)}")
