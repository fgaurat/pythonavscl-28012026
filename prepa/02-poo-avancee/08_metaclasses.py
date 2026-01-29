"""
Métaclasses
===========

Comprendre et utiliser les métaclasses en Python.
"""

# =============================================================================
# 1. Les classes sont des objets
# =============================================================================

print("=" * 60)
print("1. LES CLASSES SONT DES OBJETS")
print("=" * 60)


class MaClasse:
    pass


print(f"type(MaClasse) = {type(MaClasse)}")
print(f"isinstance(MaClasse, type) = {isinstance(MaClasse, type)}")

print("""
Hiérarchie :
  type (métaclasse)
    ↓ instancie
  MaClasse (classe)
    ↓ instancie
  obj (instance)
""")

obj = MaClasse()
print(f"type(obj) = {type(obj)}")
print(f"type(type(obj)) = {type(type(obj))}")


# =============================================================================
# 2. Création dynamique de classes avec type
# =============================================================================

print("=" * 60)
print("2. CRÉATION DYNAMIQUE AVEC TYPE")
print("=" * 60)


# Création classique
class Chien:
    espece = "Canis lupus"

    def aboyer(self):
        return "Wouf !"


# Création dynamique équivalente
def aboyer(self):
    return "Wouf !"


ChienDynamique = type(
    "ChienDynamique",          # Nom de la classe
    (),                         # Classes parentes (tuple)
    {                           # Attributs et méthodes
        "espece": "Canis lupus",
        "aboyer": aboyer
    }
)

rex = Chien()
max_ = ChienDynamique()

print(f"Chien().aboyer() = '{rex.aboyer()}'")
print(f"ChienDynamique().aboyer() = '{max_.aboyer()}'")
print(f"Chien.espece = '{Chien.espece}'")
print(f"ChienDynamique.espece = '{ChienDynamique.espece}'")


# =============================================================================
# 3. Métaclasse personnalisée basique
# =============================================================================

print("\n" + "=" * 60)
print("3. MÉTACLASSE PERSONNALISÉE BASIQUE")
print("=" * 60)


class MaMeta(type):
    """Métaclasse personnalisée."""

    def __new__(mcs, name, bases, namespace):
        """Appelé lors de la création de la classe."""
        print(f"  MaMeta.__new__ : création de {name}")

        # Modifier le namespace avant création
        namespace["_meta_info"] = f"Créé par MaMeta"
        namespace["_attributs_originaux"] = list(namespace.keys())

        # Créer la classe
        return super().__new__(mcs, name, bases, namespace)

    def __init__(cls, name, bases, namespace):
        """Appelé après la création de la classe."""
        print(f"  MaMeta.__init__ : initialisation de {name}")
        super().__init__(name, bases, namespace)


print("Définition de ClasseAvecMeta :")


class ClasseAvecMeta(metaclass=MaMeta):
    attribut = "valeur"

    def methode(self):
        pass


print(f"\nClasseAvecMeta._meta_info = '{ClasseAvecMeta._meta_info}'")
print(f"ClasseAvecMeta._attributs_originaux = {ClasseAvecMeta._attributs_originaux}")


# =============================================================================
# 4. Cas d'usage : enregistrement automatique
# =============================================================================

print("\n" + "=" * 60)
print("4. CAS D'USAGE : ENREGISTREMENT AUTOMATIQUE")
print("=" * 60)


class PluginRegistry(type):
    """Métaclasse qui enregistre automatiquement les plugins."""
    _plugins = {}

    def __new__(mcs, name, bases, namespace):
        cls = super().__new__(mcs, name, bases, namespace)

        # Ne pas enregistrer la classe de base
        if bases:  # Si ce n'est pas la classe racine
            mcs._plugins[name] = cls
            print(f"  Plugin enregistré : {name}")

        return cls

    @classmethod
    def get_plugins(mcs):
        return mcs._plugins.copy()


class Plugin(metaclass=PluginRegistry):
    """Classe de base pour les plugins."""

    def execute(self):
        raise NotImplementedError


print("Définition des plugins :")


class PluginA(Plugin):
    def execute(self):
        return "Exécution de A"


class PluginB(Plugin):
    def execute(self):
        return "Exécution de B"


class PluginC(Plugin):
    def execute(self):
        return "Exécution de C"


print(f"\nPlugins enregistrés : {list(PluginRegistry.get_plugins().keys())}")

# Utilisation
for name, plugin_cls in PluginRegistry.get_plugins().items():
    plugin = plugin_cls()
    print(f"  {name}.execute() = '{plugin.execute()}'")


# =============================================================================
# 5. Cas d'usage : validation des attributs
# =============================================================================

print("\n" + "=" * 60)
print("5. CAS D'USAGE : VALIDATION DES ATTRIBUTS")
print("=" * 60)


class ValidatedMeta(type):
    """Métaclasse qui valide les attributs requis."""

    def __new__(mcs, name, bases, namespace):
        # Récupérer les attributs requis
        required = namespace.get('_required_attrs', [])

        # Vérifier (sauf pour les classes de base)
        if bases and required:
            for attr in required:
                if attr not in namespace and not any(
                    hasattr(base, attr) for base in bases
                ):
                    raise TypeError(
                        f"La classe {name} doit définir l'attribut '{attr}'"
                    )

        return super().__new__(mcs, name, bases, namespace)


