"""
conftest.py - Configuration partagée pour pytest
=================================================

Ce fichier est automatiquement découvert par pytest.
Les fixtures définies ici sont disponibles dans tous les tests.
"""

import pytest
from dataclasses import dataclass
from typing import Dict, List

# =============================================================================
# FIXTURES PARTAGÉES
# =============================================================================


@dataclass
class User:
    """Utilisateur de test."""
    id: int
    name: str
    email: str


class Database:
    """Base de données simulée."""

    def __init__(self):
        self.users: Dict[int, User] = {}
        self.connected = False

    def connect(self):
        self.connected = True

    def disconnect(self):
        self.connected = False

    def add_user(self, user: User) -> User:
        self.users[user.id] = user
        return user

    def get_user(self, user_id: int) -> User:
        return self.users.get(user_id)

    def count(self) -> int:
        return len(self.users)


@pytest.fixture
def sample_user() -> User:
    """Fixture retournant un utilisateur exemple."""
    return User(id=1, name="Alice", email="alice@test.com")


@pytest.fixture
def database() -> Database:
    """Fixture base de données avec setup/teardown."""
    db = Database()
    db.connect()
    yield db
    db.disconnect()


@pytest.fixture
def populated_database(database, sample_user) -> Database:
    """Base de données avec des données initiales."""
    database.add_user(sample_user)
    database.add_user(User(id=2, name="Bob", email="bob@test.com"))
    return database


# =============================================================================
# CONFIGURATION PYTEST
# =============================================================================


def pytest_configure(config):
    """Configuration additionnelle de pytest."""
    config.addinivalue_line(
        "markers", "slow: marks tests as slow (deselect with '-m not slow')"
    )
    config.addinivalue_line(
        "markers", "integration: marks tests as integration tests"
    )


def pytest_collection_modifyitems(config, items):
    """Modifier la collection de tests (ex: ajouter des marqueurs automatiques)."""
    for item in items:
        # Marquer automatiquement les tests dans test_integration_*
        if "integration" in item.nodeid:
            item.add_marker(pytest.mark.integration)
