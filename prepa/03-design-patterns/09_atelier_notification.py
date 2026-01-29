"""
Atelier 1 : Système de notification
===================================

Exercice : Implémenter un système de notification utilisant
Factory, Strategy et Observer.
"""

from abc import ABC, abstractmethod
from typing import List, Callable
from dataclasses import dataclass, field
from datetime import datetime

# =============================================================================
# EXERCICE
# =============================================================================

"""
Objectif : Créer un système de notification avec :

1. FACTORY : Créer différents types de notifiers (email, sms, push)
2. STRATEGY : Différentes méthodes d'envoi (immédiat, groupé, planifié)
3. OBSERVER : Notifier plusieurs destinataires et logger les envois

Usage attendu :
    notifier = NotifierFactory.create("email")
    notifier.add_observer(logger_observer)
    notifier.set_strategy(BatchStrategy())
    notifier.send("Hello!", recipients=["alice@test.com", "bob@test.com"])
"""


# =============================================================================
# SOLUTION
# =============================================================================

# -----------------------------------------------------------------------------
# 1. Data classes
# -----------------------------------------------------------------------------

@dataclass
class Message:
    """Représente un message à envoyer."""
    recipient: str
    content: str
    type: str  # email, sms, push
    timestamp: datetime = field(default_factory=datetime.now)


@dataclass
class SendResult:
    """Résultat d'un envoi."""
    success: bool
    message: Message
    details: str = ""


# -----------------------------------------------------------------------------
# 2. Strategy Pattern - Stratégies d'envoi
# -----------------------------------------------------------------------------

class SendStrategy(ABC):
    """Interface pour les stratégies d'envoi."""

    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @abstractmethod
    def send(self, messages: List[Message]) -> List[SendResult]:
        pass


class ImmediateStrategy(SendStrategy):
    """Envoie chaque message immédiatement."""

    @property
    def name(self) -> str:
        return "immediate"

    def send(self, messages: List[Message]) -> List[SendResult]:
        results = []
        for msg in messages:
            print(f"    📤 Envoi immédiat à {msg.recipient}: {msg.content[:30]}...")
            results.append(SendResult(success=True, message=msg))
        return results


class BatchStrategy(SendStrategy):
    """Regroupe les messages avant envoi."""

    def __init__(self, batch_size: int = 10):
        self.batch_size = batch_size

    @property
    def name(self) -> str:
        return f"batch({self.batch_size})"

    def send(self, messages: List[Message]) -> List[SendResult]:
        results = []
        for i in range(0, len(messages), self.batch_size):
            batch = messages[i:i + self.batch_size]
            print(f"    📦 Envoi groupé de {len(batch)} messages")
            for msg in batch:
                print(f"      → {msg.recipient}")
                results.append(SendResult(success=True, message=msg))
        return results


class DelayedStrategy(SendStrategy):
    """Simule un envoi différé (pour démonstration)."""

    def __init__(self, delay_seconds: int = 60):
        self.delay_seconds = delay_seconds

    @property
    def name(self) -> str:
        return f"delayed({self.delay_seconds}s)"

    def send(self, messages: List[Message]) -> List[SendResult]:
        print(f"    ⏰ Planification de {len(messages)} messages (délai: {self.delay_seconds}s)")
        results = []
        for msg in messages:
            print(f"      → {msg.recipient} planifié")
            results.append(SendResult(
                success=True,
                message=msg,
                details=f"Envoi prévu dans {self.delay_seconds}s"
            ))
        return results


# -----------------------------------------------------------------------------
# 3. Observer Pattern - Observateurs
# -----------------------------------------------------------------------------

class NotificationObserver(ABC):
    """Interface pour les observateurs."""

    @abstractmethod
    def on_send(self, results: List[SendResult]) -> None:
        pass


class LoggerObserver(NotificationObserver):
    """Log tous les envois."""

    def on_send(self, results: List[SendResult]) -> None:
        for result in results:
            status = "✅" if result.success else "❌"
            print(f"  [LOG] {status} {result.message.type} → {result.message.recipient}")


class MetricsObserver(NotificationObserver):
    """Collecte des métriques."""

    def __init__(self):
        self.total_sent = 0
        self.success_count = 0
        self.failure_count = 0

    def on_send(self, results: List[SendResult]) -> None:
        self.total_sent += len(results)
        self.success_count += sum(1 for r in results if r.success)
        self.failure_count += sum(1 for r in results if not r.success)

    def report(self) -> str:
        return f"Métriques: {self.total_sent} envois, {self.success_count} succès, {self.failure_count} échecs"


class WebhookObserver(NotificationObserver):
    """Simule l'appel à un webhook."""

    def __init__(self, url: str):
        self.url = url

    def on_send(self, results: List[SendResult]) -> None:
        print(f"  [WEBHOOK] POST {self.url} avec {len(results)} résultats")


# -----------------------------------------------------------------------------
# 4. Notifiers (avec Observer intégré)
# -----------------------------------------------------------------------------

