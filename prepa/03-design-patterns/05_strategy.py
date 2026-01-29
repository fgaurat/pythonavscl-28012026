"""
Pattern Strategy
================

Permettre de changer d'algorithme dynamiquement.
"""

from abc import ABC, abstractmethod
from typing import Callable, List
from dataclasses import dataclass

# =============================================================================
# 1. Le problème : code rigide
# =============================================================================

print("=" * 60)
print("1. LE PROBLÈME : CODE RIGIDE")
print("=" * 60)


# Sans Strategy (difficile à étendre et maintenir)
class ShippingBad:
    def calculate(self, weight: float, method: str) -> float:
        if method == "standard":
            return weight * 1.5
        elif method == "express":
            return weight * 3.0
        elif method == "overnight":
            return weight * 5.0 + 10
        else:
            raise ValueError(f"Méthode inconnue: {method}")


shipping_bad = ShippingBad()
print(f"Standard (2kg) : {shipping_bad.calculate(2, 'standard')}€")
print(f"Express (2kg) : {shipping_bad.calculate(2, 'express')}€")
print("Problème : ajouter une méthode = modifier la classe")


# =============================================================================
# 2. Strategy classique avec ABC
# =============================================================================

print("\n" + "=" * 60)
print("2. STRATEGY CLASSIQUE AVEC ABC")
print("=" * 60)


@dataclass
class Order:
    weight: float
    destination: str
    items_count: int


class ShippingStrategy(ABC):
    @abstractmethod
    def calculate(self, order: Order) -> float:
        pass

    @property
    @abstractmethod
    def name(self) -> str:
        pass


class StandardShipping(ShippingStrategy):
    @property
    def name(self):
        return "Standard (3-5 jours)"

    def calculate(self, order: Order) -> float:
        return order.weight * 1.5


class ExpressShipping(ShippingStrategy):
    @property
    def name(self):
        return "Express (1-2 jours)"

    def calculate(self, order: Order) -> float:
        return order.weight * 3.0


class OvernightShipping(ShippingStrategy):
    @property
    def name(self):
        return "Overnight (lendemain)"

    def calculate(self, order: Order) -> float:
        return order.weight * 5.0 + 10


class FreeShipping(ShippingStrategy):
    """Nouveau : livraison gratuite pour les grosses commandes."""

    @property
    def name(self):
        return "Gratuit"

    def calculate(self, order: Order) -> float:
        return 0.0


class ShippingCalculator:
    def __init__(self, strategy: ShippingStrategy):
        self._strategy = strategy

    def set_strategy(self, strategy: ShippingStrategy):
        self._strategy = strategy

    def calculate(self, order: Order) -> float:
        return self._strategy.calculate(order)

    def get_strategy_name(self) -> str:
        return self._strategy.name


order = Order(weight=2.5, destination="Paris", items_count=3)
calculator = ShippingCalculator(StandardShipping())

for strategy in [StandardShipping(), ExpressShipping(), OvernightShipping(), FreeShipping()]:
    calculator.set_strategy(strategy)
    cost = calculator.calculate(order)
    print(f"  {strategy.name}: {cost:.2f}€")


# =============================================================================
# 3. Strategy pythonique avec fonctions
# =============================================================================

print("\n" + "=" * 60)
print("3. STRATEGY PYTHONIQUE AVEC FONCTIONS")
print("=" * 60)


# Les stratégies sont simplement des fonctions
def standard_shipping(order: Order) -> float:
    return order.weight * 1.5


def express_shipping(order: Order) -> float:
    return order.weight * 3.0


def overnight_shipping(order: Order) -> float:
    return order.weight * 5.0 + 10


def international_shipping(order: Order) -> float:
    """Nouvelle stratégie : ajoutée sans modifier les classes."""
    base = order.weight * 4.0
    if order.destination not in ["France", "Belgique", "Suisse"]:
        base += 15  # Supplément international
    return base


@dataclass
class OrderV2:
    weight: float
    destination: str = "France"
    shipping_fn: Callable[["OrderV2"], float] = standard_shipping

    def shipping_cost(self) -> float:
        return self.shipping_fn(self)


# Utilisation
orders = [
    OrderV2(2.5, "Paris", standard_shipping),
    OrderV2(2.5, "Paris", express_shipping),
    OrderV2(2.5, "USA", international_shipping),
]

for order in orders:
    print(f"  {order.shipping_fn.__name__}: {order.shipping_cost():.2f}€")


# =============================================================================
# 4. Strategy avec closure (paramétrable)
# =============================================================================

print("\n" + "=" * 60)
print("4. STRATEGY AVEC CLOSURE (PARAMÉTRABLE)")
print("=" * 60)


def create_tiered_shipping(tiers: List[tuple]) -> Callable[[Order], float]:
    """
    Crée une stratégie de livraison par paliers.
    tiers: liste de (poids_max, prix_par_kg)
    """
    def calculate(order: Order) -> float:
        for max_weight, price_per_kg in sorted(tiers):
            if order.weight <= max_weight:
                return order.weight * price_per_kg
        # Au-delà du dernier palier
        return order.weight * tiers[-1][1]

    return calculate


