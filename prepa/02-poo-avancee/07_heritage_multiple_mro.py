"""
Héritage Multiple et MRO
========================

Compréhension de l'héritage multiple, du problème du diamant,
et du Method Resolution Order (MRO).
"""

# =============================================================================
# 1. Héritage multiple basique
# =============================================================================

print("=" * 60)
print("1. HÉRITAGE MULTIPLE BASIQUE")
print("=" * 60)


class A:
    def methode(self):
        print("A.methode")


class B:
    def methode(self):
        print("B.methode")


class C(A, B):  # Hérite de A et B
    pass


c = C()
c.methode()  # A.methode - A vient en premier
print(f"C.__mro__ = {[cls.__name__ for cls in C.__mro__]}")


# =============================================================================
# 2. Le problème du diamant
# =============================================================================

print("\n" + "=" * 60)
print("2. LE PROBLÈME DU DIAMANT")
print("=" * 60)

print("""
       A
      / \\
     B   C
      \\ /
       D
""")


class A:
    def methode(self):
        print("A.methode")


class B(A):
    def methode(self):
        print("B.methode")
        super().methode()


class C(A):
    def methode(self):
        print("C.methode")
        super().methode()


class D(B, C):
    def methode(self):
        print("D.methode")
        super().methode()


print("D().methode() :")
D().methode()
print("\nMRO de D :", [cls.__name__ for cls in D.__mro__])
print("Remarque : A n'est appelé qu'une seule fois !")


# =============================================================================
# 3. Comprendre le MRO
# =============================================================================

print("\n" + "=" * 60)
print("3. COMPRENDRE LE MRO")
print("=" * 60)


class X:
    pass


class Y:
    pass


class Z:
    pass


class A(X, Y):
    pass


class B(Y, Z):
    pass


class M(A, B):
    pass


print(f"MRO de X : {[c.__name__ for c in X.__mro__]}")
print(f"MRO de A : {[c.__name__ for c in A.__mro__]}")
print(f"MRO de B : {[c.__name__ for c in B.__mro__]}")
print(f"MRO de M : {[c.__name__ for c in M.__mro__]}")

print("""
Règles du MRO (C3 linearization) :
1. Les enfants viennent avant les parents
2. L'ordre des parents dans la déclaration est respecté
3. Chaque classe n'apparaît qu'une seule fois
""")


# =============================================================================
# 4. super() avec héritage multiple
# =============================================================================

print("=" * 60)
print("4. SUPER() AVEC HÉRITAGE MULTIPLE")
print("=" * 60)


class Base:
    def __init__(self):
        print("  Base.__init__")


class A(Base):
    def __init__(self):
        print("  A.__init__")
        super().__init__()


class B(Base):
    def __init__(self):
        print("  B.__init__")
        super().__init__()


class C(A, B):
    def __init__(self):
        print("  C.__init__")
        super().__init__()


print("C() - Ordre des appels :")
c = C()
print(f"\nMRO de C : {[cls.__name__ for cls in C.__mro__]}")
print("super() suit le MRO, pas la hiérarchie directe !")


# =============================================================================
# 5. Mixins : héritage multiple bien utilisé
# =============================================================================

print("\n" + "=" * 60)
print("5. MIXINS")
print("=" * 60)


class JsonMixin:
    """Mixin ajoutant la sérialisation JSON."""

    def to_json(self):
        import json
        return json.dumps(self.__dict__, default=str)


class LogMixin:
    """Mixin ajoutant des capacités de logging."""

    def log(self, message):
        print(f"  [{self.__class__.__name__}] {message}")


class ComparableMixin:
    """Mixin pour les comparaisons basées sur _compare_key()."""

    def __lt__(self, other):
        return self._compare_key() < other._compare_key()

    def __le__(self, other):
        return self._compare_key() <= other._compare_key()

    def __eq__(self, other):
        return self._compare_key() == other._compare_key()

    def __gt__(self, other):
        return self._compare_key() > other._compare_key()


class Utilisateur(JsonMixin, LogMixin):
    def __init__(self, nom, email):
        self.nom = nom
        self.email = email


user = Utilisateur("Alice", "alice@example.com")
print(f"to_json() : {user.to_json()}")
user.log("Connexion réussie")


class Produit(ComparableMixin):
    def __init__(self, nom, prix):
        self.nom = nom
        self.prix = prix

    def _compare_key(self):
        return self.prix

    def __repr__(self):
        return f"Produit({self.nom!r}, {self.prix}€)"


produits = [
    Produit("Livre", 15),
    Produit("Téléphone", 500),
    Produit("Stylo", 2),
]

