# Programmation Objet Avancée

Ce dossier contient les exemples de code pour la section "Programmation Objet avancée".

## Structure des fichiers

| Fichier | Description |
|---------|-------------|
| `01_property.py` | `@property`, getter/setter/deleter, `@cached_property` |
| `02_iterateurs.py` | Protocole d'itération, `__iter__`, `__next__` |
| `03_generateurs.py` | `yield`, expressions génératrices, `yield from`, `send()` |
| `04_itertools.py` | Outils `itertools` : chain, islice, groupby, etc. |
| `05_context_managers.py` | `with`, `__enter__`/`__exit__`, `@contextmanager` |
| `06_abc.py` | Classes abstraites, `@abstractmethod`, ABC |
| `07_heritage_multiple_mro.py` | Héritage multiple, MRO, mixins |
| `08_metaclasses.py` | Métaclasses, `type`, `__init_subclass__` |

## Exécution

Chaque fichier peut être exécuté indépendamment :

```bash
python 01_property.py
python 02_iterateurs.py
# etc.
```

## Concepts clés

### @property
- Encapsulation pythonique des attributs
- Validation dans les setters
- Propriétés calculées (lecture seule)
- `@cached_property` pour les calculs coûteux

### Itérateurs et générateurs
- **Itérateur** : objet avec `__iter__()` et `__next__()`
- **Générateur** : fonction avec `yield` (plus simple)
- **Évaluation paresseuse** : économie de mémoire
- `yield from` pour déléguer à un sous-générateur

### Context managers
- Gestion automatique des ressources
- `__enter__` : acquisition
- `__exit__` : libération (même en cas d'exception)
- `@contextmanager` : syntaxe simplifiée avec `yield`

### Classes abstraites (ABC)
- Interfaces explicites et vérifiées
- `@abstractmethod` : méthodes à implémenter
- Erreurs précoces (à l'instanciation)

### Héritage multiple et MRO
- **MRO** : Method Resolution Order (algorithme C3)
- **Mixins** : petites classes réutilisables
- `super()` suit le MRO, pas la hiérarchie directe

### Métaclasses
- "Les classes sont des objets"
- `type` est la métaclasse par défaut
- `__init_subclass__` : alternative moderne et plus simple

## Bonnes pratiques

1. Préférer les générateurs aux listes pour les gros volumes
2. Toujours utiliser `with` pour les ressources (fichiers, connexions)
3. ABC pour les interfaces critiques
4. Mixins plutôt qu'héritage profond
5. `__init_subclass__` plutôt que métaclasses
6. **Composition > Héritage**
