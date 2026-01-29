"""
pytest : Paramétrisation et marqueurs
=====================================

Tests paramétrés et marqueurs pour organiser les tests.

Exécution :
    pytest 06_pytest_parametrize.py -v
    pytest 06_pytest_parametrize.py -m "not slow"
    pytest 06_pytest_parametrize.py -m "integration"
"""

import sys
import time
from typing import List

# =============================================================================
# FONCTIONS À TESTER
# =============================================================================


def fizzbuzz(n: int) -> str:
    """Retourne FizzBuzz selon les règles classiques."""
    result = ""
    if n % 3 == 0:
        result += "Fizz"
    if n % 5 == 0:
        result += "Buzz"
    return result or str(n)


def is_palindrome(s: str) -> bool:
    """Vérifie si une chaîne est un palindrome."""
    s = s.lower().replace(" ", "")
    return s == s[::-1]


def factoriel(n: int) -> int:
    """Calcule le factoriel de n."""
    if n < 0:
        raise ValueError("n doit être positif")
    if n <= 1:
        return 1
    return n * factoriel(n - 1)


def trier_liste(items: List[int]) -> List[int]:
    """Trie une liste de nombres."""
    return sorted(items)


def operation_lente() -> str:
    """Simule une opération lente."""
    time.sleep(0.5)  # Réduit pour la démo
    return "done"


# =============================================================================
# DÉMONSTRATION
# =============================================================================