print(f"\nProduits triés par prix : {sorted(produits)}")


# =============================================================================
# 6. Mixins avec arguments coopératifs
# =============================================================================

print("\n" + "=" * 60)
print("6. MIXINS AVEC ARGUMENTS COOPÉRATIFS")
print("=" * 60)


class TimestampMixin:
    """Ajoute des timestamps automatiques."""

    def __init__(self, *args, **kwargs):
        from datetime import datetime
        super().__init__(*args, **kwargs)
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

    def touch(self):
        from datetime import datetime
        self.updated_at = datetime.now()


class ValidationMixin:
    """Ajoute la validation."""

    _validators = {}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.validate()

    def validate(self):
        for name, validator in self._validators.items():
            value = getattr(self, name, None)
            if not validator(value):
                raise ValueError(f"Validation échouée pour {name}: {value}")


class BaseModel:
    """Classe de base pour les modèles."""

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)


class Article(TimestampMixin, ValidationMixin, BaseModel):
    _validators = {
        "titre": lambda x: x and len(x) > 0,
        "contenu": lambda x: x and len(x) >= 10,
    }


print("Création d'un Article valide :")
article = Article(titre="Mon Article", contenu="Contenu de l'article avec au moins 10 caractères")
print(f"  titre: {article.titre}")
print(f"  created_at: {article.created_at}")

print("\nCréation d'un Article invalide :")
try:
    article_invalide = Article(titre="", contenu="Court")
except ValueError as e:
    print(f"  Erreur : {e}")


# =============================================================================
# 7. Ordre des mixins
# =============================================================================

print("\n" + "=" * 60)
print("7. ORDRE DES MIXINS")
print("=" * 60)


class MixinA:
    def action(self):
        print("  MixinA.action")
        super().action()


class MixinB:
    def action(self):
        print("  MixinB.action")
        super().action()


class Base:
    def action(self):
        print("  Base.action")


# Ordre différent = comportement différent
class ClasseAB(MixinA, MixinB, Base):
    def action(self):
        print("  ClasseAB.action")
        super().action()


class ClasseBA(MixinB, MixinA, Base):
    def action(self):
        print("  ClasseBA.action")
        super().action()


print("ClasseAB (MixinA, MixinB, Base) :")
ClasseAB().action()
print(f"  MRO : {[c.__name__ for c in ClasseAB.__mro__]}")

print("\nClasseBA (MixinB, MixinA, Base) :")
ClasseBA().action()
print(f"  MRO : {[c.__name__ for c in ClasseBA.__mro__]}")


# =============================================================================
# 8. Bonnes pratiques
# =============================================================================

print("\n" + "=" * 60)
print("8. BONNES PRATIQUES")
print("=" * 60)

print("""
À FAIRE :
✅ Utiliser des mixins pour des fonctionnalités orthogonales
✅ Garder les mixins simples et focalisés
✅ Toujours appeler super() pour permettre la coopération
✅ Documenter les dépendances des mixins
✅ Nommer les mixins avec le suffixe "Mixin"

À ÉVITER :
❌ Créer des hiérarchies profondes avec héritage multiple
❌ Hériter de plusieurs classes avec des méthodes identiques
   (sauf si c'est intentionnel)
❌ Utiliser l'héritage multiple quand la composition suffit

RÈGLE D'OR : Préférer la composition à l'héritage
""")


# =============================================================================
# 9. Composition vs Héritage
# =============================================================================

print("=" * 60)
print("9. COMPOSITION VS HÉRITAGE")
print("=" * 60)


# Avec héritage (rigide)
class LoggableUser_Heritage(LogMixin):
    def __init__(self, nom):
        self.nom = nom


# Avec composition (flexible)
class Logger:
    def log(self, obj, message):
        print(f"  [{obj.__class__.__name__}] {message}")


class LoggableUser_Composition:
    def __init__(self, nom, logger=None):
        self.nom = nom
        self.logger = logger or Logger()

    def log(self, message):
        self.logger.log(self, message)


print("Héritage :")
user1 = LoggableUser_Heritage("Alice")
user1.log("Action")

print("\nComposition (plus flexible) :")
user2 = LoggableUser_Composition("Bob")
user2.log("Action")


# Logger personnalisé
class PrefixLogger:
    def __init__(self, prefix):
        self.prefix = prefix

    def log(self, obj, message):
        print(f"  {self.prefix} [{obj.__class__.__name__}] {message}")


user3 = LoggableUser_Composition("Charlie", logger=PrefixLogger(">>>"))
user3.log("Action avec logger personnalisé")
