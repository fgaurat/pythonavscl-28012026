"""
Mocking : Isolation des tests
=============================

Techniques de mocking avec unittest.mock et pytest-mock.

Exécution :
    pytest 08_mocking.py -v -s
"""

from unittest.mock import Mock, MagicMock, patch, call
from typing import Dict, Optional
import json

# =============================================================================
# CLASSES À TESTER
# =============================================================================


class APIClient:
    """Client API simulé."""

    def __init__(self, base_url: str):
        self.base_url = base_url

    def get(self, endpoint: str) -> Dict:
        """Fait une requête GET (simulation)."""
        # En production, utiliserait requests.get
        raise NotImplementedError("Requires network")

    def post(self, endpoint: str, data: Dict) -> Dict:
        """Fait une requête POST (simulation)."""
        raise NotImplementedError("Requires network")


class UserService:
    """Service utilisateur qui dépend de l'API."""

    def __init__(self, api_client: APIClient):
        self.api = api_client

    def get_user(self, user_id: int) -> Dict:
        """Récupère un utilisateur par ID."""
        return self.api.get(f"/users/{user_id}")

    def create_user(self, name: str, email: str) -> Dict:
        """Crée un nouvel utilisateur."""
        return self.api.post("/users", {"name": name, "email": email})

    def get_user_name(self, user_id: int) -> str:
        """Récupère juste le nom de l'utilisateur."""
        user = self.get_user(user_id)
        return user.get("name", "Unknown")


class EmailService:
    """Service d'envoi d'emails."""

    def send(self, to: str, subject: str, body: str) -> bool:
        """Envoie un email (simulation)."""
        raise NotImplementedError("Requires SMTP server")


class NotificationService:
    """Service de notifications combinant plusieurs services."""

    def __init__(self, user_service: UserService, email_service: EmailService):
        self.users = user_service
        self.email = email_service

    def notify_user(self, user_id: int, message: str) -> bool:
        """Notifie un utilisateur par email."""
        user = self.users.get_user(user_id)
        if not user:
            return False

        return self.email.send(
            to=user["email"],
            subject="Notification",
            body=message
        )


# =============================================================================
# DÉMONSTRATION
# =============================================================================


