"""
Fermetures (Closures)
=====================

Démonstration des closures : fonctions qui capturent et mémorisent
les variables de leur portée englobante.
"""

# =============================================================================
# 1. Qu'est-ce qu'une fermeture ?
# =============================================================================

print("=" * 60)
print("1. QU'EST-CE QU'UNE FERMETURE ?")
print("=" * 60)


def creer_compteur(initial=0):
    """Crée un compteur encapsulé."""
    compte = initial  # Variable capturée par la fermeture

    def incrementer():
        nonlocal compte
        compte += 1
        return compte

    return incrementer


compteur = creer_compteur(10)
print(f"compteur() = {compteur()}")  # 11
print(f"compteur() = {compteur()}")  # 12
print(f"compteur() = {compteur()}")  # 13

# Chaque appel à creer_compteur crée une nouvelle fermeture indépendante
compteur2 = creer_compteur(100)
print(f"\ncompteur2() = {compteur2()}")  # 101
print(f"compteur() = {compteur()}")      # 14 (indépendant)


# =============================================================================
# 2. Anatomie d'une fermeture
# =============================================================================

print("\n" + "=" * 60)
print("2. ANATOMIE D'UNE FERMETURE")
print("=" * 60)


def externe(x):
    def interne(y):
        return x + y  # x est "capturé" depuis la portée externe
    return interne


addition_5 = externe(5)

# Inspection de la fermeture
print(f"addition_5.__closure__ : {addition_5.__closure__}")
print(f"Nombre de cellules : {len(addition_5.__closure__)}")
print(f"Valeur capturée : {addition_5.__closure__[0].cell_contents}")

print(f"\naddition_5(10) = {addition_5(10)}")  # 15
print(f"addition_5(20) = {addition_5(20)}")  # 25


# =============================================================================
# 3. Encapsulation de données (style privé)
# =============================================================================

print("\n" + "=" * 60)
print("3. ENCAPSULATION : COMPTE BANCAIRE")
print("=" * 60)


def creer_compte_bancaire(solde_initial):
    """Simule un compte bancaire avec solde privé."""
    solde = solde_initial

    def deposer(montant):
        nonlocal solde
        if montant > 0:
            solde += montant
            print(f"  Dépôt de {montant}€ effectué")
        return solde

    def retirer(montant):
        nonlocal solde
        if montant <= solde:
            solde -= montant
            print(f"  Retrait de {montant}€ effectué")
        else:
            print(f"  Retrait refusé : solde insuffisant")
        return solde

    def consulter():
        return solde

    return deposer, retirer, consulter


deposer, retirer, consulter = creer_compte_bancaire(100)

print(f"Solde initial : {consulter()}€")
deposer(50)
print(f"Solde : {consulter()}€")
retirer(30)
print(f"Solde : {consulter()}€")
retirer(200)  # Refusé
print(f"Solde final : {consulter()}€")

# Le solde n'est pas accessible directement !
# Il n'y a pas de variable 'solde' dans la portée globale


# =============================================================================
# 4. Configuration et paramétrisation
# =============================================================================

print("\n" + "=" * 60)
print("4. CONFIGURATION : LOGGER PARAMÉTRABLE")
print("=" * 60)


def creer_logger(niveau, prefixe=""):
    """Factory de fonctions de log configurées."""
    niveaux = {"DEBUG": 0, "INFO": 1, "WARNING": 2, "ERROR": 3}
    seuil = niveaux.get(niveau, 0)

    def log(message, niveau_msg="INFO"):
        if niveaux.get(niveau_msg, 0) >= seuil:
            print(f"{prefixe}[{niveau_msg}] {message}")

    return log


# Créer des loggers spécialisés
debug_logger = creer_logger("DEBUG", prefixe="[DEV] ")
prod_logger = creer_logger("WARNING", prefixe="[PROD] ")

print("--- Debug logger (seuil: DEBUG) ---")
debug_logger("Détail de débogage", "DEBUG")   # Affiché
debug_logger("Information", "INFO")            # Affiché
debug_logger("Attention !", "WARNING")         # Affiché

print("\n--- Prod logger (seuil: WARNING) ---")
prod_logger("Détail de débogage", "DEBUG")    # Non affiché
prod_logger("Information", "INFO")             # Non affiché
prod_logger("Attention !", "WARNING")          # Affiché
prod_logger("Erreur critique !", "ERROR")      # Affiché


# =============================================================================
# 5. Piège classique : closure dans une boucle
# =============================================================================

print("\n" + "=" * 60)
print("5. PIÈGE : CLOSURE DANS UNE BOUCLE")
print("=" * 60)

# PROBLÈME : toutes les fonctions capturent la MÊME variable i
print("--- Problème ---")
fonctions_bug = []
for i in range(3):
    fonctions_bug.append(lambda: i)

print(f"Résultats attendus : [0, 1, 2]")
print(f"Résultats obtenus : {[f() for f in fonctions_bug]}")  # [2, 2, 2] !

# SOLUTION 1 : argument par défaut (capture la valeur)
print("\n--- Solution 1 : argument par défaut ---")
fonctions_v1 = []
for i in range(3):
    fonctions_v1.append(lambda x=i: x)

print(f"Résultats : {[f() for f in fonctions_v1]}")  # [0, 1, 2]

# SOLUTION 2 : utiliser une factory
print("\n--- Solution 2 : factory ---")


def creer_func(val):
    return lambda: val


fonctions_v2 = [creer_func(i) for i in range(3)]
print(f"Résultats : {[f() for f in fonctions_v2]}")  # [0, 1, 2]


# =============================================================================
# 6. Cas d'usage : multiplicateur configurable
# =============================================================================

print("\n" + "=" * 60)
print("6. CAS D'USAGE : MULTIPLICATEUR CONFIGURABLE")
print("=" * 60)


def creer_multiplicateur(facteur):
    """Retourne une fonction qui multiplie par le facteur donné."""
    def multiplier(nombre):
        return nombre * facteur
    return multiplier


# Création de fonctions spécialisées
doubler = creer_multiplicateur(2)
tripler = creer_multiplicateur(3)
fois_dix = creer_multiplicateur(10)

nombres = [1, 2, 3, 4, 5]

print(f"Nombres originaux : {nombres}")
print(f"Doublés : {[doubler(n) for n in nombres]}")
print(f"Triplés : {[tripler(n) for n in nombres]}")
print(f"x10 : {[fois_dix(n) for n in nombres]}")

# Inspection des closures
print(f"\ndoubler.__closure__[0].cell_contents = {doubler.__closure__[0].cell_contents}")
print(f"tripler.__closure__[0].cell_contents = {tripler.__closure__[0].cell_contents}")
