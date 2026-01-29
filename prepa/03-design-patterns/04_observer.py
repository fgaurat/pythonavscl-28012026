"""
Pattern Observer
================

Notifier automatiquement des objets quand un état change.
"""

from abc import ABC, abstractmethod
from typing import List, Callable

# =============================================================================
# 1. Observer classique avec ABC
# =============================================================================

print("=" * 60)
print("1. OBSERVER CLASSIQUE AVEC ABC")
print("=" * 60)


class Observer(ABC):
    @abstractmethod
    def update(self, subject, *args, **kwargs):
        pass


class Subject(ABC):
    def __init__(self):
        self._observers: List[Observer] = []

    def attach(self, observer: Observer):
        if observer not in self._observers:
            self._observers.append(observer)
            print(f"    Observer {observer.__class__.__name__} attaché")

    def detach(self, observer: Observer):
        self._observers.remove(observer)
        print(f"    Observer {observer.__class__.__name__} détaché")

    def notify(self, *args, **kwargs):
        for observer in self._observers:
            observer.update(self, *args, **kwargs)


# Implémentation concrète
class Stock(Subject):
    def __init__(self, symbol: str, price: float):
        super().__init__()
        self.symbol = symbol
        self._price = price

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value):
        old_price = self._price
        self._price = value
        self.notify(old_price=old_price, new_price=value)


class PriceAlert(Observer):
    def __init__(self, threshold: float):
        self.threshold = threshold

    def update(self, subject, **kwargs):
        new_price = kwargs.get("new_price", 0)
        if new_price > self.threshold:
            print(f"  ⚠️ ALERTE : {subject.symbol} dépasse {self.threshold}€ ! (actuel: {new_price}€)")


class PriceLogger(Observer):
    def update(self, subject, **kwargs):
        old = kwargs.get("old_price")
        new = kwargs.get("new_price")
        change = "📈" if new > old else "📉" if new < old else "➡️"
        print(f"  📝 LOG : {subject.symbol} {old}€ → {new}€ {change}")


# Utilisation
print("\nConfiguration :")
apple = Stock("AAPL", 150.0)
apple.attach(PriceAlert(threshold=160))
apple.attach(PriceLogger())

print("\nChangements de prix :")
apple.price = 155.0
apple.price = 165.0
apple.price = 158.0


# =============================================================================
# 2. Observer pythonique avec callbacks
# =============================================================================

print("\n" + "=" * 60)
print("2. OBSERVER PYTHONIQUE AVEC CALLBACKS")
print("=" * 60)


class StockPythonic:
    """Version pythonique avec liste de callbacks."""

    def __init__(self, symbol: str, price: float):
        self.symbol = symbol
        self._price = price
        self.on_price_change: List[Callable] = []

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value):
        old_price = self._price
        self._price = value
        for callback in self.on_price_change:
            callback(self, old_price, value)


# Callbacks simples (fonctions)
def log_change(stock, old, new):
    print(f"  📝 {stock.symbol}: {old}€ → {new}€")


def alert_high(stock, old, new):
    if new > 160:
        print(f"  🚨 {stock.symbol} est au-dessus de 160€ !")


google = StockPythonic("GOOG", 140.0)
google.on_price_change.append(log_change)
google.on_price_change.append(alert_high)

print("Changements avec callbacks :")
google.price = 155.0
google.price = 165.0


# =============================================================================
# 3. Observer avec événements nommés
# =============================================================================

print("\n" + "=" * 60)
print("3. OBSERVER AVEC ÉVÉNEMENTS NOMMÉS")
print("=" * 60)


class EventEmitter:
    """Émetteur d'événements générique."""

    def __init__(self):
        self._handlers = {}

    def on(self, event_name: str, handler: Callable):
        """Enregistre un handler pour un événement."""
        if event_name not in self._handlers:
            self._handlers[event_name] = []
        self._handlers[event_name].append(handler)
        return self  # Pour le chaînage

    def off(self, event_name: str, handler: Callable):
        """Retire un handler."""
        if event_name in self._handlers:
            self._handlers[event_name].remove(handler)

    def emit(self, event_name: str, *args, **kwargs):
        """Émet un événement vers tous les handlers."""
        for handler in self._handlers.get(event_name, []):
            handler(*args, **kwargs)


