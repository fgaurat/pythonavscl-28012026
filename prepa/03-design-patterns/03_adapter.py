"""
Pattern Adapter
===============

Faire collaborer des interfaces incompatibles.
"""

from abc import ABC, abstractmethod

# =============================================================================
# 1. Le problème : interfaces incompatibles
# =============================================================================

print("=" * 60)
print("1. LE PROBLÈME : INTERFACES INCOMPATIBLES")
print("=" * 60)


# Notre interface standard
class PaymentProcessor(ABC):
    """Interface de paiement standard de notre application."""

    @abstractmethod
    def pay(self, amount: float, payment_info: dict) -> bool:
        pass

    @abstractmethod
    def refund(self, transaction_id: str, amount: float) -> bool:
        pass


# API externe avec interface non standard
class LegacyPaymentSystem:
    """Système de paiement legacy avec une interface différente."""

    def execute_payment(self, amount_cents: int, card_number: str) -> dict:
        print(f"    Legacy: paiement de {amount_cents} centimes avec carte {card_number[:4]}****")
        return {"status": "OK", "ref": "LEG123", "amount": amount_cents}

    def cancel_payment(self, reference: str, cents: int) -> dict:
        print(f"    Legacy: annulation de {reference} pour {cents} centimes")
        return {"status": "CANCELLED", "ref": reference}


print("Interface Legacy :")
legacy = LegacyPaymentSystem()
legacy.execute_payment(9999, "4111111111111111")


# =============================================================================
# 2. L'Adapter : pont entre les interfaces
# =============================================================================

print("\n" + "=" * 60)
print("2. L'ADAPTER : PONT ENTRE LES INTERFACES")
print("=" * 60)


class LegacyPaymentAdapter(PaymentProcessor):
    """Adapte LegacyPaymentSystem à notre interface PaymentProcessor."""

    def __init__(self, legacy_system: LegacyPaymentSystem):
        self.legacy = legacy_system
        self._transactions = {}  # Stocke les références pour les remboursements

    def pay(self, amount: float, payment_info: dict) -> bool:
        # Conversion : euros → centimes
        amount_cents = int(amount * 100)
        card = payment_info.get("card_number", "")

        result = self.legacy.execute_payment(amount_cents, card)

        if result["status"] == "OK":
            # Stocker la référence pour un éventuel remboursement
            self._transactions[result["ref"]] = amount_cents
            return True
        return False

    def refund(self, transaction_id: str, amount: float) -> bool:
        amount_cents = int(amount * 100)
        result = self.legacy.cancel_payment(transaction_id, amount_cents)
        return result["status"] == "CANCELLED"


# Utilisation transparente
def process_order(processor: PaymentProcessor, amount: float, card: str):
    """Fonction qui utilise notre interface standard."""
    print(f"  Traitement d'une commande de {amount}€")
    success = processor.pay(amount, {"card_number": card})
    print(f"  Résultat : {'Succès' if success else 'Échec'}")
    return success


print("Utilisation via l'adapter :")
adapter = LegacyPaymentAdapter(LegacyPaymentSystem())
process_order(adapter, 99.99, "4111111111111111")


# =============================================================================
# 3. Adapter pour une API HTTP externe
# =============================================================================

print("\n" + "=" * 60)
print("3. ADAPTER POUR API HTTP EXTERNE")
print("=" * 60)


# Simuler une API HTTP externe
class ExternalWeatherAPI:
    """API météo externe avec son propre format."""

    def fetch_weather(self, lat: float, lon: float) -> dict:
        # Simule une réponse API
        return {
            "coord": {"lat": lat, "lon": lon},
            "main": {
                "temp": 293.15,  # Kelvin !
                "humidity": 65,
                "pressure": 1013
            },
            "weather": [{"description": "partly cloudy"}],
            "wind": {"speed": 5.5}  # m/s
        }


# Notre interface interne
class WeatherService(ABC):
    @abstractmethod
    def get_temperature(self, city: str) -> float:
        """Retourne la température en Celsius."""
        pass

    @abstractmethod
    def get_conditions(self, city: str) -> dict:
        pass


