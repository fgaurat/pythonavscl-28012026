"""
pytest : Framework de tests moderne
===================================

Syntaxe de base, assertions et fonctionnalités.

Exécution :
    pytest 04_pytest_base.py -v
    pytest 04_pytest_base.py::test_addition -v
"""

from typing import List

# =============================================================================
# CLASSES À TESTER
# =============================================================================


class Calculatrice:
    """Calculatrice pour démonstration."""

    def add(self, a: float, b: float) -> float:
        return a + b

    def divide(self, a: float, b: float) -> float:
        if b == 0:
            raise ZeroDivisionError("Division par zéro")
        return a / b


def valider_age(age: int) -> int:
    """Valide que l'âge est positif."""
    if age < 0:
        raise ValueError("L'âge doit être positif")
    if age > 150:
        raise ValueError("L'âge doit être inférieur à 150")
    return age


def traiter_liste(items: List[int]) -> List[int]:
    """Double chaque élément de la liste."""
    return [x * 2 for x in items]


# =============================================================================
# TESTS PYTEST : SYNTAXE DE BASE
# =============================================================================

# Avec pytest, pas besoin de classe, juste des fonctions test_*


def test_addition():
    """Test simple avec assert natif."""
    calc = Calculatrice()
    assert calc.add(2, 3) == 5


def test_addition_negatifs():
    """Test avec nombres négatifs."""
    calc = Calculatrice()
    assert calc.add(-1, -1) == -2


def test_addition_floats():
    """Test avec nombres flottants."""
    calc = Calculatrice()
    # pytest gère la comparaison de floats intelligemment
    assert calc.add(0.1, 0.2) == pytest.approx(0.3)


def test_division():
    """Test de la division."""
    calc = Calculatrice()
    assert calc.divide(10, 2) == 5


def test_division_par_zero():
    """Test d'exception avec pytest.raises."""
    import pytest

    calc = Calculatrice()
    with pytest.raises(ZeroDivisionError):
        calc.divide(10, 0)


def test_division_message_erreur():
    """Vérifier le message d'erreur."""
    import pytest

    calc = Calculatrice()
    with pytest.raises(ZeroDivisionError, match="Division par zéro"):
        calc.divide(10, 0)


def test_valider_age_valide():
    """Test d'un âge valide."""
    assert valider_age(25) == 25


def test_valider_age_negatif():
    """Test d'un âge négatif."""
    import pytest

    with pytest.raises(ValueError, match="positif"):
        valider_age(-5)


def test_valider_age_trop_grand():
    """Test d'un âge trop grand."""
    import pytest

    with pytest.raises(ValueError, match="inférieur à 150"):
        valider_age(200)


def test_traiter_liste():
    """Test du traitement de liste."""
    resultat = traiter_liste([1, 2, 3])
    assert resultat == [2, 4, 6]


def test_traiter_liste_vide():
    """Test avec liste vide."""
    assert traiter_liste([]) == []


# =============================================================================
# DÉMONSTRATION DES MESSAGES D'ERREUR
# =============================================================================


def test_comparaison_liste():
    """
    Décommentez ce test pour voir les messages d'erreur détaillés de pytest.
    """
    attendu = [1, 2, 3, 4, 5]
    obtenu = [1, 2, 3, 4, 5]  # Changez pour voir l'erreur
    assert attendu == obtenu


def test_comparaison_dict():
    """Test de comparaison de dictionnaires."""
    attendu = {"name": "Alice", "age": 30}
    obtenu = {"name": "Alice", "age": 30}  # Changez pour voir l'erreur
    assert attendu == obtenu


# =============================================================================
# TESTS AVEC CLASSES (optionnel avec pytest)
# =============================================================================


class TestCalculatrice:
    """Groupe de tests dans une classe (optionnel)."""

    def setup_method(self):
        """Équivalent de setUp, exécuté avant chaque test."""
        self.calc = Calculatrice()

    def teardown_method(self):
        """Équivalent de tearDown, exécuté après chaque test."""
        self.calc = None

    def test_add(self):
        assert self.calc.add(1, 1) == 2

    def test_divide(self):
        assert self.calc.divide(10, 5) == 2


# =============================================================================
# EXÉCUTION DÉMONSTRATIVE
# =============================================================================


def run_demo():
    """Exécute une démonstration de pytest."""
    print("=" * 60)
    print("DÉMONSTRATION PYTEST")
    print("=" * 60)

    print("""
AVANTAGES DE PYTEST :

1. Syntaxe simple : pas besoin de classes
   def test_addition():
       assert 1 + 1 == 2

2. Assertions natives Python
   assert resultat == attendu
   assert item in liste
   assert expression

3. Messages d'erreur détaillés
   pytest montre exactement où et pourquoi le test échoue

4. pytest.raises pour les exceptions
   with pytest.raises(ValueError):
       fonction_qui_leve()

5. pytest.approx pour les floats
   assert 0.1 + 0.2 == pytest.approx(0.3)
""")

    print("=" * 60)
    print("COMMANDES UTILES")
    print("=" * 60)

    print("""
# Exécuter tous les tests
pytest

# Verbose
pytest -v

# Un fichier spécifique
pytest 04_pytest_base.py

# Un test spécifique
pytest 04_pytest_base.py::test_addition

# Tests dont le nom contient "add"
pytest -k "add"

# Stopper au premier échec
pytest -x

# Voir les prints
pytest -s

# Avec couverture
pytest --cov=.
""")

    print("=" * 60)
    print("EXÉCUTION DES TESTS")
    print("=" * 60)

    # Exécution avec pytest (si disponible)
    try:
        import pytest
        print("\npytest est installé. Exécution des tests...\n")
        # Exécuter les tests de ce fichier
        pytest.main([__file__, "-v", "--tb=short"])
    except ImportError:
        print("\npytest n'est pas installé.")
        print("Installation : pip install pytest")
        print("\nExécution manuelle des tests...")

        # Exécution manuelle des tests
        calc = Calculatrice()

        tests = [
            ("test_addition", calc.add(2, 3) == 5),
            ("test_addition_negatifs", calc.add(-1, -1) == -2),
            ("test_division", calc.divide(10, 2) == 5),
            ("test_traiter_liste", traiter_liste([1, 2, 3]) == [2, 4, 6]),
        ]

        for name, passed in tests:
            status = "PASSED" if passed else "FAILED"
            print(f"  {name}: {status}")


# Import pytest pour les tests (avec fallback)
try:
    import pytest
except ImportError:
    # Créer un mock minimal pour que le fichier reste exécutable
    class MockPytest:
        @staticmethod
        def approx(val, rel=None, abs=None):
            return val

        @staticmethod
        def raises(exc, match=None):
            import contextlib

            @contextlib.contextmanager
            def raises_context():
                try:
                    yield
                except exc:
                    pass
                else:
                    raise AssertionError(f"Expected {exc}")
            return raises_context()

        @staticmethod
        def main(args):
            print("pytest not installed")

    pytest = MockPytest()


if __name__ == "__main__":
    run_demo()
