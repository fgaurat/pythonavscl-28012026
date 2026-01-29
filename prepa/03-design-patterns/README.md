# Design Patterns en Python

Ce dossier contient les exemples de code pour la section "Design Patterns en Python".

## Structure des fichiers

| Fichier | Description |
|---------|-------------|
| `01_factory.py` | Pattern Factory et Abstract Factory |
| `02_singleton.py` | Pattern Singleton (décorateur, métaclasse, module) |
| `03_adapter.py` | Pattern Adapter pour interfaces incompatibles |
| `04_observer.py` | Pattern Observer et événements |
| `05_strategy.py` | Pattern Strategy avec classes et fonctions |
| `06_patterns_pythoniques.py` | Duck typing, EAFP, Protocoles |
| `07_dataclasses.py` | Dataclasses : syntaxe, options, fonctions |
| `08_pydantic.py` | Pydantic : validation, types avancés, sérialisation |
| `09_atelier_notification.py` | Atelier : système de notification |
| `10_atelier_ecommerce.py` | Atelier : modélisation e-commerce |

## Prérequis

Certains exemples nécessitent Pydantic :

```bash
pip install pydantic[email]
```

## Exécution

Chaque fichier peut être exécuté indépendamment :

```bash
python 01_factory.py
python 02_singleton.py
# etc.
```

## Patterns classiques

### Factory
Création d'objets sans exposer la logique au client.
- Factory Method avec dictionnaire
- Registry avec décorateur
- Abstract Factory

### Singleton
Instance unique garantie.
- Décorateur (recommandé)
- Métaclasse
- Module Python (naturellement singleton)

### Adapter
Pont entre interfaces incompatibles.
- Wrapper de classes existantes
- Conversion de formats de données

### Observer
Notification automatique lors de changements d'état.
- Classique avec ABC
- Pythonique avec callbacks
- Événements nommés

### Strategy
Algorithmes interchangeables.
- Avec classes ABC
- Avec fonctions (pythonique)
- Avec closures paramétrables

## Patterns pythoniques

### Duck Typing
"If it walks like a duck and quacks like a duck..."
- Pas de vérification de type explicite
- Focus sur le comportement

### EAFP vs LBYL
- **EAFP** : Easier to Ask Forgiveness than Permission (pythonique)
- **LBYL** : Look Before You Leap

### Protocoles (typing.Protocol)
Duck typing avec vérification statique.
- Interface structurelle sans héritage
- Compatible avec mypy

## Modélisation de données

### Dataclasses
Pour les structures de données internes :
- Génération automatique de `__init__`, `__repr__`, `__eq__`
- Options : `frozen`, `order`, `slots`
- Fonctions : `asdict`, `astuple`, `fields`, `replace`

### Pydantic
Pour les données externes avec validation :
- Validation automatique des types
- Coercion intelligente
- Types avancés (EmailStr, HttpUrl)
- Validateurs personnalisés
- Sérialisation JSON native

### Quand choisir ?

| Critère | Dataclass | Pydantic |
|---------|-----------|----------|
| Données internes | ✅ | ⚠️ |
| Données externes | ⚠️ | ✅ |
| Validation | ❌ | ✅ |
| Performance | ✅✅ | ✅ |
| Dépendances | ✅ (stdlib) | ❌ (pip) |
