"""
Atelier 1.2 : Décorateur @require_positive
==========================================

Exercice : Créer un décorateur qui vérifie que tous les arguments
numériques sont positifs.
"""

from functools import wraps
import inspect


# =============================================================================
# EXERCICE
# =============================================================================

# TODO : Implémentez le décorateur @require_positive qui :
# - Vérifie que tous les arguments numériques (int, float) sont >= 0
# - Lève une ValueError si un argument est négatif
# - Fonctionne avec les arguments positionnels et nommés

def require_positive(func):
    """
    Décorateur qui vérifie que tous les arguments numériques sont positifs.

    Exemple :
    @require_positive
    def calculer_racine(nombre):
        return nombre ** 0.5

    calculer_racine(16)   # 4.0
    calculer_racine(-4)   # ValueError: nombre doit être positif, reçu: -4
    """
    # TODO : Implémentez le wrapper
    pass


# =============================================================================
# SOLUTION
# =============================================================================

def require_positive_solution(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        sig = inspect.signature(func)
        params = list(sig.parameters.keys())

        # Vérifier les arguments positionnels
        for i, arg in enumerate(args):
            if isinstance(arg, (int, float)) and arg < 0:
                param_name = params[i] if i < len(params) else f"arg{i}"
                raise ValueError(f"{param_name} doit être positif, reçu: {arg}")

        # Vérifier les arguments nommés
        for name, value in kwargs.items():
            if isinstance(value, (int, float)) and value < 0:
                raise ValueError(f"{name} doit être positif, reçu: {value}")

        return func(*args, **kwargs)
    return wrapper


# =============================================================================
# TESTS
# =============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("DÉMONSTRATION DU DÉCORATEUR @require_positive")
    print("=" * 60)

    @require_positive_solution
    def calculer_racine(nombre):
        """Calcule la racine carrée d'un nombre."""
        return nombre ** 0.5

    @require_positive_solution
    def calculer_aire(longueur, largeur):
        """Calcule l'aire d'un rectangle."""
        return longueur * largeur

    @require_positive_solution
    def calculer_volume(longueur, largeur, hauteur=1):
        """Calcule le volume d'un parallélépipède."""
        return longueur * largeur * hauteur

    print("\n--- Tests valides ---")

    print(f"calculer_racine(16) = {calculer_racine(16)}")
    print(f"calculer_racine(2.25) = {calculer_racine(2.25)}")
    print(f"calculer_aire(5, 3) = {calculer_aire(5, 3)}")
    print(f"calculer_volume(2, 3, hauteur=4) = {calculer_volume(2, 3, hauteur=4)}")

    print("\n--- Tests avec valeurs négatives ---")

    tests_negatifs = [
        ("calculer_racine(-4)", lambda: calculer_racine(-4)),
        ("calculer_aire(5, -3)", lambda: calculer_aire(5, -3)),
        ("calculer_aire(-5, 3)", lambda: calculer_aire(-5, 3)),
        ("calculer_volume(2, 3, hauteur=-4)", lambda: calculer_volume(2, 3, hauteur=-4)),
    ]

    for description, test_func in tests_negatifs:
        try:
            test_func()
            print(f"{description} : Pas d'erreur (inattendu)")
        except ValueError as e:
            print(f"{description} : ValueError - {e}")

    print("\n" + "=" * 60)
    print("EXERCICE BONUS : Permettre zéro (>= 0 vs > 0)")
    print("=" * 60)

    def require_strictly_positive(func):
        """Variante qui exige des valeurs strictement positives (> 0)."""
        @wraps(func)
        def wrapper(*args, **kwargs):
            sig = inspect.signature(func)
            params = list(sig.parameters.keys())

            for i, arg in enumerate(args):
                if isinstance(arg, (int, float)) and arg <= 0:
                    param_name = params[i] if i < len(params) else f"arg{i}"
                    raise ValueError(
                        f"{param_name} doit être strictement positif, reçu: {arg}"
                    )

            for name, value in kwargs.items():
                if isinstance(value, (int, float)) and value <= 0:
                    raise ValueError(
                        f"{name} doit être strictement positif, reçu: {value}"
                    )

            return func(*args, **kwargs)
        return wrapper

    @require_strictly_positive
    def diviser(a, b):
        return a / b

    print("\n--- Tests @require_strictly_positive ---")
    print(f"diviser(10, 2) = {diviser(10, 2)}")

    try:
        diviser(10, 0)
    except ValueError as e:
        print(f"diviser(10, 0) : ValueError - {e}")

    print("\n" + "=" * 60)
    print("EXERCICE BONUS 2 : Spécifier quels paramètres valider")
    print("=" * 60)

    def require_positive_params(*param_names):
        """Valide uniquement les paramètres spécifiés."""
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                sig = inspect.signature(func)
                params = list(sig.parameters.keys())

                # Créer un mapping args -> params
                for i, arg in enumerate(args):
                    if i < len(params) and params[i] in param_names:
                        if isinstance(arg, (int, float)) and arg < 0:
                            raise ValueError(
                                f"{params[i]} doit être positif, reçu: {arg}"
                            )

                for name, value in kwargs.items():
                    if name in param_names:
                        if isinstance(value, (int, float)) and value < 0:
                            raise ValueError(
                                f"{name} doit être positif, reçu: {value}"
                            )

                return func(*args, **kwargs)
            return wrapper
        return decorator

    @require_positive_params("quantite", "prix")
    def vendre(produit, quantite, prix, remise=0):
        """La remise peut être négative (pourquoi pas ?)"""
        total = quantite * prix * (1 - remise)
        return f"{quantite}x {produit} = {total:.2f}€"

    print("\n--- Tests @require_positive_params ---")
    print(vendre("Widget", 5, 10.0, remise=0.1))
    print(vendre("Gadget", 3, 25.0, remise=-0.2))  # Remise négative OK

    try:
        vendre("Widget", -5, 10.0)
    except ValueError as e:
        print(f"Quantité négative : ValueError - {e}")