def run_demo():
    """Démonstration des fonctionnalités pytest."""
    print("=" * 60)
    print("PYTEST : PARAMÉTRISATION ET MARQUEURS")
    print("=" * 60)

    # ==========================================================================
    print("\n" + "-" * 60)
    print("1. PARAMÉTRISATION (@pytest.mark.parametrize)")
    print("-" * 60)

    print("""
# Tester plusieurs cas avec un seul test

@pytest.mark.parametrize("a, b, expected", [
    (2, 3, 5),
    (0, 0, 0),
    (-1, 1, 0),
    (100, 200, 300),
])
def test_addition(a, b, expected):
    assert a + b == expected

# Sortie :
# test_calc.py::test_addition[2-3-5] PASSED
# test_calc.py::test_addition[0-0-0] PASSED
# test_calc.py::test_addition[-1-1-0] PASSED
# test_calc.py::test_addition[100-200-300] PASSED
""")

    # Démonstration FizzBuzz
    print("    Démonstration FizzBuzz :")
    test_cases = [(1, "1"), (3, "Fizz"), (5, "Buzz"), (15, "FizzBuzz")]
    for n, expected in test_cases:
        result = fizzbuzz(n)
        status = "OK" if result == expected else "FAIL"
        print(f"      fizzbuzz({n}) = {result} (attendu: {expected}) [{status}]")

    # ==========================================================================
    print("\n" + "-" * 60)
    print("2. PARAMÉTRISATION AVEC IDS")
    print("-" * 60)

    print("""
# IDs personnalisés pour une meilleure lisibilité

@pytest.mark.parametrize("input_str, expected", [
    pytest.param("kayak", True, id="simple_palindrome"),
    pytest.param("A man a plan a canal Panama", True, id="phrase_with_spaces"),
    pytest.param("hello", False, id="not_palindrome"),
    pytest.param("", True, id="empty_string"),
], ids=["simple", "phrase", "not_palindrome", "empty"])
def test_is_palindrome(input_str, expected):
    assert is_palindrome(input_str) == expected
""")

    # Démonstration
    print("    Démonstration Palindrome :")
    palindrome_cases = [
        ("kayak", True, "simple_palindrome"),
        ("A man a plan a canal Panama", True, "phrase_with_spaces"),
        ("hello", False, "not_palindrome"),
    ]
    for text, expected, case_id in palindrome_cases:
        result = is_palindrome(text)
        status = "OK" if result == expected else "FAIL"
        print(f"      {case_id}: is_palindrome('{text[:15]}...') = {result} [{status}]")

    # ==========================================================================
    print("\n" + "-" * 60)
    print("3. MARQUEURS (@pytest.mark)")
    print("-" * 60)

    print("""
# Marqueurs pour organiser et filtrer les tests

@pytest.mark.slow
def test_operation_lente():
    '''Ce test prend du temps.'''
    assert operation_lente() == "done"

@pytest.mark.skip(reason="Pas encore implémenté")
def test_fonctionnalite_future():
    pass

@pytest.mark.skipif(sys.platform == "win32", reason="Unix only")
def test_unix_specific():
    pass

@pytest.mark.xfail(reason="Bug connu #123")
def test_avec_bug_connu():
    assert False  # Attendu comme échec

# Exécution sélective :
# pytest -m "not slow"       # Exclure les tests lents
# pytest -m "slow"           # Seulement les tests lents
# pytest -m "slow or fast"   # Tests slow OU fast
""")

    # ==========================================================================
    print("\n" + "-" * 60)
    print("4. MARQUEURS PERSONNALISÉS")
    print("-" * 60)

    print("""
# Dans pytest.ini ou pyproject.toml :

[tool.pytest.ini_options]
markers = [
    "slow: marks tests as slow (deselect with '-m not slow')",
    "integration: marks tests as integration tests",
    "unit: marks tests as unit tests",
    "database: marks tests that require database",
]

# Utilisation :
@pytest.mark.integration
@pytest.mark.database
def test_database_connection():
    pass

# Exécuter uniquement les tests d'intégration :
# pytest -m "integration"
""")

    # ==========================================================================
    print("\n" + "-" * 60)
    print("5. COMBINAISON PARAMÉTRISATION + FIXTURES")
    print("-" * 60)

    print("""
@pytest.fixture
def calculator():
    return Calculator()

@pytest.mark.parametrize("a, b, expected", [
    (1, 1, 2),
    (2, 3, 5),
])
def test_addition(calculator, a, b, expected):
    # La fixture est injectée, les paramètres viennent de parametrize
    assert calculator.add(a, b) == expected
""")

    # ==========================================================================
    print("\n" + "-" * 60)
    print("6. PARAMÉTRISATION MULTIPLE")
    print("-" * 60)

    print("""
# Produit cartésien des paramètres

@pytest.mark.parametrize("a", [1, 2])
@pytest.mark.parametrize("b", [10, 20])
def test_multiplication(a, b):
    result = a * b
    assert result == a * b

# Génère 4 tests :
# test_multiplication[10-1], test_multiplication[10-2]
# test_multiplication[20-1], test_multiplication[20-2]
""")

    # Démonstration
    print("    Démonstration produit cartésien :")
    for a in [1, 2]:
        for b in [10, 20]:
            print(f"      {a} * {b} = {a * b}")

    # ==========================================================================
    print("\n" + "-" * 60)
    print("7. EXPECTED FAILURES ET SKIP CONDITIONNELS")
    print("-" * 60)

    print("""
import sys

@pytest.mark.xfail(reason="Bug connu, sera corrigé en v2.0")
def test_bug_connu():
    assert buggy_function() == expected  # Échec attendu

@pytest.mark.xfail(strict=True)  # Doit échouer, sinon le test échoue
def test_doit_echouer():
    assert False

@pytest.mark.skipif(
    sys.version_info < (3, 10),
    reason="Requires Python 3.10+"
)
def test_python_310_feature():
    # Utilise match statement (Python 3.10+)
    pass

@pytest.mark.skipif(
    sys.platform != "linux",
    reason="Linux only"
)
def test_linux_specific():
    pass
""")

    # ==========================================================================
    print("\n" + "-" * 60)
    print("8. FILTRAGE PAR NOM DE TEST")
    print("-" * 60)

    print("""
# pytest -k pour filtrer par nom

pytest -k "test_add"              # Tests contenant "add"
pytest -k "not slow"              # Tests ne contenant pas "slow"
pytest -k "add or subtract"       # Tests contenant "add" OU "subtract"
pytest -k "test_calc and not div" # Combinaisons

# Exemples :
# pytest -k "parametrize"    # Ce fichier uniquement les tests paramétrés
# pytest -k "fizzbuzz"       # Tests FizzBuzz
""")

    print("\n" + "=" * 60)
    print("COMMANDES UTILES")
    print("=" * 60)
    print("""
# Exécuter avec marqueurs
pytest -m "slow"                # Seulement les tests marqués slow
pytest -m "not slow"            # Exclure les tests slow
pytest -m "unit and not slow"   # Tests unit sans slow

# Exécuter avec filtrage par nom
pytest -k "test_fizz"           # Tests contenant "fizz"

# Voir les marqueurs disponibles
pytest --markers

# Mode verbose avec sortie
pytest -v -s
""")


