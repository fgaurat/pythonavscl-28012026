"""
pytest : Fixtures
==================

Injection de dépendances et gestion des ressources.

Exécution :
    pytest 05_pytest_fixtures.py -v -s
"""

from typing import List, Dict
from dataclasses import dataclass, field
from datetime import datetime

# =============================================================================
# CLASSES À TESTER
# =============================================================================


@dataclass
class User:
    """Utilisateur simple."""
    id: int
    name: str
    email: str
    created_at: datetime = field(default_factory=datetime.now)


class Database:
    """Simule une base de données."""

    def __init__(self, name: str = ":memory:"):
        self.name = name
        self.connected = False
        self.users: Dict[int, User] = {}
        print(f"    [DB] Création de la base '{name}'")

    def connect(self):
        """Connecte à la base."""
        self.connected = True
        print(f"    [DB] Connexion à '{self.name}'")

    def disconnect(self):
        """Déconnecte de la base."""
        self.connected = False
        print(f"    [DB] Déconnexion de '{self.name}'")

    def add_user(self, user: User):
        """Ajoute un utilisateur."""
        if not self.connected:
            raise RuntimeError("Base non connectée")
        self.users[user.id] = user
        return user

    def get_user(self, user_id: int) -> User:
        """Récupère un utilisateur."""
        if not self.connected:
            raise RuntimeError("Base non connectée")
        return self.users.get(user_id)

    def count_users(self) -> int:
        """Compte les utilisateurs."""
        return len(self.users)


class UserService:
    """Service métier pour les utilisateurs."""

    def __init__(self, database: Database):
        self.db = database

    def create_user(self, name: str, email: str) -> User:
        """Crée un nouvel utilisateur."""
        user_id = len(self.db.users) + 1
        user = User(id=user_id, name=name, email=email)
        return self.db.add_user(user)

    def get_user_by_id(self, user_id: int) -> User:
        """Récupère un utilisateur par ID."""
        return self.db.get_user(user_id)


# =============================================================================
# DÉMONSTRATION SANS PYTEST (pour exécution directe)
# =============================================================================


def run_demo():
    """Démonstration des concepts de fixtures."""
    print("=" * 60)
    print("DÉMONSTRATION DES FIXTURES PYTEST")
    print("=" * 60)

    print("""
Les fixtures pytest permettent :
- Injecter des dépendances dans les tests
- Gérer le setup/teardown de manière élégante
- Partager des ressources entre tests
- Paramétrer les tests avec différentes configurations
""")

    # ==========================================================================
    print("\n" + "-" * 60)
    print("1. FIXTURE SIMPLE")
    print("-" * 60)

    print("""
@pytest.fixture
def calculatrice():
    '''Retourne une instance de Calculatrice.'''
    return Calculatrice()

def test_addition(calculatrice):  # Injection automatique
    assert calculatrice.add(2, 3) == 5
""")

    # Démonstration
    class Calculatrice:
        def add(self, a, b):
            return a + b

    calc = Calculatrice()
    print(f"    Résultat : calc.add(2, 3) = {calc.add(2, 3)}")

    # ==========================================================================
    print("\n" + "-" * 60)
    print("2. FIXTURE AVEC SETUP ET TEARDOWN (yield)")
    print("-" * 60)

    print("""
@pytest.fixture
def database():
    '''Fixture avec setup et teardown.'''
    # Setup
    db = Database(":memory:")
    db.connect()

    yield db  # Le test s'exécute ici

    # Teardown (exécuté même si le test échoue)
    db.disconnect()
""")

    # Démonstration
    print("\n    Simulation :")
    db = Database(":memory:")
    db.connect()
    db.add_user(User(1, "Alice", "alice@test.com"))
    print(f"    Users count : {db.count_users()}")
    db.disconnect()

    # ==========================================================================
    print("\n" + "-" * 60)
    print("3. SCOPE DES FIXTURES")
    print("-" * 60)

    print("""
@pytest.fixture(scope="function")  # Par défaut : nouveau pour chaque test
def fixture_par_test():
    return create_resource()

@pytest.fixture(scope="class")  # Une par classe de test
def fixture_par_classe():
    return create_expensive_resource()

@pytest.fixture(scope="module")  # Une par fichier de test
def fixture_par_module():
    return create_very_expensive_resource()

@pytest.fixture(scope="session")  # Une pour toute la session pytest
def fixture_session():
    return create_singleton_resource()
""")

    # ==========================================================================
    print("\n" + "-" * 60)
    print("4. FIXTURES AVEC DÉPENDANCES")
    print("-" * 60)

    print("""
@pytest.fixture
def database():
    db = Database()
    db.connect()
    yield db
    db.disconnect()

@pytest.fixture
def user_service(database):  # Dépend de database
    return UserService(database)

def test_create_user(user_service):  # Injecte automatiquement les deux
    user = user_service.create_user("Alice", "alice@test.com")
    assert user.name == "Alice"
""")

    # Démonstration
    print("\n    Simulation avec dépendances :")
    db = Database(":memory:")
    db.connect()
    service = UserService(db)
    user = service.create_user("Alice", "alice@test.com")
    print(f"    User créé : {user.name} ({user.email})")
    db.disconnect()

    # ==========================================================================
    print("\n" + "-" * 60)
    print("5. FIXTURES PARAMÉTRÉES")
    print("-" * 60)

    print("""
@pytest.fixture(params=["mysql", "postgresql", "sqlite"])
def database_type(request):
    '''Le test sera exécuté 3 fois, une fois par type.'''
    return request.param

def test_connection(database_type):
    print(f"Testing with {database_type}")
    assert database_type in ["mysql", "postgresql", "sqlite"]
""")

    # Démonstration
    print("\n    Simulation avec paramètres :")
    for db_type in ["mysql", "postgresql", "sqlite"]:
        print(f"    Test avec {db_type} : OK")

    # ==========================================================================
    print("\n" + "-" * 60)
    print("6. CONFTEST.PY : PARTAGER DES FIXTURES")
    print("-" * 60)

    print("""
# tests/conftest.py
# Ce fichier est automatiquement découvert par pytest

import pytest

@pytest.fixture
def app():
    '''Application Flask pour les tests.'''
    from mon_app import create_app
    app = create_app(testing=True)
    return app

@pytest.fixture
def client(app):
    '''Client de test.'''
    return app.test_client()

# Toutes les fixtures de conftest.py sont disponibles
# dans tous les fichiers de test du même répertoire et sous-répertoires
""")

    # ==========================================================================
    print("\n" + "-" * 60)
    print("7. AUTOUSE : FIXTURES AUTOMATIQUES")
    print("-" * 60)

    print("""
@pytest.fixture(autouse=True)
def setup_logging():
    '''Cette fixture est exécutée automatiquement pour chaque test.'''
    print("Setup logging...")
    yield
    print("Teardown logging...")

# Pas besoin de l'injecter, elle s'exécute automatiquement
def test_something():
    assert True
""")

    # ==========================================================================
    print("\n" + "-" * 60)
    print("8. FIXTURES INTÉGRÉES À PYTEST")
    print("-" * 60)

    print("""
Fixtures fournies par pytest :

- tmp_path : Répertoire temporaire unique (Path)
- tmp_path_factory : Factory pour créer des répertoires temporaires
- capsys : Capture stdout/stderr
- caplog : Capture les logs
- monkeypatch : Modifier temporairement des attributs
- request : Accès aux informations de la fixture

def test_avec_fichier_temp(tmp_path):
    fichier = tmp_path / "test.txt"
    fichier.write_text("hello")
    assert fichier.read_text() == "hello"

def test_capture_stdout(capsys):
    print("Hello")
    captured = capsys.readouterr()
    assert captured.out == "Hello\\n"
""")

    print("\n" + "=" * 60)
    print("POUR EXÉCUTER AVEC PYTEST")
    print("=" * 60)
    print("""
# Installer pytest
pip install pytest

# Exécuter ce fichier
pytest 05_pytest_fixtures.py -v -s
""")


