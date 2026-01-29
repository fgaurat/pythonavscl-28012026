"""
unittest : Module standard de tests
===================================

Structure de base et assertions du module unittest.
"""

import unittest
from typing import List

# =============================================================================
# CLASSE À TESTER
# =============================================================================


class Calculatrice:
    """Calculatrice simple pour démonstration."""

    def add(self, a: float, b: float) -> float:
        """Addition de deux nombres."""
        return a + b

    def subtract(self, a: float, b: float) -> float:
        """Soustraction de deux nombres."""
        return a - b

    def multiply(self, a: float, b: float) -> float:
        """Multiplication de deux nombres."""
        return a * b

    def divide(self, a: float, b: float) -> float:
        """Division de deux nombres."""
        if b == 0:
            raise ZeroDivisionError("Division par zéro impossible")
        return a / b

    def moyenne(self, nombres: List[float]) -> float:
        """Calcule la moyenne d'une liste."""
        if not nombres:
            raise ValueError("La liste ne peut pas être vide")
        return sum(nombres) / len(nombres)


# =============================================================================
# TESTS AVEC UNITTEST
# =============================================================================


class TestCalculatriceBase(unittest.TestCase):
    """Tests de base pour la calculatrice."""

    def setUp(self):
        """Exécuté AVANT chaque test."""
        print(f"\n  [setUp] Création de la calculatrice")
        self.calc = Calculatrice()

    def tearDown(self):
        """Exécuté APRÈS chaque test."""
        print(f"  [tearDown] Nettoyage")
        self.calc = None

    def test_addition_positive(self):
        """Test de l'addition avec nombres positifs."""
        resultat = self.calc.add(2, 3)
        self.assertEqual(resultat, 5)
        print(f"  test_addition_positive: 2 + 3 = {resultat}")

    def test_addition_negative(self):
        """Test de l'addition avec nombres négatifs."""
        resultat = self.calc.add(-1, -1)
        self.assertEqual(resultat, -2)
        print(f"  test_addition_negative: -1 + -1 = {resultat}")

    def test_soustraction(self):
        """Test de la soustraction."""
        resultat = self.calc.subtract(10, 4)
        self.assertEqual(resultat, 6)
        print(f"  test_soustraction: 10 - 4 = {resultat}")

    def test_multiplication(self):
        """Test de la multiplication."""
        resultat = self.calc.multiply(3, 4)
        self.assertEqual(resultat, 12)
        print(f"  test_multiplication: 3 * 4 = {resultat}")


class TestCalculatriceDivision(unittest.TestCase):
    """Tests de la division et des erreurs."""

    def setUp(self):
        self.calc = Calculatrice()

    def test_division_normale(self):
        """Test de la division normale."""
        resultat = self.calc.divide(10, 2)
        self.assertEqual(resultat, 5)

    def test_division_par_zero(self):
        """Test de la division par zéro."""
        # assertRaises vérifie qu'une exception est levée
        with self.assertRaises(ZeroDivisionError):
            self.calc.divide(10, 0)

    def test_division_message_erreur(self):
        """Test du message d'erreur de la division."""
        with self.assertRaises(ZeroDivisionError) as context:
            self.calc.divide(10, 0)
        self.assertIn("Division par zéro", str(context.exception))


class TestCalculatriceMoyenne(unittest.TestCase):
    """Tests de la fonction moyenne."""

    def setUp(self):
        self.calc = Calculatrice()

    def test_moyenne_normale(self):
        """Test de la moyenne avec des valeurs normales."""
        resultat = self.calc.moyenne([1, 2, 3, 4, 5])
        self.assertEqual(resultat, 3.0)

    def test_moyenne_un_element(self):
        """Test de la moyenne avec un seul élément."""
        resultat = self.calc.moyenne([42])
        self.assertEqual(resultat, 42)

    def test_moyenne_liste_vide(self):
        """Test de la moyenne avec liste vide."""
        with self.assertRaises(ValueError):
            self.calc.moyenne([])


