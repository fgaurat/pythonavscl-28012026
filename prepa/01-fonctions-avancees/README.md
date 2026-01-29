# Fonctions avancées et idiomes Python

Ce dossier contient les exemples de code pour la section "Fonctions avancées et idiomes Python".

## Structure des fichiers

| Fichier | Description |
|---------|-------------|
| `01_references_mutabilite.py` | Références, mutabilité, pièges des arguments mutables |
| `02_portee_variables.py` | Règle LEGB, `global`, `nonlocal` |
| `03_fonctions_first_class.py` | Fonctions comme objets de première classe |
| `04_closures.py` | Fermetures (closures) et encapsulation |
| `05_decorateurs_base.py` | Introduction aux décorateurs |
| `06_decorateurs_parametres.py` | Décorateurs avec paramètres |
| `07_decorateurs_design_patterns.py` | Patterns Singleton, Observer, Registry, etc. |
| `08_atelier_log_calls.py` | Atelier : décorateur `@log_calls` |
| `09_atelier_require_positive.py` | Atelier : décorateur `@require_positive` |
| `10_atelier_pipeline.py` | Atelier : pipeline de transformations |

## Exécution

Chaque fichier peut être exécuté indépendamment :

```bash
python 01_references_mutabilite.py
python 02_portee_variables.py
# etc.
```

## Concepts clés

### Références et mutabilité
- Variables = références vers des objets
- Types mutables vs immutables
- Piège des arguments mutables par défaut

### Portée des variables (LEGB)
- **L**ocal : variables dans la fonction courante
- **E**nclosing : variables des fonctions englobantes
- **G**lobal : variables au niveau module
- **B**uilt-in : noms Python prédéfinis

### Fonctions first-class
Les fonctions peuvent être :
- Assignées à des variables
- Passées en argument
- Retournées par d'autres fonctions
- Stockées dans des structures de données

### Closures (Fermetures)
Fonctions qui capturent et mémorisent les variables de leur portée englobante.

### Décorateurs
Pattern permettant de modifier le comportement d'une fonction sans modifier son code.

```python
@mon_decorateur
def ma_fonction():
    pass
```

Équivalent à :
```python
ma_fonction = mon_decorateur(ma_fonction)
```