class Model(metaclass=ValidatedMeta):
    _required_attrs = []


class User(Model):
    _required_attrs = ['table_name', 'primary_key']
    table_name = "users"
    primary_key = "id"


print(f"User.table_name = '{User.table_name}'")
print(f"User.primary_key = '{User.primary_key}'")

print("\nTentative de créer une classe sans les attributs requis :")
try:
    class BadModel(Model):
        _required_attrs = ['table_name']
        # Oubli de définir table_name !
        pass
except TypeError as e:
    print(f"  TypeError : {e}")


# =============================================================================
# 6. Cas d'usage : Singleton avec métaclasse
# =============================================================================

print("\n" + "=" * 60)
print("6. CAS D'USAGE : SINGLETON")
print("=" * 60)


class SingletonMeta(type):
    """Métaclasse qui implémente le pattern Singleton."""
    _instances = {}

    def __call__(cls, *args, **kwargs):
        """Appelé lors de l'instanciation."""
        if cls not in cls._instances:
            print(f"  Création de l'instance unique de {cls.__name__}")
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        else:
            print(f"  Retour de l'instance existante de {cls.__name__}")
        return cls._instances[cls]


class Database(metaclass=SingletonMeta):
    def __init__(self, connection_string):
        self.connection_string = connection_string


print("Première instanciation :")
db1 = Database("postgresql://localhost/db")

print("\nDeuxième instanciation :")
db2 = Database("mysql://localhost/db")

print(f"\ndb1 is db2 : {db1 is db2}")
print(f"connection_string : {db2.connection_string}")  # postgresql (le premier)


# =============================================================================
# 7. __init_subclass__ : alternative moderne
# =============================================================================

print("\n" + "=" * 60)
print("7. __init_subclass__ : ALTERNATIVE MODERNE")
print("=" * 60)


class PluginV2:
    """Alternative aux métaclasses avec __init_subclass__."""
    _plugins = {}

    def __init_subclass__(cls, plugin_name=None, **kwargs):
        """Appelé automatiquement quand une classe hérite de PluginV2."""
        super().__init_subclass__(**kwargs)

        name = plugin_name or cls.__name__
        PluginV2._plugins[name] = cls
        print(f"  Plugin V2 enregistré : {name}")


print("Définition des plugins V2 :")


class AuthPlugin(PluginV2, plugin_name="auth"):
    pass


class CachePlugin(PluginV2):  # Utilise le nom de classe par défaut
    pass


class LogPlugin(PluginV2, plugin_name="logger"):
    pass


print(f"\nPlugins V2 : {list(PluginV2._plugins.keys())}")


# =============================================================================
# 8. __init_subclass__ avec validation
# =============================================================================

print("\n" + "=" * 60)
print("8. __init_subclass__ AVEC VALIDATION")
print("=" * 60)


class BaseHandler:
    """Classe de base avec validation des sous-classes."""

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)

        # Vérifier que handle() est implémenté
        if not hasattr(cls, 'handle') or cls.handle is BaseHandler.handle:
            raise TypeError(f"{cls.__name__} doit implémenter handle()")

        # Vérifier que pattern est défini
        if not hasattr(cls, 'pattern'):
            raise TypeError(f"{cls.__name__} doit définir 'pattern'")

        print(f"  Handler validé : {cls.__name__} (pattern: {cls.pattern})")

    def handle(self):
        raise NotImplementedError


print("Création de handlers valides :")


class EmailHandler(BaseHandler):
    pattern = r".*@.*\..*"

    def handle(self):
        return "Traitement email"


class PhoneHandler(BaseHandler):
    pattern = r"\+?\d{10,}"

    def handle(self):
        return "Traitement téléphone"


print("\nTentative de créer un handler invalide :")
try:
    class BadHandler(BaseHandler):
        # Oubli de pattern et handle()
        pass
except TypeError as e:
    print(f"  TypeError : {e}")


# =============================================================================
# 9. Quand utiliser les métaclasses ?
# =============================================================================

print("\n" + "=" * 60)
print("9. QUAND UTILISER LES MÉTACLASSES ?")
print("=" * 60)

print("""
CAS LÉGITIMES :
🔧 Frameworks (Django ORM, SQLAlchemy, Pydantic)
📝 Enregistrement automatique de classes
✅ Validation de la structure des classes
🔄 Transformation automatique de méthodes

ALTERNATIVES PLUS SIMPLES :
┌──────────────────────────────┬─────────────────────────┐
│ Besoin                       │ Solution préférée       │
├──────────────────────────────┼─────────────────────────┤
│ Modifier une méthode         │ Décorateur              │
│ Ajouter des attributs        │ __init_subclass__       │
│ Valider les types            │ Type hints + Pydantic   │
│ Singleton                    │ Décorateur ou module    │
└──────────────────────────────┴─────────────────────────┘

Citation de Tim Peters :
"Les métaclasses sont une magie plus profonde que 99% des
utilisateurs n'auront jamais besoin."

RÈGLE : Préférez __init_subclass__ quand c'est possible !
""")
