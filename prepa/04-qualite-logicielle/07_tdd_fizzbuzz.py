"""
TDD : Test-Driven Development
==============================

Exemple pratique du cycle Red-Green-Refactor avec FizzBuzz.

Exécution :
    pytest 07_tdd_fizzbuzz.py -v
"""

# =============================================================================
# TDD : LE CYCLE RED-GREEN-REFACTOR
# =============================================================================

"""
Le TDD suit un cycle strict en 3 étapes :

┌─────────────────────────────────────────────────────────────┐
│                                                             │
│    1. RED           2. GREEN          3. REFACTOR          │
│    ┌─────┐          ┌─────┐           ┌─────────┐          │
│    │Écrire│    →    │Faire │    →     │Améliorer│          │
│    │ test │         │passer│          │le code  │          │
│    │  ❌  │         │  ✅  │          │   ✨    │          │
│    └─────┘          └─────┘           └─────────┘          │
│        ↑                                  │                │
│        └──────────────────────────────────┘                │
│                                                             │
└─────────────────────────────────────────────────────────────┘

RÈGLES DU TDD :
1. N'écrire du code de production que pour faire passer un test qui échoue
2. N'écrire que le minimum de test pour échouer
3. N'écrire que le minimum de code pour passer le test
"""


# =============================================================================
# SPÉCIFICATION FIZZBUZZ
# =============================================================================

"""
Spécification : fonction fizzbuzz(n)

- Retourne "Fizz" si n est divisible par 3
- Retourne "Buzz" si n est divisible par 5
- Retourne "FizzBuzz" si divisible par 3 ET 5
- Sinon retourne le nombre en string

Exemples :
- fizzbuzz(1) → "1"
- fizzbuzz(3) → "Fizz"
- fizzbuzz(5) → "Buzz"
- fizzbuzz(15) → "FizzBuzz"
"""


# =============================================================================
# DÉMONSTRATION DU CYCLE TDD
# =============================================================================