# Stratégies personnalisées
economique = create_tiered_shipping([
    (1.0, 2.0),   # Jusqu'à 1kg : 2€/kg
    (5.0, 1.5),   # 1-5kg : 1.5€/kg
    (10.0, 1.0),  # 5-10kg : 1€/kg
])

premium = create_tiered_shipping([
    (1.0, 5.0),
    (5.0, 4.0),
    (10.0, 3.0),
])

orders = [
    Order(0.5, "Paris", 1),
    Order(3.0, "Lyon", 2),
    Order(8.0, "Marseille", 5),
]

print("Stratégie économique :")
for order in orders:
    print(f"  {order.weight}kg: {economique(order):.2f}€")

print("\nStratégie premium :")
for order in orders:
    print(f"  {order.weight}kg: {premium(order):.2f}€")


# =============================================================================
# 5. Strategy pour le tri
# =============================================================================

print("\n" + "=" * 60)
print("5. STRATEGY POUR LE TRI")
print("=" * 60)


@dataclass
class Product:
    name: str
    price: float
    rating: float
    sales: int

    def __repr__(self):
        return f"{self.name} ({self.price}€, ★{self.rating}, {self.sales} ventes)"


# Stratégies de tri (fonctions key)
def by_price(p: Product) -> float:
    return p.price


def by_rating(p: Product) -> float:
    return -p.rating  # Négatif pour tri décroissant


def by_popularity(p: Product) -> int:
    return -p.sales


def by_value(p: Product) -> float:
    """Rapport qualité/prix."""
    return -(p.rating / p.price)


products = [
    Product("Laptop", 999.99, 4.5, 150),
    Product("Mouse", 29.99, 4.8, 500),
    Product("Keyboard", 79.99, 4.2, 200),
    Product("Monitor", 299.99, 4.6, 100),
]


class ProductCatalog:
    def __init__(self, products: List[Product]):
        self.products = products
        self._sort_strategy = by_price

    def set_sort_strategy(self, strategy: Callable[[Product], float]):
        self._sort_strategy = strategy

    def get_sorted(self) -> List[Product]:
        return sorted(self.products, key=self._sort_strategy)


catalog = ProductCatalog(products)

strategies = [
    ("Par prix (croissant)", by_price),
    ("Par note (décroissant)", by_rating),
    ("Par popularité", by_popularity),
    ("Par rapport qualité/prix", by_value),
]

for name, strategy in strategies:
    catalog.set_sort_strategy(strategy)
    print(f"\n{name}:")
    for p in catalog.get_sorted():
        print(f"  {p}")


# =============================================================================
# 6. Strategy avec contexte (discount)
# =============================================================================

print("\n" + "=" * 60)
print("6. STRATEGY AVEC CONTEXTE (DISCOUNT)")
print("=" * 60)


class DiscountStrategy(ABC):
    @abstractmethod
    def apply(self, price: float, context: dict) -> float:
        pass


class NoDiscount(DiscountStrategy):
    def apply(self, price: float, context: dict) -> float:
        return price


class PercentageDiscount(DiscountStrategy):
    def __init__(self, percentage: float):
        self.percentage = percentage

    def apply(self, price: float, context: dict) -> float:
        return price * (1 - self.percentage / 100)


class LoyaltyDiscount(DiscountStrategy):
    """Réduction basée sur l'ancienneté du client."""

    def apply(self, price: float, context: dict) -> float:
        years = context.get("customer_years", 0)
        discount = min(years * 2, 20)  # 2% par an, max 20%
        return price * (1 - discount / 100)


class BulkDiscount(DiscountStrategy):
    """Réduction basée sur la quantité."""

    def __init__(self, thresholds: List[tuple]):
        # [(quantity, discount%), ...]
        self.thresholds = sorted(thresholds, reverse=True)

    def apply(self, price: float, context: dict) -> float:
        quantity = context.get("quantity", 1)
        for min_qty, discount in self.thresholds:
            if quantity >= min_qty:
                return price * (1 - discount / 100)
        return price


class PricingEngine:
    def __init__(self):
        self.strategies: List[DiscountStrategy] = []

    def add_strategy(self, strategy: DiscountStrategy):
        self.strategies.append(strategy)

    def calculate_final_price(self, base_price: float, context: dict) -> float:
        price = base_price
        for strategy in self.strategies:
            price = strategy.apply(price, context)
        return price


# Configuration
engine = PricingEngine()
engine.add_strategy(PercentageDiscount(10))  # Soldes -10%
engine.add_strategy(LoyaltyDiscount())
engine.add_strategy(BulkDiscount([(10, 5), (50, 10), (100, 15)]))

# Tests
contexts = [
    {"customer_years": 0, "quantity": 1},
    {"customer_years": 5, "quantity": 1},
    {"customer_years": 5, "quantity": 50},
    {"customer_years": 10, "quantity": 100},
]

base_price = 100.0
print(f"Prix de base : {base_price}€")
for ctx in contexts:
    final = engine.calculate_final_price(base_price, ctx)
    print(f"  Client {ctx['customer_years']} ans, qté {ctx['quantity']:3d} : {final:.2f}€")
