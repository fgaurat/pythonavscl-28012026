"""
Profiling et mesure de performance
==================================

Outils de profiling : timeit, cProfile, memory_profiler.
"""

import timeit
import time
import cProfile
import pstats
import io
import sys
from functools import wraps, lru_cache
from typing import List

# =============================================================================
# 1. Mesure de temps avec timeit
# =============================================================================

print("=" * 60)
print("1. MESURE DE TEMPS AVEC TIMEIT")
print("=" * 60)

# timeit.timeit pour mesurer des expressions


# Comparaison de deux approches pour créer une liste de carrés
setup = "data = list(range(1000))"

# Approche 1 : List comprehension
temps_comprehension = timeit.timeit(
    "[x**2 for x in data]",
    setup=setup,
    number=10000
)

# Approche 2 : map + lambda
temps_map = timeit.timeit(
    "list(map(lambda x: x**2, data))",
    setup=setup,
    number=10000
)

print(f"  List comprehension : {temps_comprehension:.4f}s")
print(f"  map + lambda       : {temps_map:.4f}s")
print(f"  Ratio              : {temps_map/temps_comprehension:.2f}x")


# timeit pour mesurer une fonction
def sum_squares(n):
    """Calcule la somme des carrés de 1 à n."""
    return sum(i ** 2 for i in range(n))


temps_fonction = timeit.timeit(lambda: sum_squares(1000), number=1000)
print(f"\n  sum_squares(1000) x 1000 : {temps_fonction:.4f}s")
print(f"  Temps moyen par appel    : {temps_fonction / 1000 * 1000:.4f}ms")


# =============================================================================
# 2. Décorateur de mesure de temps
# =============================================================================

print("\n" + "=" * 60)
print("2. DÉCORATEUR DE MESURE DE TEMPS")
print("=" * 60)


def timer(func):
    """Décorateur pour mesurer le temps d'exécution."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        end = time.perf_counter()
        duration = (end - start) * 1000
        print(f"  {func.__name__}: {duration:.2f}ms")
        return result
    return wrapper


@timer
def calcul_lourd(n):
    """Calcul avec simulation de charge."""
    return sum(i ** 2 for i in range(n))


@timer
def tri_liste(n):
    """Tri d'une grande liste."""
    import random
    data = [random.randint(0, n) for _ in range(n)]
    return sorted(data)


print("  Exemples de mesure :")
calcul_lourd(100_000)
tri_liste(10_000)


# =============================================================================
# 3. cProfile : profiler Python
# =============================================================================

print("\n" + "=" * 60)
print("3. CPROFILE : PROFILER PYTHON")
print("=" * 60)


def fonction_a_profiler():
    """Fonction complexe à profiler."""
    # Étape 1 : création de données
    data = [i ** 2 for i in range(10000)]

    # Étape 2 : filtrage
    filtered = [x for x in data if x % 2 == 0]

    # Étape 3 : tri
    sorted_data = sorted(filtered, reverse=True)

    # Étape 4 : agrégation
    result = sum(sorted_data[:100])

    return result


# Profiler avec cProfile
print("  Profiling de 'fonction_a_profiler' :")
print()

# Capturer la sortie du profiler
profiler = cProfile.Profile()
profiler.enable()

# Exécuter la fonction
for _ in range(100):
    fonction_a_profiler()

profiler.disable()

# Afficher les statistiques
stream = io.StringIO()
stats = pstats.Stats(profiler, stream=stream)
stats.sort_stats('cumulative')
stats.print_stats(10)

# Afficher un résumé
output = stream.getvalue()
lines = output.split('\n')
for line in lines[:15]:  # Limiter la sortie
    print(f"  {line}")


# =============================================================================
# 4. Comparaison d'algorithmes
# =============================================================================

print("\n" + "=" * 60)
print("4. COMPARAISON D'ALGORITHMES")
print("=" * 60)


def recherche_lineaire(items: List[int], target: int) -> int:
    """Recherche linéaire O(n)."""
    for i, item in enumerate(items):
        if item == target:
            return i
    return -1


