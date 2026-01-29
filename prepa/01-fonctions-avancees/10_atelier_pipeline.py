"""
Atelier 2 : Pipeline de transformations
=======================================

Exercice : Créer un système de pipeline où les transformations
sont appliquées séquentiellement via des décorateurs.
"""

from functools import wraps


# =============================================================================
# EXERCICE
# =============================================================================

# TODO : Implémentez les décorateurs @pipeline et @transformation qui permettent :
# - D'appliquer une série de transformations à une valeur
# - Les transformations s'appliquent dans l'ordre des décorateurs

# Exemple d'utilisation attendue :
# @pipeline
# @transformation(lambda x: x.strip())
# @transformation(lambda x: x.lower())
# @transformation(lambda x: x.replace(" ", "_"))
# def nettoyer_identifiant(texte):
#     return texte
#
# print(nettoyer_identifiant("  Hello World  "))
# # "hello_world"


def transformation(transform_func):
    """Ajoute une transformation au pipeline."""
    # TODO : Implémentez le décorateur
    pass


def pipeline(func):
    """Marque une fonction comme point d'entrée du pipeline."""
    # TODO : Implémentez le décorateur
    pass


# =============================================================================
# SOLUTION
# =============================================================================

def transformation_solution(transform_func):
    """Ajoute une transformation au pipeline."""
    def decorator(func):
        @wraps(func)
        def wrapper(data):
            # Appliquer d'abord la fonction existante
            result = func(data)
            # Puis appliquer cette transformation
            return transform_func(result)
        return wrapper
    return decorator


def pipeline_solution(func):
    """Marque une fonction comme point d'entrée du pipeline."""
    @wraps(func)
    def wrapper(data):
        return func(data)
    return wrapper


# =============================================================================
# TESTS
# =============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("DÉMONSTRATION DU PIPELINE DE TRANSFORMATIONS")
    print("=" * 60)

    # Les décorateurs s'appliquent de bas en haut :
    # 1. pipeline(func) - point d'entrée
    # 2. transformation(replace) - appliqué en 3ème
    # 3. transformation(lower) - appliqué en 2ème
    # 4. transformation(strip) - appliqué en 1er

    @pipeline_solution
    @transformation_solution(lambda x: x.strip())
    @transformation_solution(lambda x: x.lower())
    @transformation_solution(lambda x: x.replace(" ", "_"))
    def nettoyer_identifiant(texte):
        return texte

    print("\n--- Test nettoyer_identifiant ---")
    tests = [
        "  Hello World  ",
        "  PYTHON Programming  ",
        "   Mixed CASE Text   ",
    ]

    for test in tests:
        result = nettoyer_identifiant(test)
        print(f"'{test}' -> '{result}'")

    print("\n" + "=" * 60)
    print("PIPELINE DE VALIDATION")
    print("=" * 60)

    def validate_not_empty(value):
        if not value or not value.strip():
            raise ValueError("La valeur ne peut pas être vide")
        return value

    def validate_length(max_length):
        def validator(value):
            if len(value) > max_length:
                raise ValueError(f"Longueur max: {max_length}, reçu: {len(value)}")
            return value
        return validator

    def validate_alphanumeric(value):
        clean = value.replace("_", "").replace("-", "")
        if not clean.isalnum():
            raise ValueError("Seuls les caractères alphanumériques, _ et - sont autorisés")
        return value

    @pipeline_solution
    @transformation_solution(lambda x: x.strip())
    @transformation_solution(lambda x: x.lower())
    @transformation_solution(validate_not_empty)
    @transformation_solution(validate_length(20))
    @transformation_solution(validate_alphanumeric)
    def creer_username(texte):
        return texte

    print("\n--- Test creer_username ---")
    tests_valides = ["Alice", "  Bob  ", "User_123"]
    tests_invalides = ["", "A" * 25, "User@Name!"]

    print("\nTests valides :")
    for test in tests_valides:
        try:
            result = creer_username(test)
            print(f"  '{test}' -> '{result}'")
        except ValueError as e:
            print(f"  '{test}' -> Erreur: {e}")

    print("\nTests invalides :")
    for test in tests_invalides:
        try:
            result = creer_username(test)
            print(f"  '{test}' -> '{result}'")
        except ValueError as e:
            print(f"  '{test}' -> Erreur: {e}")

    print("\n" + "=" * 60)
    print("PIPELINE DE TRAITEMENT DE DONNÉES")
    print("=" * 60)

    def parse_json_string(value):
        import json
        if isinstance(value, str):
            return json.loads(value)
        return value

    def extract_field(field_name):
        def extractor(data):
            return data.get(field_name, None)
        return extractor

    def default_value(default):
        def setter(value):
            return value if value is not None else default
        return setter

    @pipeline_solution
    @transformation_solution(parse_json_string)
    @transformation_solution(extract_field("name"))
    @transformation_solution(default_value("Inconnu"))
    @transformation_solution(lambda x: x.title())
    def get_formatted_name(data):
        return data

    print("\n--- Test get_formatted_name ---")
    tests = [
        '{"name": "john doe", "age": 30}',
        '{"age": 25}',
        '{"name": "ALICE MARTIN"}',
    ]

    for test in tests:
        result = get_formatted_name(test)
        print(f"  {test[:40]}... -> '{result}'")

    print("\n" + "=" * 60)
    print("PIPELINE NUMÉRIQUE")
    print("=" * 60)

    @pipeline_solution
    @transformation_solution(lambda x: abs(x))
    @transformation_solution(lambda x: x ** 2)
    @transformation_solution(lambda x: x + 10)
    @transformation_solution(lambda x: round(x, 2))
    def transformer_nombre(n):
        return n

    print("\n--- Test transformer_nombre (abs -> carré -> +10 -> round) ---")
    for n in [-3, 2.5, -4.7, 0]:
        result = transformer_nombre(n)
        print(f"  {n} -> {result}")