class Notifier(ABC):
    """Classe de base pour les notifiers."""

    def __init__(self):
        self._strategy: SendStrategy = ImmediateStrategy()
        self._observers: List[NotificationObserver] = []

    def set_strategy(self, strategy: SendStrategy):
        print(f"  Stratégie changée : {strategy.name}")
        self._strategy = strategy

    def add_observer(self, observer: NotificationObserver):
        self._observers.append(observer)

    def remove_observer(self, observer: NotificationObserver):
        self._observers.remove(observer)

    @property
    @abstractmethod
    def type(self) -> str:
        pass

    @abstractmethod
    def format_message(self, content: str, recipient: str) -> Message:
        pass

    def send(self, content: str, recipients: List[str]) -> List[SendResult]:
        # Créer les messages
        messages = [self.format_message(content, r) for r in recipients]

        # Envoyer via la stratégie
        results = self._strategy.send(messages)

        # Notifier les observers
        for observer in self._observers:
            observer.on_send(results)

        return results


class EmailNotifier(Notifier):
    """Notifier pour emails."""

    def __init__(self, sender: str = "noreply@example.com"):
        super().__init__()
        self.sender = sender

    @property
    def type(self) -> str:
        return "email"

    def format_message(self, content: str, recipient: str) -> Message:
        return Message(
            recipient=recipient,
            content=f"From: {self.sender}\nTo: {recipient}\n\n{content}",
            type=self.type
        )


class SMSNotifier(Notifier):
    """Notifier pour SMS."""

    def __init__(self, sender_number: str = "+33600000000"):
        super().__init__()
        self.sender_number = sender_number

    @property
    def type(self) -> str:
        return "sms"

    def format_message(self, content: str, recipient: str) -> Message:
        # SMS limité à 160 caractères
        truncated = content[:157] + "..." if len(content) > 160 else content
        return Message(
            recipient=recipient,
            content=truncated,
            type=self.type
        )


class PushNotifier(Notifier):
    """Notifier pour push notifications."""

    def __init__(self, app_id: str = "my-app"):
        super().__init__()
        self.app_id = app_id

    @property
    def type(self) -> str:
        return "push"

    def format_message(self, content: str, recipient: str) -> Message:
        return Message(
            recipient=recipient,
            content=f"{self.app_id}: {content}",
            type=self.type
        )


# -----------------------------------------------------------------------------
# 5. Factory Pattern
# -----------------------------------------------------------------------------

class NotifierFactory:
    """Factory pour créer des notifiers."""

    _notifiers = {
        "email": EmailNotifier,
        "sms": SMSNotifier,
        "push": PushNotifier,
    }

    @classmethod
    def register(cls, name: str, notifier_class):
        """Enregistre un nouveau type de notifier."""
        cls._notifiers[name] = notifier_class

    @classmethod
    def create(cls, notifier_type: str, **kwargs) -> Notifier:
        """Crée un notifier du type spécifié."""
        if notifier_type not in cls._notifiers:
            raise ValueError(f"Type de notifier inconnu : {notifier_type}")
        return cls._notifiers[notifier_type](**kwargs)

    @classmethod
    def available_types(cls) -> List[str]:
        return list(cls._notifiers.keys())


# =============================================================================
# DÉMONSTRATION
# =============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("DÉMONSTRATION DU SYSTÈME DE NOTIFICATION")
    print("=" * 60)

    # Créer les observers
    logger = LoggerObserver()
    metrics = MetricsObserver()
    webhook = WebhookObserver("https://api.example.com/webhook")

    # Test 1: Email avec stratégie immédiate
    print("\n--- Test 1: Email (immédiat) ---")
    email_notifier = NotifierFactory.create("email", sender="team@company.com")
    email_notifier.add_observer(logger)
    email_notifier.add_observer(metrics)
    email_notifier.send(
        "Bienvenue sur notre plateforme !",
        recipients=["alice@test.com", "bob@test.com"]
    )

    # Test 2: SMS avec stratégie batch
    print("\n--- Test 2: SMS (batch) ---")
    sms_notifier = NotifierFactory.create("sms")
    sms_notifier.add_observer(logger)
    sms_notifier.add_observer(metrics)
    sms_notifier.set_strategy(BatchStrategy(batch_size=2))
    sms_notifier.send(
        "Votre code de vérification est : 123456",
        recipients=["+33611111111", "+33622222222", "+33633333333"]
    )

    # Test 3: Push avec stratégie différée
    print("\n--- Test 3: Push (différé) ---")
    push_notifier = NotifierFactory.create("push", app_id="myapp")
    push_notifier.add_observer(logger)
    push_notifier.add_observer(metrics)
    push_notifier.add_observer(webhook)
    push_notifier.set_strategy(DelayedStrategy(delay_seconds=300))
    push_notifier.send(
        "Nouvelle mise à jour disponible !",
        recipients=["device_token_1", "device_token_2"]
    )

    # Rapport des métriques
    print("\n--- Rapport ---")
    print(f"  {metrics.report()}")
    print(f"  Types disponibles : {NotifierFactory.available_types()}")