def run_demo():
    """Démonstration du cycle TDD."""
    print("=" * 60)
    print("TDD : TEST-DRIVEN DEVELOPMENT")
    print("=" * 60)

    # ==========================================================================
    print("\n" + "-" * 60)
    print("ÉTAPE 1 : RED - Premier test (échoue)")
    print("-" * 60)

    print("""
# tests/test_fizzbuzz.py

def test_retourne_1_pour_1():
    assert fizzbuzz(1) == "1"

# $ pytest
# NameError: name 'fizzbuzz' is not defined
# ❌ Test échoue (RED)
""")

    # ==========================================================================
    print("\n" + "-" * 60)
    print("ÉTAPE 2 : GREEN - Code minimal")
    print("-" * 60)

    print("""
# src/fizzbuzz.py

def fizzbuzz(n):
    return str(n)

# $ pytest
# ✅ Test passe (GREEN)
""")

    # Démonstration
    def fizzbuzz_v1(n):
        return str(n)

    print(f"    fizzbuzz_v1(1) = '{fizzbuzz_v1(1)}'")
    print(f"    fizzbuzz_v1(2) = '{fizzbuzz_v1(2)}'")

    # ==========================================================================
    print("\n" + "-" * 60)
    print("ÉTAPE 3 : RED - Nouveau test pour Fizz")
    print("-" * 60)

    print("""
def test_retourne_fizz_pour_3():
    assert fizzbuzz(3) == "Fizz"

# $ pytest
# AssertionError: assert '3' == 'Fizz'
# ❌ Test échoue (RED)
""")

    # ==========================================================================
    print("\n" + "-" * 60)
    print("ÉTAPE 4 : GREEN - Ajouter la logique Fizz")
    print("-" * 60)

    print("""
def fizzbuzz(n):
    if n % 3 == 0:
        return "Fizz"
    return str(n)

# $ pytest
# ✅ Tous les tests passent (GREEN)
""")

    # Démonstration
    def fizzbuzz_v2(n):
        if n % 3 == 0:
            return "Fizz"
        return str(n)

    print(f"    fizzbuzz_v2(1) = '{fizzbuzz_v2(1)}'")
    print(f"    fizzbuzz_v2(3) = '{fizzbuzz_v2(3)}'")
    print(f"    fizzbuzz_v2(6) = '{fizzbuzz_v2(6)}'")

    # ==========================================================================
    print("\n" + "-" * 60)
    print("ÉTAPE 5 : RED - Test pour Buzz")
    print("-" * 60)

    print("""
def test_retourne_buzz_pour_5():
    assert fizzbuzz(5) == "Buzz"

# $ pytest
# AssertionError: assert '5' == 'Buzz'
# ❌ Test échoue (RED)
""")

    # ==========================================================================
    print("\n" + "-" * 60)
    print("ÉTAPE 6 : GREEN - Ajouter la logique Buzz")
    print("-" * 60)

    print("""
def fizzbuzz(n):
    if n % 3 == 0:
        return "Fizz"
    if n % 5 == 0:
        return "Buzz"
    return str(n)

# $ pytest
# ✅ Tous les tests passent (GREEN)
""")

    # Démonstration
    def fizzbuzz_v3(n):
        if n % 3 == 0:
            return "Fizz"
        if n % 5 == 0:
            return "Buzz"
        return str(n)

    print(f"    fizzbuzz_v3(1) = '{fizzbuzz_v3(1)}'")
    print(f"    fizzbuzz_v3(3) = '{fizzbuzz_v3(3)}'")
    print(f"    fizzbuzz_v3(5) = '{fizzbuzz_v3(5)}'")

    # ==========================================================================
    print("\n" + "-" * 60)
    print("ÉTAPE 7 : RED - Test pour FizzBuzz")
    print("-" * 60)

    print("""
def test_retourne_fizzbuzz_pour_15():
    assert fizzbuzz(15) == "FizzBuzz"

# $ pytest
# AssertionError: assert 'Fizz' == 'FizzBuzz'
# ❌ Test échoue (RED)
#
# Note : 15 % 3 == 0, donc on retourne "Fizz" avant de tester % 5
""")

    # ==========================================================================
    print("\n" + "-" * 60)
    print("ÉTAPE 8 : GREEN - Logique FizzBuzz")
    print("-" * 60)

    print("""
def fizzbuzz(n):
    if n % 3 == 0 and n % 5 == 0:
        return "FizzBuzz"
    if n % 3 == 0:
        return "Fizz"
    if n % 5 == 0:
        return "Buzz"
    return str(n)

# $ pytest
# ✅ Tous les tests passent (GREEN)
""")

    # Démonstration
    def fizzbuzz_v4(n):
        if n % 3 == 0 and n % 5 == 0:
            return "FizzBuzz"
        if n % 3 == 0:
            return "Fizz"
        if n % 5 == 0:
            return "Buzz"
        return str(n)

    print(f"    fizzbuzz_v4(15) = '{fizzbuzz_v4(15)}'")
    print(f"    fizzbuzz_v4(30) = '{fizzbuzz_v4(30)}'")

    # ==========================================================================
    print("\n" + "-" * 60)
    print("ÉTAPE 9 : REFACTOR - Amélioration du code")
    print("-" * 60)

    print("""
# Le code fonctionne, mais on peut l'améliorer

def fizzbuzz(n: int) -> str:
    '''
    Retourne FizzBuzz selon les règles classiques.

    Args:
        n: Un entier positif

    Returns:
        "Fizz", "Buzz", "FizzBuzz" ou le nombre en string
    '''
    result = ""

    if n % 3 == 0:
        result += "Fizz"
    if n % 5 == 0:
        result += "Buzz"

    return result or str(n)

# $ pytest
# ✅ Tous les tests passent encore (REFACTOR réussi)
""")

    # ==========================================================================
    print("\n" + "-" * 60)
    print("SOLUTION FINALE")
    print("-" * 60)

    print("    Version finale avec tests complets :\n")

    # Tests avec la version finale
    for n in [1, 2, 3, 4, 5, 6, 10, 15, 20, 30]:
        result = fizzbuzz(n)
        print(f"      fizzbuzz({n:2d}) = '{result}'")

    # ==========================================================================
    print("\n" + "-" * 60)
    print("AVANTAGES DU TDD")
    print("-" * 60)

    print("""
1. CODE TESTABLE PAR CONCEPTION
   - Le code est écrit pour être testé
   - Design découplé et modulaire

2. DOCUMENTATION VIVANTE
   - Les tests documentent le comportement attendu
   - Toujours à jour avec le code

3. CONFIANCE POUR LE REFACTORING
   - On peut améliorer le code en toute sécurité
   - Les tests garantissent le comportement

4. DÉTECTION PRÉCOCE DES BUGS
   - Bugs trouvés immédiatement
   - Moins coûteux à corriger

5. MEILLEURE CONCEPTION
   - Force à réfléchir à l'API avant l'implémentation
   - Résulte en un code plus propre
""")


