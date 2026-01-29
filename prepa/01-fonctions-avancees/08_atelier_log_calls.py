"""
Atelier 1.1 : Décorateur @log_calls
===================================

Exercice : Créer un décorateur qui log les appels de fonction
avec les arguments, le résultat et le temps d'exécution.
"""

from functools import wraps
import time


# =============================================================================
# EXERCICE
# =============================================================================

# TODO : Implémentez le décorateur @log_calls qui :
# - Affiche le nom de la fonction appelée
# - Affiche les arguments reçus
# - Affiche la valeur de retour
# - Mesure le temps d'exécution

def log_calls(func):
    """
    Décorateur qui log les appels de fonction.

    Exemple de sortie attendue :
    [LOG] Appel de calculer(5, 3, operation='add')
    [LOG] Résultat: 8 (en 0.0001s)
    """
    # TODO : Implémentez le wrapper
    pass


# =============================================================================
# SOLUTION
# =============================================================================

def log_calls_solution(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        # Formater les arguments
        args_str = ", ".join(repr(a) for a in args)
        kwargs_str = ", ".join(f"{k}={v!r}" for k, v in kwargs.items())
        all_args = ", ".join(filter(None, [args_str, kwargs_str]))

        print(f"[LOG] Appel de {func.__name__}({all_args})")

        debut = time.perf_counter()
        resultat = func(*args, **kwargs)
        duree = time.perf_counter() - debut

        print(f"[LOG] Résultat: {resultat} (en {duree:.4f}s)")
        return resultat
    return wrapper


# =============================================================================
# TESTS
# =============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("DÉMONSTRATION DU DÉCORATEUR @log_calls")
    print("=" * 60)

    @log_calls_solution
    def calculer(x, y, operation="add"):
        if operation == "add":
            return x + y
        return x * y

    @log_calls_solution
    def saluer(nom, enthousiaste=False):
        message = f"Bonjour, {nom}"
        if enthousiaste:
            message += " !!!"
        return message

    @log_calls_solution
    def operation_lente():
        time.sleep(0.5)
        return "Terminé"

    print("\n--- Test 1 : calculer(5, 3, operation='add') ---")
    calculer(5, 3, operation="add")

    print("\n--- Test 2 : calculer(4, 7, operation='mul') ---")
    calculer(4, 7, operation="mul")

    print("\n--- Test 3 : saluer('Alice') ---")
    saluer("Alice")

    print("\n--- Test 4 : saluer('Bob', enthousiaste=True) ---")
    saluer("Bob", enthousiaste=True)

    print("\n--- Test 5 : operation_lente() ---")
    operation_lente()

    print("\n" + "=" * 60)
    print("EXERCICE BONUS : Ajouter un niveau de log paramétrable")
    print("=" * 60)

    # Version avec paramètre
    def log_calls_niveau(niveau="INFO"):
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                args_str = ", ".join(repr(a) for a in args)
                kwargs_str = ", ".join(f"{k}={v!r}" for k, v in kwargs.items())
                all_args = ", ".join(filter(None, [args_str, kwargs_str]))

                print(f"[{niveau}] Appel de {func.__name__}({all_args})")

                debut = time.perf_counter()
                resultat = func(*args, **kwargs)
                duree = time.perf_counter() - debut

                print(f"[{niveau}] Résultat: {resultat} (en {duree:.4f}s)")
                return resultat
            return wrapper
        return decorator

    @log_calls_niveau(niveau="DEBUG")
    def fonction_debug():
        return 42

    @log_calls_niveau(niveau="ERROR")
    def fonction_error():
        return "Erreur simulée"

    print("\n--- Avec @log_calls_niveau(niveau='DEBUG') ---")
    fonction_debug()

    print("\n--- Avec @log_calls_niveau(niveau='ERROR') ---")
    fonction_error()