def run_demo():
    """Démonstration des techniques de mocking."""
    print("=" * 60)
    print("MOCKING : ISOLATION DES TESTS")
    print("=" * 60)

    # ==========================================================================
    print("\n" + "-" * 60)
    print("1. MOCK DE BASE")
    print("-" * 60)

    # Créer un mock simple
    mock = Mock()

    # Configurer le retour
    mock.return_value = 42
    print(f"    mock() = {mock()}")

    # Configurer un attribut
    mock.name = "test_mock"
    print(f"    mock.name = {mock.name}")

    # Méthode avec retour
    mock.method.return_value = "result"
    print(f"    mock.method() = {mock.method()}")

    # Appel avec arguments
    mock.method("arg1", key="value")

    # Vérifier les appels
    mock.method.assert_called()
    mock.method.assert_called_once()
    mock.method.assert_called_with("arg1", key="value")
    print("    Assertions d'appel : OK")

    # ==========================================================================
    print("\n" + "-" * 60)
    print("2. MAGICMOCK")
    print("-" * 60)

    # MagicMock supporte les méthodes magiques
    magic = MagicMock()

    # Configurer __len__
    magic.__len__.return_value = 5
    print(f"    len(magic) = {len(magic)}")

    # Configurer __getitem__
    magic.__getitem__.return_value = "item"
    print(f"    magic[0] = {magic[0]}")

    # Configurer __iter__
    magic.__iter__.return_value = iter([1, 2, 3])
    print(f"    list(magic) = {list(magic)}")

    # ==========================================================================
    print("\n" + "-" * 60)
    print("3. MOCKER UNE CLASSE/MÉTHODE")
    print("-" * 60)

    # Créer un mock de APIClient
    mock_api = Mock(spec=APIClient)
    mock_api.get.return_value = {"id": 1, "name": "Alice", "email": "alice@test.com"}

    # Utiliser le mock dans UserService
    service = UserService(mock_api)
    user = service.get_user(1)

    print(f"    user = {user}")
    print(f"    service.get_user_name(1) = {service.get_user_name(1)}")

    # Vérifier que l'API a été appelée correctement
    mock_api.get.assert_called_with("/users/1")
    print("    API appelée avec '/users/1' : OK")

    # ==========================================================================
    print("\n" + "-" * 60)
    print("4. PATCH : REMPLACER TEMPORAIREMENT")
    print("-" * 60)

    print("""
    # Patch remplace un objet dans un module spécifique

    # Méthode 1 : décorateur
    @patch("module.fonction")
    def test_avec_patch(mock_fonction):
        mock_fonction.return_value = "mocked"
        result = fonction()
        assert result == "mocked"

    # Méthode 2 : context manager
    def test_avec_context():
        with patch("module.fonction") as mock_fonction:
            mock_fonction.return_value = "mocked"
            result = fonction()
            assert result == "mocked"

    # IMPORTANT : Patcher là où c'est UTILISÉ, pas où c'est DÉFINI
    # Si mon_module fait : from requests import get
    # Patcher : @patch("mon_module.get")  # Correct
    # Pas : @patch("requests.get")  # Ne marchera pas !
    """)

    # ==========================================================================
    print("\n" + "-" * 60)
    print("5. SIDE_EFFECT")
    print("-" * 60)

    # side_effect avec une exception
    mock_api_error = Mock()
    mock_api_error.get.side_effect = ConnectionError("Network error")

    print("    side_effect avec exception :")
    try:
        mock_api_error.get("/test")
    except ConnectionError as e:
        print(f"      Exception levée : {e}")

    # side_effect avec une fonction
    def fake_get(endpoint):
        if "users" in endpoint:
            return {"id": 1, "name": "Alice"}
        return {"error": "Not found"}

    mock_api_func = Mock()
    mock_api_func.get.side_effect = fake_get

    print("\n    side_effect avec fonction :")
    print(f"      get('/users/1') = {mock_api_func.get('/users/1')}")
    print(f"      get('/other') = {mock_api_func.get('/other')}")

    # side_effect avec liste de valeurs (appels successifs)
    mock_counter = Mock()
    mock_counter.next.side_effect = [1, 2, 3, StopIteration("Fin")]

    print("\n    side_effect avec liste de valeurs :")
    print(f"      next() = {mock_counter.next()}")
    print(f"      next() = {mock_counter.next()}")
    print(f"      next() = {mock_counter.next()}")

    # ==========================================================================
    print("\n" + "-" * 60)
    print("6. VÉRIFICATION DES APPELS")
    print("-" * 60)

    mock_verify = Mock()

    # Plusieurs appels
    mock_verify.process("a")
    mock_verify.process("b")
    mock_verify.process("c")

    # Vérifications
    print(f"    call_count = {mock_verify.process.call_count}")
    print(f"    call_args_list = {mock_verify.process.call_args_list}")

    # Vérifier l'ordre des appels
    mock_verify.process.assert_has_calls([
        call("a"),
        call("b"),
        call("c"),
    ])
    print("    assert_has_calls : OK")

    # Dernier appel
    mock_verify.process.assert_called_with("c")
    print("    Dernier appel avec 'c' : OK")

    # ==========================================================================
    print("\n" + "-" * 60)
    print("7. EXEMPLE COMPLET : NOTIFICATION SERVICE")
    print("-" * 60)

    # Créer les mocks
    mock_api = Mock(spec=APIClient)
    mock_api.get.return_value = {
        "id": 1,
        "name": "Alice",
        "email": "alice@test.com"
    }

    mock_email = Mock(spec=EmailService)
    mock_email.send.return_value = True

    # Créer les services avec les mocks
    user_service = UserService(mock_api)
    notification_service = NotificationService(user_service, mock_email)

    # Tester la notification
    result = notification_service.notify_user(1, "Hello!")

    print(f"    Notification envoyée : {result}")

    # Vérifier les interactions
    mock_api.get.assert_called_once_with("/users/1")
    mock_email.send.assert_called_once_with(
        to="alice@test.com",
        subject="Notification",
        body="Hello!"
    )
    print("    Interactions vérifiées : OK")

    # ==========================================================================
    print("\n" + "-" * 60)
    print("8. PYTEST-MOCK (fixture mocker)")
    print("-" * 60)

    print("""
    # pip install pytest-mock

    def test_avec_mocker(mocker):
        '''La fixture mocker simplifie le mocking.'''

        # Patch automatiquement nettoyé après le test
        mock_get = mocker.patch("requests.get")
        mock_get.return_value.json.return_value = {"status": "ok"}

        result = fetch_data()
        assert result["status"] == "ok"

    def test_spy(mocker):
        '''Spy : observer sans remplacer le comportement.'''
        spy = mocker.spy(ma_classe, "ma_methode")

        ma_classe.ma_methode("arg")

        spy.assert_called_once_with("arg")
    """)

    print("\n" + "=" * 60)
    print("BONNES PRATIQUES")
    print("=" * 60)

    print("""
1. PATCHER AU BON ENDROIT
   - Patcher là où l'objet est UTILISÉ, pas où il est DÉFINI
   - @patch("mon_module.requests") si mon_module importe requests

2. UTILISER spec=
   - Mock(spec=MaClasse) vérifie que les méthodes existent
   - Évite les fautes de frappe

3. VÉRIFIER LES INTERACTIONS
   - assert_called_once() : appelé exactement une fois
   - assert_called_with(args) : appelé avec ces arguments
   - call_count : nombre d'appels

4. GARDER LES TESTS SIMPLES
   - Un test = un comportement
   - Ne pas sur-mocker

5. PRÉFÉRER L'INJECTION DE DÉPENDANCES
   - Plus facile à tester
   - Code plus découplé
    """)