# =============================================================================
# IMPLÉMENTATION FINALE
# =============================================================================


def fizzbuzz(n: int) -> str:
    """
    Retourne FizzBuzz selon les règles classiques.

    Args:
        n: Un entier positif

    Returns:
        "Fizz" si n est divisible par 3
        "Buzz" si n est divisible par 5
        "FizzBuzz" si divisible par 3 et 5
        Le nombre en string sinon
    """
    result = ""

    if n % 3 == 0:
        result += "Fizz"
    if n % 5 == 0:
        result += "Buzz"

    return result or str(n)


# =============================================================================
# TESTS PYTEST
# =============================================================================

try:
    import pytest

    # Tests individuels (comme dans le TDD)
    def test_retourne_1_pour_1():
        """Premier test TDD."""
        assert fizzbuzz(1) == "1"

    def test_retourne_2_pour_2():
        """Test pour nombres non divisibles."""
        assert fizzbuzz(2) == "2"

    def test_retourne_fizz_pour_3():
        """Test pour divisible par 3."""
        assert fizzbuzz(3) == "Fizz"

    def test_retourne_fizz_pour_6():
        """Test pour autre multiple de 3."""
        assert fizzbuzz(6) == "Fizz"

    def test_retourne_buzz_pour_5():
        """Test pour divisible par 5."""
        assert fizzbuzz(5) == "Buzz"

    def test_retourne_buzz_pour_10():
        """Test pour autre multiple de 5."""
        assert fizzbuzz(10) == "Buzz"

    def test_retourne_fizzbuzz_pour_15():
        """Test pour divisible par 3 et 5."""
        assert fizzbuzz(15) == "FizzBuzz"

    def test_retourne_fizzbuzz_pour_30():
        """Test pour autre multiple de 15."""
        assert fizzbuzz(30) == "FizzBuzz"

    # Tests paramétrés (après TDD, pour consolidation)
    @pytest.mark.parametrize("n, expected", [
        (1, "1"),
        (2, "2"),
        (3, "Fizz"),
        (4, "4"),
        (5, "Buzz"),
        (6, "Fizz"),
        (7, "7"),
        (8, "8"),
        (9, "Fizz"),
        (10, "Buzz"),
        (11, "11"),
        (12, "Fizz"),
        (13, "13"),
        (14, "14"),
        (15, "FizzBuzz"),
        (30, "FizzBuzz"),
        (45, "FizzBuzz"),
    ])
    def test_fizzbuzz_comprehensive(n, expected):
        """Test complet paramétré."""
        assert fizzbuzz(n) == expected

    # Test de propriétés
    @pytest.mark.parametrize("n", range(1, 101))
    def test_fizzbuzz_retourne_toujours_string(n):
        """Propriété : retourne toujours une string."""
        result = fizzbuzz(n)
        assert isinstance(result, str)
        assert len(result) > 0

    def test_fizzbuzz_multiples_de_3_contiennent_fizz():
        """Propriété : multiples de 3 contiennent 'Fizz'."""
        for n in range(3, 100, 3):
            assert "Fizz" in fizzbuzz(n)

    def test_fizzbuzz_multiples_de_5_contiennent_buzz():
        """Propriété : multiples de 5 contiennent 'Buzz'."""
        for n in range(5, 100, 5):
            assert "Buzz" in fizzbuzz(n)

except ImportError:
    pass


if __name__ == "__main__":
    run_demo()
