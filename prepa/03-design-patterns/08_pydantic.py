"""
Pydantic
========

Validation de données et sérialisation avec Pydantic v2.
"""

try:
    from pydantic import (
        BaseModel, Field, field_validator, model_validator,
        ConfigDict, EmailStr, HttpUrl, computed_field
    )
    PYDANTIC_AVAILABLE = True
except ImportError:
    PYDANTIC_AVAILABLE = False
    print("⚠️  Pydantic n'est pas installé. Installez-le avec : pip install pydantic[email]")

from typing import List, Optional, Union, Literal
from datetime import datetime
from enum import Enum

if PYDANTIC_AVAILABLE:

    # =========================================================================
    # 1. Syntaxe de base
    # =========================================================================

    print("=" * 60)
    print("1. SYNTAXE DE BASE")
    print("=" * 60)

    class User(BaseModel):
        name: str
        age: int
        email: str

    # Validation automatique
    user = User(name="Alice", age=30, email="alice@example.com")
    print(f"User : {user}")

    # Conversion automatique (coercion)
    user2 = User(name="Bob", age="25", email="bob@test.com")  # age en string !
    print(f"Coercion : age={user2.age}, type={type(user2.age).__name__}")

    # Erreur de validation
    print("\nErreur de validation :")
    try:
        User(name="Charlie", age="pas un nombre", email="test@test.com")
    except Exception as e:
        print(f"  {type(e).__name__}: {e.errors()[0]['msg']}")


    # =========================================================================
    # 2. Types avancés
    # =========================================================================

    print("\n" + "=" * 60)
    print("2. TYPES AVANCÉS")
    print("=" * 60)

    class Contact(BaseModel):
        # Email validé
        email: EmailStr

        # URL validée (optionnelle)
        website: Optional[HttpUrl] = None

        # Contraintes numériques
        age: int = Field(ge=0, le=150)  # 0 <= age <= 150

        # Contraintes de chaîne
        username: str = Field(min_length=3, max_length=20)

        # Datetime avec parsing automatique
        created_at: datetime

    contact = Contact(
        email="test@example.com",
        age=25,
        username="alice",
        created_at="2024-01-15T10:30:00"  # String → datetime
    )
    print(f"Contact : {contact}")
    print(f"  created_at type : {type(contact.created_at).__name__}")


    # =========================================================================
    # 3. Validation avec Field()
    # =========================================================================

    print("\n" + "=" * 60)
    print("3. VALIDATION AVEC FIELD()")
    print("=" * 60)

    class Product(BaseModel):
        # Valeur par défaut
        name: str = Field(default="Unknown")

        # Description pour la documentation
        price: float = Field(gt=0, description="Prix du produit en euros")

        # Alias pour les données JSON
        sku: str = Field(alias="product_code")

        # Pattern regex
        reference: str = Field(pattern=r"^[A-Z]{2}-\d{4}$")

        # Liste avec contrainte de taille
        tags: List[str] = Field(default_factory=list, max_length=5)

        model_config = ConfigDict(populate_by_name=True)

    # Utilisation avec alias
    data = {
        "name": "Laptop",
        "price": 999.99,
        "product_code": "ABC123",  # Utilise l'alias
        "reference": "AB-1234"
    }
    product = Product(**data)
    print(f"Product : {product}")
    print(f"  sku (via alias) : {product.sku}")


    # =========================================================================
    # 4. Validateurs personnalisés
    # =========================================================================

    print("\n" + "=" * 60)
    print("4. VALIDATEURS PERSONNALISÉS")
    print("=" * 60)

    class UserRegistration(BaseModel):
        username: str
        email: EmailStr
        password: str
        password_confirm: str

        @field_validator("username")
        @classmethod
        def username_alphanumeric(cls, v: str) -> str:
            if not v.isalnum():
                raise ValueError("Le username doit être alphanumérique")
            return v.lower()  # Transformation

        @field_validator("password")
        @classmethod
        def password_strength(cls, v: str) -> str:
            if len(v) < 8:
                raise ValueError("Le mot de passe doit avoir au moins 8 caractères")
            if not any(c.isupper() for c in v):
                raise ValueError("Le mot de passe doit contenir une majuscule")
            if not any(c.isdigit() for c in v):
                raise ValueError("Le mot de passe doit contenir un chiffre")
            return v

        @model_validator(mode="after")
        def passwords_match(self):
            if self.password != self.password_confirm:
                raise ValueError("Les mots de passe ne correspondent pas")
            return self

    user = UserRegistration(
        username="Alice123",
        email="alice@test.com",
        password="Secret123",
        password_confirm="Secret123"
    )
    print(f"UserRegistration : username='{user.username}'")

    print("\nValidation échouée :")
    try:
        UserRegistration(
            username="Alice123",
            email="alice@test.com",
            password="Secret123",
            password_confirm="Different456"
        )
    except Exception as e:
        print(f"  {e.errors()[0]['msg']}")


    # =========================================================================
    # 5. Modèles imbriqués
    # =========================================================================

    print("\n" + "=" * 60)
    print("5. MODÈLES IMBRIQUÉS")
    print("=" * 60)

    class Address(BaseModel):
        street: str
        city: str
        postal_code: str
        country: str = "France"

    class Company(BaseModel):
        name: str
        address: Address

    class Employee(BaseModel):
        name: str
        email: EmailStr
        company: Company
        addresses: List[Address] = []

    # Pydantic valide récursivement
    data = {
        "name": "Alice",
        "email": "alice@company.com",
        "company": {
            "name": "TechCorp",
            "address": {
                "street": "123 Main St",
                "city": "Paris",
                "postal_code": "75001"
            }
        },
        "addresses": [
            {"street": "Home St", "city": "Lyon", "postal_code": "69001"}
        ]
    }
    employee = Employee(**data)
    print(f"Employee : {employee.name}")
    print(f"  Company : {employee.company.name}")
    print(f"  Company city : {employee.company.address.city}")


    # =========================================================================
    # 6. Sérialisation JSON
    # =========================================================================

    print("\n" + "=" * 60)
    print("6. SÉRIALISATION JSON")
    print("=" * 60)

    class Article(BaseModel):
        title: str
        content: str
        created_at: datetime = Field(default_factory=datetime.now)
        views: int = 0

    article = Article(title="Hello World", content="Lorem ipsum...")

    # Vers dictionnaire
    print(f"model_dump() : {article.model_dump()}")

    # Vers JSON string
    json_str = article.model_dump_json()
    print(f"model_dump_json() : {json_str[:60]}...")

    # Depuis JSON
    article2 = Article.model_validate_json(json_str)
    print(f"model_validate_json() : {article2.title}")

    # Options de sérialisation
    print(f"\nExclude : {article.model_dump(exclude={'content'})}")
    print(f"Include : {article.model_dump(include={'title', 'views'})}")


    # =========================================================================
    # 7. Enums et types discriminants
    # =========================================================================

    print("\n" + "=" * 60)
    print("7. ENUMS ET TYPES DISCRIMINANTS")
    print("=" * 60)

    class Status(str, Enum):
        DRAFT = "draft"
        PUBLISHED = "published"
        ARCHIVED = "archived"

    class Priority(int, Enum):
        LOW = 1
        MEDIUM = 2
        HIGH = 3

    class Task(BaseModel):
        title: str
        status: Status = Status.DRAFT
        priority: Priority = Priority.MEDIUM

    task = Task(title="My Task", status="published", priority=3)
    print(f"Task : {task}")
    print(f"  status type : {type(task.status)}")
    print(f"  model_dump : {task.model_dump()}")

    # Types discriminants (Union)
    class Cat(BaseModel):
        type: Literal["cat"] = "cat"
        meow_volume: int

    class Dog(BaseModel):
        type: Literal["dog"] = "dog"
        bark_volume: int

    class Pet(BaseModel):
        animal: Union[Cat, Dog] = Field(discriminator="type")

    pet1 = Pet(animal={"type": "cat", "meow_volume": 5})
    pet2 = Pet(animal={"type": "dog", "bark_volume": 10})
    print(f"\nPet1 animal type : {type(pet1.animal).__name__}")
    print(f"Pet2 animal type : {type(pet2.animal).__name__}")


    # =========================================================================
    # 8. Champs calculés
    # =========================================================================

    print("\n" + "=" * 60)
    print("8. CHAMPS CALCULÉS")
    print("=" * 60)

    class OrderItem(BaseModel):
        product_name: str
        quantity: int = Field(gt=0)
        unit_price: float = Field(gt=0)

        @computed_field
        @property
        def subtotal(self) -> float:
            return self.quantity * self.unit_price

    class Order(BaseModel):
        id: int
        items: List[OrderItem] = Field(min_length=1)
        discount_percent: float = Field(ge=0, le=100, default=0)

        @computed_field
        @property
        def total_before_discount(self) -> float:
            return sum(item.subtotal for item in self.items)

        @computed_field
        @property
        def total(self) -> float:
            return self.total_before_discount * (1 - self.discount_percent / 100)

    order = Order(
        id=1,
        items=[
            OrderItem(product_name="Widget", quantity=2, unit_price=29.99),
            OrderItem(product_name="Gadget", quantity=1, unit_price=49.99),
        ],
        discount_percent=10
    )

    print(f"Order #{order.id}")
    for item in order.items:
        print(f"  {item.product_name}: {item.quantity} x {item.unit_price}€ = {item.subtotal}€")
    print(f"  Total avant remise : {order.total_before_discount:.2f}€")
    print(f"  Remise : {order.discount_percent}%")
    print(f"  Total final : {order.total:.2f}€")


    # =========================================================================
    # 9. Configuration du modèle
    # =========================================================================

    print("\n" + "=" * 60)
    print("9. CONFIGURATION DU MODÈLE")
    print("=" * 60)

    class StrictUser(BaseModel):
        model_config = ConfigDict(
            strict=True,           # Pas de coercion
            extra="forbid",        # Interdit les champs supplémentaires
            frozen=True,           # Immutable
        )

        name: str
        age: int

    print("Mode strict :")
    user = StrictUser(name="Alice", age=30)
    print(f"  Création OK : {user}")

    try:
        StrictUser(name="Bob", age="25")  # String au lieu de int
    except Exception as e:
        print(f"  Strict mode error : type incorrect détecté")

    try:
        StrictUser(name="Charlie", age=25, extra_field="oops")
    except Exception as e:
        print(f"  Extra forbid error : champ inconnu détecté")

    try:
        user.name = "Modified"
    except Exception as e:
        print(f"  Frozen error : modification interdite")


    # =========================================================================
    # 10. Quand utiliser Pydantic ?
    # =========================================================================

    print("\n" + "=" * 60)
    print("10. QUAND UTILISER PYDANTIC ?")
    print("=" * 60)

    print("""
✅ CAS D'USAGE IDÉAUX :
• API endpoints - validation des données utilisateur
• Configuration externe (fichiers, variables d'environnement)
• Parsing de données JSON/XML externes
• Webhooks et intégrations tierces
• Validation de formulaires

❌ À ÉVITER QUAND :
• Structures de données purement internes → dataclass
• Performance ultra-critique sans validation → dataclass
• Aucune dépendance externe souhaitée → dataclass

💡 CONSEIL :
• Pydantic aux "frontières" de l'application
• dataclass pour le "cœur" du domaine
""")

else:
    print("\nExemples non disponibles sans Pydantic.")
    print("Installation : pip install pydantic[email]")