# =============================================================================
# TESTS PYTEST (exécutés si pytest est disponible)
# =============================================================================

try:
    import pytest

    @pytest.fixture
    def database():
        """Fixture database avec setup/teardown."""
        db = Database(":memory:")
        db.connect()
        yield db
        db.disconnect()

    @pytest.fixture
    def user_service(database):
        """Service utilisateur (dépend de database)."""
        return UserService(database)

    @pytest.fixture
    def sample_user():
        """Utilisateur exemple."""
        return User(id=1, name="Alice", email="alice@test.com")

    def test_database_connection(database):
        """Test de connexion à la base."""
        assert database.connected is True

    def test_add_user(database, sample_user):
        """Test d'ajout d'utilisateur."""
        database.add_user(sample_user)
        assert database.count_users() == 1

    def test_get_user(database, sample_user):
        """Test de récupération d'utilisateur."""
        database.add_user(sample_user)
        user = database.get_user(1)
        assert user.name == "Alice"

    def test_user_service_create(user_service):
        """Test du service de création."""
        user = user_service.create_user("Bob", "bob@test.com")
        assert user.id == 1
        assert user.name == "Bob"

    def test_user_service_get(user_service):
        """Test du service de récupération."""
        user_service.create_user("Charlie", "charlie@test.com")
        user = user_service.get_user_by_id(1)
        assert user.name == "Charlie"

    # Fixture avec scope class
    @pytest.fixture(scope="class")
    def shared_database():
        """Base partagée entre tests de la classe."""
        db = Database("shared")
        db.connect()
        yield db
        db.disconnect()

    class TestWithSharedDatabase:
        """Tests partageant la même base de données."""

        def test_add_first_user(self, shared_database):
            shared_database.add_user(User(1, "User1", "user1@test.com"))
            assert shared_database.count_users() >= 1

        def test_add_second_user(self, shared_database):
            shared_database.add_user(User(2, "User2", "user2@test.com"))
            assert shared_database.count_users() >= 2

    # Fixture paramétrée
    @pytest.fixture(params=[1, 2, 3])
    def user_id(request):
        """IDs utilisateur pour tests paramétrés."""
        return request.param

    def test_with_parameterized_fixture(database, user_id):
        """Test exécuté 3 fois avec différents IDs."""
        user = User(id=user_id, name=f"User{user_id}", email=f"user{user_id}@test.com")
        database.add_user(user)
        assert database.get_user(user_id).id == user_id

except ImportError:
    pass


if __name__ == "__main__":
    run_demo()