def recherche_binaire(items: List[int], target: int) -> int:
    """Recherche binaire O(log n) - liste triée requise."""
    left, right = 0, len(items) - 1
    while left <= right:
        mid = (left + right) // 2
        if items[mid] == target:
            return mid
        elif items[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1


# Comparer les performances
n = 100_000
data = list(range(n))
target = n - 1  # Pire cas pour recherche linéaire

temps_lineaire = timeit.timeit(
    lambda: recherche_lineaire(data, target),
    number=100
)

temps_binaire = timeit.timeit(
    lambda: recherche_binaire(data, target),
    number=100
)

print(f"  Recherche dans {n:,} éléments :")
print(f"  Linéaire O(n)    : {temps_lineaire:.4f}s")
print(f"  Binaire O(log n) : {temps_binaire:.6f}s")
print(f"  Ratio            : {temps_lineaire/temps_binaire:.0f}x plus rapide")


# =============================================================================
# 5. Structures de données : performances
# =============================================================================

print("\n" + "=" * 60)
print("5. STRUCTURES DE DONNÉES : PERFORMANCES")
print("=" * 60)

n = 10_000
test_list = list(range(n))
test_set = set(range(n))
test_dict = {i: i for i in range(n)}

# Recherche dans liste vs set vs dict
target = n // 2

temps_list = timeit.timeit(lambda: target in test_list, number=10000)
temps_set = timeit.timeit(lambda: target in test_set, number=10000)
temps_dict = timeit.timeit(lambda: target in test_dict, number=10000)

print(f"  Recherche 'in' ({n:,} éléments, 10000 itérations) :")
print(f"  list : {temps_list:.4f}s (O(n))")
print(f"  set  : {temps_set:.4f}s (O(1))")
print(f"  dict : {temps_dict:.4f}s (O(1))")

print(f"\n  Tableau des complexités :")
print("""
  | Opération        | list   | set    | dict   |
  |------------------|--------|--------|--------|
  | Recherche `in`   | O(n)   | O(1)   | O(1)   |
  | Ajout            | O(1)*  | O(1)   | O(1)   |
  | Suppression      | O(n)   | O(1)   | O(1)   |
  | Accès par index  | O(1)   | N/A    | O(1)   |

  * O(n) dans le pire cas si redimensionnement
""")


# =============================================================================
# 6. Mémoïsation avec lru_cache
# =============================================================================

print("\n" + "=" * 60)
print("6. MÉMOÏSATION AVEC LRU_CACHE")
print("=" * 60)


def fibonacci_slow(n):
    """Fibonacci sans cache (exponentiel)."""
    if n < 2:
        return n
    return fibonacci_slow(n - 1) + fibonacci_slow(n - 2)


@lru_cache(maxsize=128)
def fibonacci_fast(n):
    """Fibonacci avec cache (linéaire)."""
    if n < 2:
        return n
    return fibonacci_fast(n - 1) + fibonacci_fast(n - 2)


# Comparer les performances
print("  Fibonacci(30) :")

start = time.perf_counter()
result_slow = fibonacci_slow(30)
temps_slow = time.perf_counter() - start
print(f"  Sans cache : {temps_slow:.4f}s (résultat: {result_slow})")

start = time.perf_counter()
result_fast = fibonacci_fast(30)
temps_fast = time.perf_counter() - start
print(f"  Avec cache : {temps_fast:.6f}s (résultat: {result_fast})")

if temps_fast > 0:
    print(f"  Ratio      : {temps_slow/temps_fast:.0f}x plus rapide")

# Stats du cache
print(f"\n  Cache stats : {fibonacci_fast.cache_info()}")


# =============================================================================
# 7. Optimisation des strings
# =============================================================================

print("\n" + "=" * 60)
print("7. OPTIMISATION DES STRINGS")
print("=" * 60)

n = 10000
strings = [f"item_{i}" for i in range(n)]


# Mauvaise pratique : concaténation en boucle
def concat_mauvais(items):
    result = ""
    for s in items:
        result += s + ", "  # Crée une nouvelle string à chaque itération
    return result[:-2]


# Bonne pratique : join()
def concat_bon(items):
    return ", ".join(items)


temps_mauvais = timeit.timeit(lambda: concat_mauvais(strings), number=100)
temps_bon = timeit.timeit(lambda: concat_bon(strings), number=100)

print(f"  Concaténation de {n:,} strings (100 itérations) :")
print(f"  += en boucle : {temps_mauvais:.4f}s")
print(f"  join()       : {temps_bon:.4f}s")
print(f"  Ratio        : {temps_mauvais/temps_bon:.0f}x plus rapide")


# =============================================================================
# 8. Générateurs vs listes
# =============================================================================

print("\n" + "=" * 60)
print("8. GÉNÉRATEURS VS LISTES (MÉMOIRE)")
print("=" * 60)


def carres_liste(n):
    """Retourne une liste de carrés."""
    return [i ** 2 for i in range(n)]


def carres_gen(n):
    """Retourne un générateur de carrés."""
    for i in range(n):
        yield i ** 2


n = 1_000_000

# Mesure mémoire approximative
liste = carres_liste(n)
gen = carres_gen(n)

print(f"  Génération de {n:,} carrés :")
print(f"  Liste      : {sys.getsizeof(liste) / 1024 / 1024:.1f} MB")
print(f"  Générateur : {sys.getsizeof(gen)} bytes")

# Nettoyage
del liste


# =============================================================================
# 9. memory_profiler (démonstration conceptuelle)
# =============================================================================

print("\n" + "=" * 60)
print("9. MEMORY_PROFILER")
print("=" * 60)

print("""
  Installation : pip install memory_profiler

  Utilisation :

  from memory_profiler import profile

  @profile
  def fonction_gourmande():
      # Cette ligne alloue ~76 MB
      big_list = [i for i in range(10_000_000)]

      # Cette ligne alloue ~76 MB supplémentaires
      big_list_2 = big_list.copy()

      del big_list  # Libère ~76 MB
      return big_list_2

  Sortie :

  Line #    Mem usage    Increment   Line Contents
       4     38.5 MiB     38.5 MiB   @profile
       5                             def fonction_gourmande():
       6    114.9 MiB     76.4 MiB       big_list = [i for i in range(10_000_000)]
       7    191.3 MiB     76.4 MiB       big_list_2 = big_list.copy()
       8    114.9 MiB    -76.4 MiB       del big_list
""")


# =============================================================================
# 10. Bonnes pratiques d'optimisation
# =============================================================================

print("\n" + "=" * 60)
print("10. BONNES PRATIQUES D'OPTIMISATION")
print("=" * 60)

print("""
1. MESURER AVANT D'OPTIMISER
   - Identifier le vrai goulot d'étranglement
   - "Premature optimization is the root of all evil" - Knuth

2. CHOISIR LES BONNES STRUCTURES DE DONNÉES
   - set/dict pour recherche O(1)
   - list pour accès indexé O(1)
   - deque pour ajouts/suppressions aux extrémités O(1)

3. ÉVITER LES COPIES INUTILES
   - Utiliser join() pour les strings
   - Utiliser des générateurs pour les grands volumes

4. UTILISER LE CACHING
   - @lru_cache pour les fonctions pures coûteuses
   - functools.cache (Python 3.9+) pour cache illimité

5. PROFILER EN CONDITIONS RÉELLES
   - Les micro-benchmarks peuvent être trompeurs
   - Tester avec des données représentatives

6. PRÉFÉRER LES BUILT-INS
   - sum(), max(), min(), sorted() sont optimisés en C
   - Éviter de réimplémenter ce qui existe

7. COMPLEXITÉ ALGORITHMIQUE PRIME
   - Un O(n) bien écrit bat un O(n²) optimisé
   - Connaître les complexités des opérations de base
""")


# =============================================================================
# RÉSUMÉ DES OUTILS
# =============================================================================

print("\n" + "=" * 60)
print("RÉSUMÉ DES OUTILS DE PROFILING")
print("=" * 60)

print("""
| Outil              | Usage                           | Commande              |
|--------------------|--------------------------------|-----------------------|
| timeit             | Micro-benchmarks               | timeit.timeit(...)    |
| time.perf_counter  | Mesure précise                 | start = perf_counter()|
| cProfile           | Profiling CPU                  | python -m cProfile    |
| pstats             | Analyse résultats cProfile     | stats.print_stats()   |
| snakeviz           | Visualisation cProfile         | snakeviz output.prof  |
| memory_profiler    | Profiling mémoire              | @profile              |
| line_profiler      | Profiling ligne par ligne      | @profile              |
| py-spy             | Sampling profiler (production) | py-spy top --pid PID  |
""")

print("\n--- Fin des exemples de profiling ---")
