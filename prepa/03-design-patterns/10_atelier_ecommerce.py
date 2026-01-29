"""
Atelier 2 : Modélisation e-commerce avec Pydantic
=================================================

Exercice : Modéliser un système e-commerce avec validation.
"""

try:
    from pydantic import (
        BaseModel, Field, field_validator, model_validator,
        computed_field, EmailStr, ConfigDict
    )
    PYDANTIC_AVAILABLE = True
except ImportError:
    PYDANTIC_AVAILABLE = False
    print("⚠️  Pydantic n'est pas installé. Installez-le avec : pip install pydantic[email]")

from typing import List, Optional
from datetime import datetime
from enum import Enum
from decimal import Decimal

# =============================================================================
# EXERCICE
# =============================================================================

"""
Objectif : Modéliser un système e-commerce avec :

- Product : nom, prix (> 0), stock (>= 0), catégorie
- Address : rue, ville, code postal (5 chiffres), pays
- Customer : nom, email valide, liste d'adresses
- OrderItem : produit, quantité (> 0), prix unitaire, sous-total calculé
- Order : client, articles, statut (enum), total calculé

Contraintes :
- Prix > 0, stock >= 0
- Email valide
- Code postal français (5 chiffres)
- Statut parmi : pending, paid, shipped, delivered, cancelled
- Le total doit être calculé automatiquement
"""