class UserService(EventEmitter):
    def __init__(self):
        super().__init__()
        self._users = {}

    def create_user(self, user_id: int, name: str, email: str):
        user = {"id": user_id, "name": name, "email": email}
        self._users[user_id] = user
        self.emit("user_created", user)
        return user

    def delete_user(self, user_id: int):
        if user_id in self._users:
            user = self._users.pop(user_id)
            self.emit("user_deleted", user)
            return True
        return False

    def update_user(self, user_id: int, **updates):
        if user_id in self._users:
            old_data = self._users[user_id].copy()
            self._users[user_id].update(updates)
            self.emit("user_updated", old_data, self._users[user_id])
            return self._users[user_id]
        return None


# Handlers
def send_welcome_email(user):
    print(f"  📧 Email de bienvenue envoyé à {user['email']}")


def log_user_creation(user):
    print(f"  📝 Log: Utilisateur '{user['name']}' créé (id={user['id']})")


def notify_admin(user):
    print(f"  🔔 Admin notifié de la création de {user['name']}")


def log_deletion(user):
    print(f"  🗑️ Log: Utilisateur '{user['name']}' supprimé")


# Configuration
service = UserService()
service.on("user_created", send_welcome_email)
service.on("user_created", log_user_creation)
service.on("user_created", notify_admin)
service.on("user_deleted", log_deletion)

print("Création d'utilisateurs :")
service.create_user(1, "Alice", "alice@test.com")
service.create_user(2, "Bob", "bob@test.com")

print("\nSuppression :")
service.delete_user(1)


# =============================================================================
# 4. Observer avec décorateur
# =============================================================================

print("\n" + "=" * 60)
print("4. OBSERVER AVEC DÉCORATEUR")
print("=" * 60)


class EventManager:
    """Gestionnaire d'événements avec enregistrement par décorateur."""
    _handlers = {}

    @classmethod
    def on(cls, event_name: str):
        """Décorateur pour enregistrer un handler."""
        def decorator(func):
            if event_name not in cls._handlers:
                cls._handlers[event_name] = []
            cls._handlers[event_name].append(func)
            return func
        return decorator

    @classmethod
    def emit(cls, event_name: str, *args, **kwargs):
        for handler in cls._handlers.get(event_name, []):
            handler(*args, **kwargs)

    @classmethod
    def clear(cls):
        cls._handlers = {}


# Enregistrement via décorateurs
@EventManager.on("order_placed")
def process_payment(order):
    print(f"  💳 Traitement paiement pour commande #{order['id']}")


@EventManager.on("order_placed")
def update_inventory(order):
    print(f"  📦 Mise à jour stock pour {len(order['items'])} articles")


@EventManager.on("order_placed")
def send_confirmation(order):
    print(f"  📧 Confirmation envoyée à {order['customer_email']}")


@EventManager.on("order_shipped")
def notify_customer(order):
    print(f"  🚚 Client notifié de l'expédition #{order['id']}")


print("Commande passée :")
order = {
    "id": 12345,
    "customer_email": "client@test.com",
    "items": ["item1", "item2", "item3"]
}
EventManager.emit("order_placed", order)

print("\nCommande expédiée :")
EventManager.emit("order_shipped", order)

EventManager.clear()


# =============================================================================
# 5. Observer avec typage (Protocol)
# =============================================================================

print("\n" + "=" * 60)
print("5. OBSERVER AVEC TYPAGE (PROTOCOL)")
print("=" * 60)

from typing import Protocol


class PriceObserver(Protocol):
    """Protocole définissant un observateur de prix."""
    def on_price_change(self, symbol: str, old_price: float, new_price: float) -> None:
        ...


class TypedStock:
    def __init__(self, symbol: str, price: float):
        self.symbol = symbol
        self._price = price
        self._observers: List[PriceObserver] = []

    def add_observer(self, observer: PriceObserver):
        self._observers.append(observer)

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value: float):
        old = self._price
        self._price = value
        for obs in self._observers:
            obs.on_price_change(self.symbol, old, value)


class ConsoleObserver:
    """Observe et affiche dans la console."""

    def on_price_change(self, symbol: str, old_price: float, new_price: float):
        print(f"  Console: {symbol} {old_price} → {new_price}")


class AlertObserver:
    """Observe et alerte si seuil dépassé."""

    def __init__(self, threshold: float):
        self.threshold = threshold

    def on_price_change(self, symbol: str, old_price: float, new_price: float):
        if new_price > self.threshold:
            print(f"  Alerte: {symbol} > {self.threshold} !")


stock = TypedStock("MSFT", 300.0)
stock.add_observer(ConsoleObserver())
stock.add_observer(AlertObserver(350.0))

print("Changements typés :")
stock.price = 340.0
stock.price = 360.0