# =============================================================================
# TESTS PYTEST
# =============================================================================

try:
    import pytest

    # -------------------------------------------------------------------------
    # Tests paramétrés FizzBuzz
    # -------------------------------------------------------------------------

    @pytest.mark.parametrize("n, expected", [
        (1, "1"),
        (2, "2"),
        (3, "Fizz"),
        (4, "4"),
        (5, "Buzz"),
        (6, "Fizz"),
        (10, "Buzz"),
        (15, "FizzBuzz"),
        (30, "FizzBuzz"),
    ])
    def test_fizzbuzz(n, expected):
        """Test paramétré de FizzBuzz."""
        assert fizzbuzz(n) == expected

    # -------------------------------------------------------------------------
    # Tests paramétrés avec IDs
    # -------------------------------------------------------------------------

    @pytest.mark.parametrize("text, expected", [
        pytest.param("kayak", True, id="simple"),
        pytest.param("A man a plan a canal Panama", True, id="phrase"),
        pytest.param("hello", False, id="not_palindrome"),
        pytest.param("", True, id="empty"),
        pytest.param("a", True, id="single_char"),
    ])
    def test_is_palindrome(text, expected):
        """Test paramétré de palindrome."""
        assert is_palindrome(text) == expected

    # -------------------------------------------------------------------------
    # Tests paramétrés factoriel
    # -------------------------------------------------------------------------

    @pytest.mark.parametrize("n, expected", [
        (0, 1),
        (1, 1),
        (5, 120),
        (10, 3628800),
    ])
    def test_factoriel(n, expected):
        """Test paramétré de factoriel."""
        assert factoriel(n) == expected

    def test_factoriel_negatif():
        """Test d'erreur pour factoriel négatif."""
        with pytest.raises(ValueError, match="positif"):
            factoriel(-1)

    # -------------------------------------------------------------------------
    # Marqueurs
    # -------------------------------------------------------------------------

    @pytest.mark.slow
    def test_operation_lente():
        """Test marqué comme lent."""
        assert operation_lente() == "done"

    @pytest.mark.skip(reason="Fonctionnalité non implémentée")
    def test_feature_future():
        """Test ignoré."""
        pass

    @pytest.mark.skipif(sys.version_info < (3, 9), reason="Python 3.9+ requis")
    def test_python39_feature():
        """Test conditionnel sur version Python."""
        # list[int] syntax works in 3.9+
        items: list[int] = [1, 2, 3]
        assert len(items) == 3

    @pytest.mark.xfail(reason="Bug connu dans le tri")
    def test_tri_bug_connu():
        """Test avec échec attendu."""
        # Ce test est marqué comme devant échouer
        assert trier_liste([3, 1, 2]) == [1, 2, 3]  # Passe en fait !

    # -------------------------------------------------------------------------
    # Paramétrisation multiple (produit cartésien)
    # -------------------------------------------------------------------------

    @pytest.mark.parametrize("a", [1, 2, 3])
    @pytest.mark.parametrize("b", [10, 100])
    def test_multiplication_cartesian(a, b):
        """Test avec produit cartésien des paramètres."""
        result = a * b
        assert result == a * b
        assert result > 0

    # -------------------------------------------------------------------------
    # Marqueurs personnalisés
    # -------------------------------------------------------------------------

    @pytest.mark.unit
    def test_unit_simple():
        """Test unitaire simple."""
        assert 1 + 1 == 2

    @pytest.mark.integration
    def test_integration_simple():
        """Test d'intégration simple."""
        # Simule un test d'intégration
        result = trier_liste([5, 3, 1, 4, 2])
        assert result == [1, 2, 3, 4, 5]

except ImportError:
    pass


if __name__ == "__main__":
    run_demo()