# =============================================================================
# TESTS PYTEST
# =============================================================================

try:
    import pytest

    # -------------------------------------------------------------------------
    # Tests avec Mock
    # -------------------------------------------------------------------------

    def test_user_service_get_user():
        """Test UserService avec mock."""
        # Arrange
        mock_api = Mock(spec=APIClient)
        mock_api.get.return_value = {"id": 1, "name": "Alice"}
        service = UserService(mock_api)

        # Act
        user = service.get_user(1)

        # Assert
        assert user["name"] == "Alice"
        mock_api.get.assert_called_once_with("/users/1")

    def test_user_service_get_user_name():
        """Test get_user_name."""
        mock_api = Mock(spec=APIClient)
        mock_api.get.return_value = {"id": 1, "name": "Bob"}
        service = UserService(mock_api)

        name = service.get_user_name(1)

        assert name == "Bob"

    def test_user_service_create_user():
        """Test création d'utilisateur."""
        mock_api = Mock(spec=APIClient)
        mock_api.post.return_value = {"id": 1, "name": "Charlie", "email": "c@test.com"}
        service = UserService(mock_api)

        user = service.create_user("Charlie", "c@test.com")

        assert user["name"] == "Charlie"
        mock_api.post.assert_called_once_with(
            "/users",
            {"name": "Charlie", "email": "c@test.com"}
        )

    # -------------------------------------------------------------------------
    # Tests avec side_effect
    # -------------------------------------------------------------------------

    def test_api_error_handling():
        """Test gestion d'erreur API."""
        mock_api = Mock(spec=APIClient)
        mock_api.get.side_effect = ConnectionError("Network error")
        service = UserService(mock_api)

        with pytest.raises(ConnectionError):
            service.get_user(1)

    def test_multiple_api_calls():
        """Test avec appels successifs différents."""
        mock_api = Mock(spec=APIClient)
        mock_api.get.side_effect = [
            {"id": 1, "name": "User1"},
            {"id": 2, "name": "User2"},
        ]
        service = UserService(mock_api)

        user1 = service.get_user(1)
        user2 = service.get_user(2)

        assert user1["name"] == "User1"
        assert user2["name"] == "User2"
        assert mock_api.get.call_count == 2

    # -------------------------------------------------------------------------
    # Tests NotificationService
    # -------------------------------------------------------------------------

    def test_notification_service_success():
        """Test notification réussie."""
        # Arrange
        mock_api = Mock(spec=APIClient)
        mock_api.get.return_value = {"id": 1, "email": "test@test.com"}

        mock_email = Mock(spec=EmailService)
        mock_email.send.return_value = True

        user_service = UserService(mock_api)
        notif_service = NotificationService(user_service, mock_email)

        # Act
        result = notif_service.notify_user(1, "Hello!")

        # Assert
        assert result is True
        mock_email.send.assert_called_once_with(
            to="test@test.com",
            subject="Notification",
            body="Hello!"
        )

    def test_notification_service_user_not_found():
        """Test notification échoue si utilisateur non trouvé."""
        mock_api = Mock(spec=APIClient)
        mock_api.get.return_value = None  # Utilisateur non trouvé

        mock_email = Mock(spec=EmailService)

        user_service = UserService(mock_api)
        notif_service = NotificationService(user_service, mock_email)

        result = notif_service.notify_user(999, "Hello!")

        assert result is False
        mock_email.send.assert_not_called()

    # -------------------------------------------------------------------------
    # Tests avec patch
    # -------------------------------------------------------------------------

    @patch.object(APIClient, 'get')
    def test_with_patch_object(mock_get):
        """Test avec patch.object."""
        mock_get.return_value = {"id": 1, "name": "Patched"}

        api = APIClient("http://api.test")
        result = api.get("/users/1")

        assert result["name"] == "Patched"

    def test_with_patch_context_manager():
        """Test avec patch comme context manager."""
        with patch.object(APIClient, 'get') as mock_get:
            mock_get.return_value = {"id": 1, "name": "Context"}

            api = APIClient("http://api.test")
            result = api.get("/users/1")

            assert result["name"] == "Context"

except ImportError:
    pass


if __name__ == "__main__":
    run_demo()