class TestAssertionsVariees(unittest.TestCase):
    """Démonstration des différentes assertions disponibles."""

    def test_egalite(self):
        """Assertions d'égalité."""
        self.assertEqual(1 + 1, 2)        # a == b
        self.assertNotEqual(1 + 1, 3)     # a != b

    def test_verite(self):
        """Assertions de vérité."""
        self.assertTrue(1 < 2)            # bool(x) is True
        self.assertFalse(1 > 2)           # bool(x) is False

    def test_none(self):
        """Assertions sur None."""
        valeur = None
        self.assertIsNone(valeur)         # x is None
        self.assertIsNotNone("hello")     # x is not None

    def test_identite(self):
        """Assertions d'identité."""
        a = [1, 2, 3]
        b = a  # même objet
        c = [1, 2, 3]  # objet différent avec même valeur

        self.assertIs(a, b)               # a is b
        self.assertIsNot(a, c)            # a is not c

    def test_appartenance(self):
        """Assertions d'appartenance."""
        liste = [1, 2, 3]
        self.assertIn(2, liste)           # a in b
        self.assertNotIn(5, liste)        # a not in b

    def test_type(self):
        """Assertions de type."""
        self.assertIsInstance(42, int)    # isinstance(a, type)
        self.assertIsInstance("hello", str)

    def test_comparaison(self):
        """Assertions de comparaison."""
        self.assertGreater(5, 3)          # a > b
        self.assertGreaterEqual(5, 5)     # a >= b
        self.assertLess(3, 5)             # a < b
        self.assertLessEqual(3, 3)        # a <= b

    def test_floats(self):
        """Comparaison de nombres flottants."""
        # Les floats ont des erreurs d'arrondi
        resultat = 0.1 + 0.2
        # self.assertEqual(resultat, 0.3)  # Peut échouer !
        self.assertAlmostEqual(resultat, 0.3, places=7)

    def test_sequences(self):
        """Assertions sur les séquences."""
        self.assertListEqual([1, 2, 3], [1, 2, 3])
        self.assertTupleEqual((1, 2), (1, 2))
        self.assertDictEqual({"a": 1}, {"a": 1})
        self.assertSetEqual({1, 2, 3}, {3, 2, 1})

    def test_regex(self):
        """Assertions avec expressions régulières."""
        import re
        self.assertRegex("hello world", r"hello.*")
        self.assertNotRegex("hello world", r"^world")


class TestAvecSetUpClass(unittest.TestCase):
    """Démonstration de setUpClass et tearDownClass."""

    @classmethod
    def setUpClass(cls):
        """Exécuté UNE FOIS avant tous les tests de la classe."""
        print("\n  [setUpClass] Initialisation unique (ex: connexion DB)")
        cls.shared_resource = "ressource partagée"

    @classmethod
    def tearDownClass(cls):
        """Exécuté UNE FOIS après tous les tests de la classe."""
        print("  [tearDownClass] Nettoyage final (ex: fermeture DB)")
        cls.shared_resource = None

    def test_utilise_ressource_1(self):
        """Premier test utilisant la ressource partagée."""
        self.assertIsNotNone(self.shared_resource)

    def test_utilise_ressource_2(self):
        """Deuxième test utilisant la même ressource."""
        self.assertEqual(self.shared_resource, "ressource partagée")


class TestSkipEtExpectedFailure(unittest.TestCase):
    """Démonstration de skip et expectedFailure."""

    @unittest.skip("Pas encore implémenté")
    def test_fonctionnalite_future(self):
        """Ce test sera ignoré."""
        pass

    @unittest.skipIf(True, "Condition vraie, test ignoré")
    def test_conditionnel(self):
        """Ce test est ignoré conditionnellement."""
        pass

    @unittest.skipUnless(False, "Condition fausse, test ignoré")
    def test_conditionnel_inverse(self):
        """Ce test est ignoré sauf si condition vraie."""
        pass

    @unittest.expectedFailure
    def test_bug_connu(self):
        """Ce test échoue de manière attendue (bug connu)."""
        self.assertEqual(1, 2)  # Échec attendu


# =============================================================================
# EXÉCUTION DES TESTS
# =============================================================================


def run_demo():
    """Exécute une démonstration des tests."""
    print("=" * 60)
    print("DÉMONSTRATION UNITTEST")
    print("=" * 60)

    print("\n--- Structure d'un test unittest ---")
    print("""
    class TestMaClasse(unittest.TestCase):

        def setUp(self):
            # Exécuté avant chaque test
            pass

        def tearDown(self):
            # Exécuté après chaque test
            pass

        def test_quelque_chose(self):
            # Le test proprement dit
            self.assertEqual(resultat, attendu)
    """)

    print("--- Exécution des tests ---\n")

    # Créer une suite de tests limitée pour la démo
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # Ajouter seulement quelques tests pour la démonstration
    suite.addTests(loader.loadTestsFromTestCase(TestCalculatriceBase))

    # Exécuter avec un runner verbose
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)

    print("\n" + "=" * 60)
    print("ASSERTIONS DISPONIBLES")
    print("=" * 60)

    print("""
    assertEqual(a, b)          # a == b
    assertNotEqual(a, b)       # a != b
    assertTrue(x)              # bool(x) is True
    assertFalse(x)             # bool(x) is False
    assertIsNone(x)            # x is None
    assertIsNotNone(x)         # x is not None
    assertIs(a, b)             # a is b
    assertIsNot(a, b)          # a is not b
    assertIn(a, b)             # a in b
    assertNotIn(a, b)          # a not in b
    assertIsInstance(a, type)  # isinstance(a, type)
    assertRaises(Exception)    # Vérifie qu'une exception est levée
    assertAlmostEqual(a, b)    # Pour les floats
    """)

    print("\n--- Pour exécuter tous les tests ---")
    print("  python -m unittest 03_unittest_base.py")
    print("  python -m unittest discover -v")


if __name__ == "__main__":
    run_demo()
