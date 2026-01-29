# Qualité logicielle et bonnes pratiques

Ce dossier contient les exemples de code pour la section "Qualité logicielle".

## Structure des fichiers

| Fichier | Description |
|---------|-------------|
| `01_conventions_style.py` | PEP8, PEP20, conventions de nommage |
| `02_type_hints.py` | Annotations de type, typing, Protocol |
| `03_unittest_base.py` | Module unittest : structure et assertions |
| `04_pytest_base.py` | pytest : syntaxe de base |
| `05_pytest_fixtures.py` | Fixtures et injection de dépendances |
| `06_pytest_parametrize.py` | Paramétrisation et marqueurs |
| `07_tdd_fizzbuzz.py` | TDD : cycle Red-Green-Refactor |
| `08_mocking.py` | Mocking avec unittest.mock et pytest-mock |
| `09_profiling.py` | timeit, cProfile, optimisation |
| `pyproject.toml` | Configuration unifiée des outils |
| `.pre-commit-config.yaml` | Configuration pre-commit |
| `tests/` | Exemples de tests avec conftest.py |

## Prérequis

```bash
# Outils de test
pip install pytest pytest-cov pytest-mock

# Linters et formateurs
pip install ruff mypy

# Pre-commit
pip install pre-commit
```

## Exécution des exemples

Chaque fichier peut être exécuté indépendamment :

```bash
python 01_conventions_style.py
python 02_type_hints.py
# etc.
```

## Exécution des tests

```bash
# Tous les tests
pytest tests/ -v

# Avec couverture
pytest tests/ --cov=. --cov-report=term-missing

# Exclure les tests lents
pytest tests/ -m "not slow"

# Tests d'intégration uniquement
pytest tests/ -m "integration"
```

## Utilisation des linters

### Ruff (recommandé)

```bash
# Lint
ruff check .

# Lint avec correction automatique
ruff check --fix .

# Format
ruff format .
```

### Mypy

```bash
mypy *.py
```

## Configuration pre-commit

```bash
# Installation
pre-commit install

# Exécution manuelle
pre-commit run --all-files

# Mise à jour des hooks
pre-commit autoupdate
```

## Conventions de style (PEP8)

### Nommage

| Type | Convention | Exemple |
|------|------------|---------|
| Modules/packages | snake_case | `mon_module.py` |
| Fonctions/variables | snake_case | `ma_fonction()` |
| Constantes | SCREAMING_SNAKE_CASE | `MAX_SIZE = 100` |
| Classes | PascalCase | `MaClasse` |
| Méthodes "privées" | _préfixe | `_methode_interne()` |

### Imports

```python
# 1. Bibliothèque standard
import os
import sys

# 2. Bibliothèques tierces
import requests
import pandas as pd

# 3. Imports locaux
from mon_projet import utils
```

## pytest : aide-mémoire

### Assertions

```python
assert resultat == attendu
assert item in liste
assert expression
```

### Exceptions

```python
with pytest.raises(ValueError, match="message"):
    fonction_qui_leve()
```

### Fixtures

```python
@pytest.fixture
def ma_fixture():
    # Setup
    resource = create()
    yield resource
    # Teardown
    resource.cleanup()

def test_avec_fixture(ma_fixture):
    assert ma_fixture.ready
```

### Paramétrisation

```python
@pytest.mark.parametrize("input, expected", [
    (1, 2),
    (2, 4),
    (3, 6),
])
def test_double(input, expected):
    assert input * 2 == expected
```

### Marqueurs

```python
@pytest.mark.slow
@pytest.mark.skip(reason="...")
@pytest.mark.skipif(condition, reason="...")
@pytest.mark.xfail(reason="Bug connu")
```

## Mocking : aide-mémoire

```python
from unittest.mock import Mock, patch

# Mock simple
mock = Mock()
mock.return_value = 42
mock.method.return_value = "result"

# Patch
@patch("module.fonction")
def test_avec_patch(mock_fonction):
    mock_fonction.return_value = "mocked"

# side_effect
mock.method.side_effect = Exception("Error")
mock.method.side_effect = [1, 2, 3]  # Valeurs successives

# Vérifications
mock.assert_called_once()
mock.assert_called_with(arg1, arg2)
```

## Profiling : aide-mémoire

```python
import timeit
import cProfile

# timeit
temps = timeit.timeit("expression", number=10000)

# cProfile
cProfile.run('ma_fonction()')

# Décorateur de mesure
@timer
def fonction():
    pass
```

## Quand utiliser quoi ?

| Outil | Quand l'utiliser |
|-------|------------------|
| `unittest` | Projets legacy, compatibilité Python |
| `pytest` | Nouveaux projets (recommandé) |
| `Mock` | Isoler les dépendances externes |
| `timeit` | Micro-benchmarks |
| `cProfile` | Trouver les goulots d'étranglement |
| `ruff` | Linting + formatting (tout-en-un) |
| `mypy` | Vérification des types |