class ExternalWeatherAdapter(WeatherService):
    """Adapte l'API externe à notre interface."""

    # Coordonnées des villes (simplifié)
    CITIES = {
        "paris": (48.8566, 2.3522),
        "lyon": (45.7640, 4.8357),
        "marseille": (43.2965, 5.3698),
    }

    def __init__(self, api: ExternalWeatherAPI):
        self.api = api

    def _get_coords(self, city: str) -> tuple:
        city_lower = city.lower()
        if city_lower not in self.CITIES:
            raise ValueError(f"Ville inconnue : {city}")
        return self.CITIES[city_lower]

    def get_temperature(self, city: str) -> float:
        lat, lon = self._get_coords(city)
        data = self.api.fetch_weather(lat, lon)
        # Conversion Kelvin → Celsius
        kelvin = data["main"]["temp"]
        return kelvin - 273.15

    def get_conditions(self, city: str) -> dict:
        lat, lon = self._get_coords(city)
        data = self.api.fetch_weather(lat, lon)
        return {
            "temperature_celsius": data["main"]["temp"] - 273.15,
            "humidity_percent": data["main"]["humidity"],
            "description": data["weather"][0]["description"],
            "wind_kmh": data["wind"]["speed"] * 3.6  # m/s → km/h
        }


weather_service = ExternalWeatherAdapter(ExternalWeatherAPI())
print(f"Température à Paris : {weather_service.get_temperature('paris'):.1f}°C")
print(f"Conditions à Lyon : {weather_service.get_conditions('lyon')}")


# =============================================================================
# 4. Adapter avec plusieurs systèmes
# =============================================================================

print("\n" + "=" * 60)
print("4. ADAPTER AVEC PLUSIEURS SYSTÈMES")
print("=" * 60)


# Différents systèmes de notification
class SMSProvider:
    def send_sms(self, phone: str, text: str):
        print(f"    SMS vers {phone}: {text[:30]}...")
        return True


class EmailService:
    def send_email(self, to: str, subject: str, body: str):
        print(f"    Email vers {to}: [{subject}]")
        return {"sent": True, "id": "EMAIL123"}


class PushNotificationAPI:
    def push(self, device_token: str, payload: dict):
        print(f"    Push vers {device_token[:10]}...: {payload['title']}")
        return 200


# Interface unifiée
class Notifier(ABC):
    @abstractmethod
    def send(self, recipient: str, message: str) -> bool:
        pass


class SMSAdapter(Notifier):
    def __init__(self, provider: SMSProvider):
        self.provider = provider

    def send(self, recipient: str, message: str) -> bool:
        return self.provider.send_sms(recipient, message)


class EmailAdapter(Notifier):
    def __init__(self, service: EmailService, default_subject: str = "Notification"):
        self.service = service
        self.default_subject = default_subject

    def send(self, recipient: str, message: str) -> bool:
        result = self.service.send_email(recipient, self.default_subject, message)
        return result.get("sent", False)


class PushAdapter(Notifier):
    def __init__(self, api: PushNotificationAPI):
        self.api = api

    def send(self, recipient: str, message: str) -> bool:
        payload = {"title": "Notification", "body": message}
        status = self.api.push(recipient, payload)
        return status == 200


# Utilisation polymorphique
def notify_user(notifier: Notifier, recipient: str, message: str):
    print(f"  Envoi vers {recipient[:20]}...")
    notifier.send(recipient, message)


print("Notification par différents canaux :")
notify_user(SMSAdapter(SMSProvider()), "+33612345678", "Votre code: 1234")
notify_user(EmailAdapter(EmailService()), "user@example.com", "Bienvenue !")
notify_user(PushAdapter(PushNotificationAPI()), "device_token_abc123", "Nouvelle mise à jour")


# =============================================================================
# 5. Adapter bidirectionnel
# =============================================================================

print("\n" + "=" * 60)
print("5. ADAPTER BIDIRECTIONNEL")
print("=" * 60)


class XMLDataSource:
    """Source de données retournant du XML."""

    def get_data(self) -> str:
        return """
        <users>
            <user id="1"><name>Alice</name><email>alice@test.com</email></user>
            <user id="2"><name>Bob</name><email>bob@test.com</email></user>
        </users>
        """


class JSONDataConsumer:
    """Consommateur attendant des données JSON."""

    def process(self, json_data: list):
        for item in json_data:
            print(f"    Traitement : {item}")


class XMLToJSONAdapter:
    """Adapte une source XML pour un consommateur JSON."""

    def __init__(self, xml_source: XMLDataSource):
        self.source = xml_source

    def get_json_data(self) -> list:
        import xml.etree.ElementTree as ET

        xml_str = self.source.get_data()
        root = ET.fromstring(xml_str.strip())

        result = []
        for user in root.findall("user"):
            result.append({
                "id": user.get("id"),
                "name": user.find("name").text,
                "email": user.find("email").text
            })
        return result


xml_source = XMLDataSource()
adapter = XMLToJSONAdapter(xml_source)
consumer = JSONDataConsumer()

print("Conversion XML → JSON :")
json_data = adapter.get_json_data()
consumer.process(json_data)