if PYDANTIC_AVAILABLE:

    # =========================================================================
    # SOLUTION
    # =========================================================================

    # -------------------------------------------------------------------------
    # Enums
    # -------------------------------------------------------------------------

    class OrderStatus(str, Enum):
        PENDING = "pending"
        PAID = "paid"
        SHIPPED = "shipped"
        DELIVERED = "delivered"
        CANCELLED = "cancelled"

    class ProductCategory(str, Enum):
        ELECTRONICS = "electronics"
        CLOTHING = "clothing"
        BOOKS = "books"
        HOME = "home"
        FOOD = "food"
        OTHER = "other"

    # -------------------------------------------------------------------------
    # Modèles de base
    # -------------------------------------------------------------------------

    class Address(BaseModel):
        """Adresse de livraison ou facturation."""
        model_config = ConfigDict(str_strip_whitespace=True)

        street: str = Field(min_length=5, max_length=100)
        city: str = Field(min_length=2, max_length=50)
        postal_code: str = Field(pattern=r"^\d{5}$")
        country: str = Field(default="France", max_length=50)

        @field_validator("city")
        @classmethod
        def capitalize_city(cls, v: str) -> str:
            return v.title()

    class Product(BaseModel):
        """Produit du catalogue."""
        id: int
        name: str = Field(min_length=1, max_length=100)
        description: str = Field(default="", max_length=500)
        price: Decimal = Field(gt=0, decimal_places=2)
        stock: int = Field(ge=0)
        category: ProductCategory = ProductCategory.OTHER
        is_active: bool = True

        @field_validator("price", mode="before")
        @classmethod
        def convert_price(cls, v):
            """Convertit en Decimal si nécessaire."""
            if isinstance(v, (int, float)):
                return Decimal(str(v))
            return v

        def is_available(self, quantity: int = 1) -> bool:
            """Vérifie si le produit est disponible."""
            return self.is_active and self.stock >= quantity

    # -------------------------------------------------------------------------
    # Client
    # -------------------------------------------------------------------------

    class Customer(BaseModel):
        """Client de la boutique."""
        id: int
        first_name: str = Field(min_length=1, max_length=50)
        last_name: str = Field(min_length=1, max_length=50)
        email: EmailStr
        phone: Optional[str] = Field(default=None, pattern=r"^\+?\d{10,15}$")
        addresses: List[Address] = Field(default_factory=list, max_length=5)
        created_at: datetime = Field(default_factory=datetime.now)
        is_vip: bool = False

        @computed_field
        @property
        def full_name(self) -> str:
            return f"{self.first_name} {self.last_name}"

        @property
        def default_address(self) -> Optional[Address]:
            return self.addresses[0] if self.addresses else None

    # -------------------------------------------------------------------------
    # Commande
    # -------------------------------------------------------------------------

    class OrderItem(BaseModel):
        """Ligne de commande."""
        product_id: int
        product_name: str
        quantity: int = Field(gt=0, le=100)
        unit_price: Decimal = Field(gt=0)

        @computed_field
        @property
        def subtotal(self) -> Decimal:
            return self.quantity * self.unit_price

        @classmethod
        def from_product(cls, product: Product, quantity: int) -> "OrderItem":
            """Crée un OrderItem depuis un Product."""
            return cls(
                product_id=product.id,
                product_name=product.name,
                quantity=quantity,
                unit_price=product.price
            )

    class Order(BaseModel):
        """Commande client."""
        model_config = ConfigDict(validate_default=True)

        id: int
        customer_id: int
        items: List[OrderItem] = Field(min_length=1)
        status: OrderStatus = OrderStatus.PENDING
        shipping_address: Address
        billing_address: Optional[Address] = None
        discount_percent: Decimal = Field(ge=0, le=100, default=Decimal("0"))
        notes: str = Field(default="", max_length=500)
        created_at: datetime = Field(default_factory=datetime.now)
        updated_at: Optional[datetime] = None

        @computed_field
        @property
        def items_count(self) -> int:
            return sum(item.quantity for item in self.items)

        @computed_field
        @property
        def subtotal(self) -> Decimal:
            return sum(item.subtotal for item in self.items)

        @computed_field
        @property
        def discount_amount(self) -> Decimal:
            return self.subtotal * self.discount_percent / 100

        @computed_field
        @property
        def total(self) -> Decimal:
            return self.subtotal - self.discount_amount

        @model_validator(mode="after")
        def set_billing_address(self):
            """Utilise l'adresse de livraison comme facturation par défaut."""
            if self.billing_address is None:
                self.billing_address = self.shipping_address
            return self

        def can_cancel(self) -> bool:
            """Vérifie si la commande peut être annulée."""
            return self.status in [OrderStatus.PENDING, OrderStatus.PAID]

        def can_ship(self) -> bool:
            """Vérifie si la commande peut être expédiée."""
            return self.status == OrderStatus.PAID

    # =========================================================================
    # DÉMONSTRATION
    # =========================================================================

    if __name__ == "__main__":
        print("=" * 60)
        print("DÉMONSTRATION DU SYSTÈME E-COMMERCE")
        print("=" * 60)

        # Créer des produits
        print("\n--- Création des produits ---")
        products = [
            Product(
                id=1,
                name="Laptop Pro",
                description="Ordinateur portable haute performance",
                price=1299.99,
                stock=50,
                category=ProductCategory.ELECTRONICS
            ),
            Product(
                id=2,
                name="T-shirt Python",
                description="T-shirt avec logo Python",
                price=29.99,
                stock=200,
                category=ProductCategory.CLOTHING
            ),
            Product(
                id=3,
                name="Clean Code",
                description="Livre de Robert C. Martin",
                price=45.00,
                stock=30,
                category=ProductCategory.BOOKS
            ),
        ]

        for p in products:
            print(f"  {p.name}: {p.price}€ ({p.stock} en stock)")

        # Créer un client
        print("\n--- Création du client ---")
        customer = Customer(
            id=1,
            first_name="Alice",
            last_name="Martin",
            email="alice.martin@example.com",
            phone="+33612345678",
            addresses=[
                Address(
                    street="123 Rue de la Paix",
                    city="paris",  # Sera capitalisé
                    postal_code="75001"
                ),
                Address(
                    street="456 Avenue des Champs",
                    city="lyon",
                    postal_code="69001"
                )
            ],
            is_vip=True
        )
        print(f"  Client: {customer.full_name}")
        print(f"  Email: {customer.email}")
        print(f"  VIP: {customer.is_vip}")
        print(f"  Adresse par défaut: {customer.default_address.city}")

        # Créer une commande
        print("\n--- Création de la commande ---")
        order = Order(
            id=1001,
            customer_id=customer.id,
            items=[
                OrderItem.from_product(products[0], quantity=1),  # Laptop
                OrderItem.from_product(products[1], quantity=2),  # 2 T-shirts
                OrderItem.from_product(products[2], quantity=1),  # Livre
            ],
            shipping_address=customer.default_address,
            discount_percent=Decimal("10"),  # -10% VIP
            notes="Livraison express souhaitée"
        )

        print(f"  Commande #{order.id}")
        print(f"  Articles :")
        for item in order.items:
            print(f"    - {item.product_name} x{item.quantity}: {item.subtotal}€")
        print(f"  Sous-total: {order.subtotal}€")
        print(f"  Remise ({order.discount_percent}%): -{order.discount_amount}€")
        print(f"  Total: {order.total}€")
        print(f"  Statut: {order.status.value}")

        # Sérialisation JSON
        print("\n--- Sérialisation JSON ---")
        json_data = order.model_dump_json(indent=2)
        print(f"  Taille JSON: {len(json_data)} caractères")
        print(f"  Aperçu: {json_data[:200]}...")

        # Validation d'erreurs
        print("\n--- Tests de validation ---")

        # Test: prix négatif
        try:
            Product(id=99, name="Bad Product", price=-10, stock=5)
        except Exception as e:
            print(f"  Prix négatif: ✓ Erreur détectée")

        # Test: email invalide
        try:
            Customer(id=99, first_name="Bad", last_name="User", email="invalid")
        except Exception as e:
            print(f"  Email invalide: ✓ Erreur détectée")

        # Test: code postal invalide
        try:
            Address(street="123 Test St", city="Test", postal_code="ABC")
        except Exception as e:
            print(f"  Code postal invalide: ✓ Erreur détectée")

        # Test: commande vide
        try:
            Order(
                id=99,
                customer_id=1,
                items=[],  # Vide !
                shipping_address=customer.default_address
            )
        except Exception as e:
            print(f"  Commande vide: ✓ Erreur détectée")

        print("\n--- Fin de la démonstration ---")

else:
    print("\nExemples non disponibles sans Pydantic.")
    print("Installation : pip install pydantic[email]")
