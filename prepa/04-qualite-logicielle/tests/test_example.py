"""
Tests d'exemple
===============

Démontre l'utilisation des fixtures de conftest.py.

Exécution :
    pytest tests/ -v
"""

import pytest


class TestDatabaseFixture:
    """Tests utilisant les fixtures de conftest.py."""

    def test_database_is_connected(self, database):
        """La fixture database connecte automatiquement."""
        assert database.connected is True

    def test_add_user(self, database, sample_user):
        """Ajouter un utilisateur."""
        database.add_user(sample_user)
        assert database.count() == 1

    def test_get_user(self, database, sample_user):
        """Récupérer un utilisateur."""
        database.add_user(sample_user)
        user = database.get_user(1)
        assert user.name == "Alice"

    def test_populated_database(self, populated_database):
        """Utiliser la base pré-remplie."""
        assert populated_database.count() == 2


class TestSampleUser:
    """Tests sur la fixture sample_user."""

    def test_sample_user_has_name(self, sample_user):
        """L'utilisateur a un nom."""
        assert sample_user.name == "Alice"

    def test_sample_user_has_email(self, sample_user):
        """L'utilisateur a un email."""
        assert "@" in sample_user.email


@pytest.mark.parametrize("name, expected_length", [
    ("Alice", 5),
    ("Bob", 3),
    ("Charlie", 7),
])
def test_name_length(name, expected_length):
    """Test paramétré de longueur de nom."""
    assert len(name) == expected_length


@pytest.mark.slow
def test_slow_operation():
    """Test marqué comme lent."""
    import time
    time.sleep(0.1)
    assert True


@pytest.mark.integration
def test_integration_example(populated_database):
    """Test d'intégration."""
    # Simule un scénario complet
    from conftest import User
    new_user = User(id=3, name="Charlie", email="charlie@test.com")
    populated_database.add_user(new_user)
    assert populated_database.count() == 3
