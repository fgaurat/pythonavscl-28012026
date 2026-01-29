"""
Portée des variables en Python
==============================

Démonstration de la règle LEGB et des mots-clés global/nonlocal.
"""

# =============================================================================
# 1. Règle LEGB - Local, Enclosing, Global, Built-in
# =============================================================================

print("=" * 60)
print("1. RÈGLE LEGB")
print("=" * 60)

x = "global"  # Global


def externe():
    x = "enclosing"  # Enclosing

    def interne():
        x = "local"  # Local
        print(f"  Dans interne() : x = '{x}'")  # "local"

    interne()
    print(f"  Dans externe() : x = '{x}'")  # "enclosing"


externe()
print(f"Au niveau module : x = '{x}'")  # "global"


# =============================================================================
# 2. Accès aux variables englobantes (lecture seule)
# =============================================================================

print("\n" + "=" * 60)
print("2. ACCÈS EN LECTURE AUX VARIABLES ENGLOBANTES")
print("=" * 60)


def externe2():
    message = "Je suis dans externe"

    def interne2():
        # On peut LIRE la variable englobante sans problème
        print(f"  interne2 lit : '{message}'")

    interne2()


externe2()


# =============================================================================
# 3. Mot-clé `global`
# =============================================================================

print("\n" + "=" * 60)
print("3. MOT-CLÉ `global`")
print("=" * 60)

compteur = 0


def incrementer():
    global compteur  # Déclare qu'on utilise la variable globale
    compteur += 1


print(f"Compteur initial : {compteur}")
incrementer()
print(f"Après incrementer() : {compteur}")
incrementer()
print(f"Après 2ème incrementer() : {compteur}")

# Attention : global est généralement à éviter !
# Préférez les retours de fonction ou les classes


# =============================================================================
# 4. Mot-clé `nonlocal`
# =============================================================================

print("\n" + "=" * 60)
print("4. MOT-CLÉ `nonlocal`")
print("=" * 60)


def externe3():
    x = 10

    def interne3():
        nonlocal x  # Déclare qu'on modifie la variable englobante
        x += 5
        print(f"  Dans interne3() : x = {x}")

    print(f"Avant interne3() : x = {x}")
    interne3()
    print(f"Après interne3() : x = {x}")


externe3()


# =============================================================================
# 5. Exemple pratique : compteur avec closure
# =============================================================================

print("\n" + "=" * 60)
print("5. EXEMPLE PRATIQUE : COMPTEUR AVEC CLOSURE")
print("=" * 60)


def creer_compteur(initial=0):
    """Crée un compteur encapsulé."""
    compte = initial

    def incrementer():
        nonlocal compte
        compte += 1
        return compte

    def decrementer():
        nonlocal compte
        compte -= 1
        return compte

    def valeur():
        return compte

    return incrementer, decrementer, valeur


inc, dec, val = creer_compteur(10)

print(f"Valeur initiale : {val()}")
print(f"Après inc() : {inc()}")
print(f"Après inc() : {inc()}")
print(f"Après dec() : {dec()}")
print(f"Valeur finale : {val()}")


# =============================================================================
# 6. Erreur courante : UnboundLocalError
# =============================================================================

print("\n" + "=" * 60)
print("6. ERREUR COURANTE : UnboundLocalError")
print("=" * 60)

valeur_globale = 100


def fonction_erreur():
    # Cette fonction va échouer !
    # Python voit que `valeur_globale` est assignée plus bas,
    # donc il la considère comme locale dès le début
    try:
        print(valeur_globale)  # UnboundLocalError !
        valeur_globale = 200   # Cette ligne cause le problème
    except UnboundLocalError as e:
        print(f"  Erreur : {e}")


def fonction_correcte():
    global valeur_globale
    print(f"  Valeur : {valeur_globale}")
    valeur_globale = 200


print("Tentative avec fonction_erreur() :")
fonction_erreur()

print("\nAvec fonction_correcte() :")
fonction_correcte()
print(f"Valeur après modification : {valeur_globale}")
