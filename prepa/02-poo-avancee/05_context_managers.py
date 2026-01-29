"""
Context Managers
================

Création et utilisation de context managers avec __enter__/__exit__
et le décorateur @contextmanager.
"""

from contextlib import contextmanager, ExitStack
import time
import os
import sys

# =============================================================================
# 1. Le protocole context manager
# =============================================================================

print("=" * 60)
print("1. LE PROTOCOLE CONTEXT MANAGER")
print("=" * 60)


class GestionFichier:
    """Context manager basique pour fichiers."""

    def __init__(self, chemin, mode):
        self.chemin = chemin
        self.mode = mode
        self.fichier = None

    def __enter__(self):
        """Appelé à l'entrée du bloc with."""
        print(f"  Ouverture de {self.chemin}")
        self.fichier = open(self.chemin, self.mode)
        return self.fichier  # Valeur assignée à 'as'

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Appelé à la sortie du bloc with."""
        print(f"  Fermeture de {self.chemin}")
        self.fichier.close()
        return False  # Ne pas supprimer les exceptions


# Création d'un fichier temporaire pour le test
print("Test du context manager GestionFichier :")
with GestionFichier("/tmp/test_cm.txt", "w") as f:
    f.write("Hello World\n")
    print("  Écriture effectuée")

print("  Fin du bloc with")


# =============================================================================
# 2. Gestion des exceptions dans __exit__
# =============================================================================

print("\n" + "=" * 60)
print("2. GESTION DES EXCEPTIONS")
print("=" * 60)


class SuppresseurErreur:
    """Context manager qui supprime certaines exceptions."""

    def __init__(self, *exceptions):
        self.exceptions = exceptions

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            print(f"  Exception capturée : {exc_type.__name__}: {exc_val}")

        # Retourner True supprime l'exception
        return exc_type in self.exceptions


print("Test avec ValueError (supprimée) :")
with SuppresseurErreur(ValueError, TypeError):
    print("  Avant l'erreur")
    int("pas un nombre")  # ValueError
    print("  Après l'erreur (non atteint)")

print("  Continue après le with")

print("\nTest avec KeyError (non supprimée) :")
try:
    with SuppresseurErreur(ValueError):
        d = {}
        d["inexistant"]  # KeyError
except KeyError:
    print("  KeyError propagée et capturée à l'extérieur")


# =============================================================================
# 3. @contextmanager : syntaxe simplifiée
# =============================================================================

print("\n" + "=" * 60)
print("3. @contextmanager : SYNTAXE SIMPLIFIÉE")
print("=" * 60)


@contextmanager
def gestion_fichier_simple(chemin, mode):
    """Context manager simplifié avec décorateur."""
    print(f"  Ouverture de {chemin}")
    f = open(chemin, mode)
    try:
        yield f  # Point de suspension
    finally:
        print(f"  Fermeture de {chemin}")
        f.close()


print("Test avec @contextmanager :")
with gestion_fichier_simple("/tmp/test_cm2.txt", "w") as f:
    f.write("Test avec contextmanager\n")
    print("  Écriture effectuée")


# =============================================================================
# 4. Context manager : mesure de temps
# =============================================================================

print("\n" + "=" * 60)
print("4. MESURE DE TEMPS")
print("=" * 60)


@contextmanager
def chronometre(description="Opération"):
    """Mesure le temps d'exécution d'un bloc."""
    debut = time.perf_counter()
    try:
        yield
    finally:
        duree = time.perf_counter() - debut
        print(f"  {description}: {duree:.4f} secondes")


print("Mesure de temps :")
with chronometre("Calcul de somme"):
    resultat = sum(i ** 2 for i in range(100_000))
    print(f"  Résultat : {resultat}")

with chronometre("Sleep de 0.2s"):
    time.sleep(0.2)


# =============================================================================
# 5. Context manager : changement temporaire de contexte
# =============================================================================

print("\n" + "=" * 60)
print("5. CHANGEMENT TEMPORAIRE DE CONTEXTE")
print("=" * 60)


@contextmanager
def working_directory(chemin):
    """Change temporairement le répertoire de travail."""
    ancien = os.getcwd()
    try:
        os.chdir(chemin)
        yield
    finally:
        os.chdir(ancien)


print(f"Répertoire actuel : {os.getcwd()}")
with working_directory("/tmp"):
    print(f"Dans le with : {os.getcwd()}")
print(f"Après le with : {os.getcwd()}")


@contextmanager
def environnement_temporaire(**variables):
    """Définit des variables d'environnement temporaires."""
    anciennes = {}
    for nom, valeur in variables.items():
        anciennes[nom] = os.environ.get(nom)
        os.environ[nom] = valeur
    try:
        yield
    finally:
        for nom, ancienne_valeur in anciennes.items():
            if ancienne_valeur is None:
                del os.environ[nom]
            else:
                os.environ[nom] = ancienne_valeur


print("\nVariables d'environnement temporaires :")
print(f"  Avant : DEBUG = {os.environ.get('DEBUG', 'non défini')}")
with environnement_temporaire(DEBUG="true", APP_ENV="test"):
    print(f"  Dans with : DEBUG = {os.environ.get('DEBUG')}")
    print(f"  Dans with : APP_ENV = {os.environ.get('APP_ENV')}")
print(f"  Après : DEBUG = {os.environ.get('DEBUG', 'non défini')}")


# =============================================================================
# 6. Context manager : redirection de sortie
# =============================================================================

print("\n" + "=" * 60)
print("6. REDIRECTION DE SORTIE")
print("=" * 60)


@contextmanager
def capture_stdout():
    """Capture la sortie standard."""
    from io import StringIO

    ancien_stdout = sys.stdout
    sys.stdout = StringIO()
    try:
        yield sys.stdout
    finally:
        sys.stdout = ancien_stdout


print("Capture de stdout :")
with capture_stdout() as output:
    print("Ce texte est capturé")
    print("Et celui-ci aussi")

captured = output.getvalue()
print(f"  Texte capturé :\n{captured}")


# =============================================================================
# 7. Context manager : verrouillage (lock)
# =============================================================================

print("=" * 60)
print("7. VERROUILLAGE (SIMULATION)")
print("=" * 60)


class SimpleLock:
    """Simulation d'un verrou (lock)."""

    def __init__(self, nom="lock"):
        self.nom = nom
        self.locked = False

    def __enter__(self):
        print(f"  Acquisition du verrou '{self.nom}'")
        self.locked = True
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        print(f"  Libération du verrou '{self.nom}'")
        self.locked = False
        return False


lock = SimpleLock("resource")
print(f"Avant with : locked = {lock.locked}")
with lock:
    print(f"  Dans with : locked = {lock.locked}")
print(f"Après with : locked = {lock.locked}")


# =============================================================================
# 8. Context managers multiples
# =============================================================================

print("\n" + "=" * 60)
print("8. CONTEXT MANAGERS MULTIPLES")
print("=" * 60)


@contextmanager
def contexte_nomme(nom):
    """Context manager simple pour la démonstration."""
    print(f"  Entrée dans {nom}")
    try:
        yield nom
    finally:
        print(f"  Sortie de {nom}")


# Plusieurs context managers
print("Plusieurs context managers :")
with contexte_nomme("A") as a, contexte_nomme("B") as b:
    print(f"    Dans le bloc : a={a}, b={b}")

# Avec ExitStack pour un nombre variable
print("\nAvec ExitStack :")
noms = ["X", "Y", "Z"]
with ExitStack() as stack:
    contextes = [stack.enter_context(contexte_nomme(nom)) for nom in noms]
    print(f"    Contextes actifs : {contextes}")


# =============================================================================
# 9. Context manager réutilisable
# =============================================================================

print("\n" + "=" * 60)
print("9. CONTEXT MANAGER RÉUTILISABLE")
print("=" * 60)


class Connexion:
    """Simule une connexion réutilisable."""

    def __init__(self, nom):
        self.nom = nom
        self.ouverte = False

    def __enter__(self):
        if self.ouverte:
            print(f"  {self.nom} déjà ouverte")
        else:
            print(f"  Ouverture de {self.nom}")
            self.ouverte = True
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        print(f"  Fermeture de {self.nom}")
        self.ouverte = False
        return False

    def execute(self, query):
        print(f"    Exécution : {query}")


conn = Connexion("DB")

print("Première utilisation :")
with conn:
    conn.execute("SELECT * FROM users")

print("\nDeuxième utilisation :")
with conn:
    conn.execute("INSERT INTO logs ...")


# =============================================================================
# 10. Exemple pratique : transaction simulée
# =============================================================================

print("\n" + "=" * 60)
print("10. EXEMPLE PRATIQUE : TRANSACTION")
print("=" * 60)


class Transaction:
    """Simule une transaction de base de données."""

    def __init__(self, nom="transaction"):
        self.nom = nom
        self.operations = []

    def __enter__(self):
        print(f"  BEGIN {self.nom}")
        self.operations = []
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            print(f"  COMMIT {self.nom} ({len(self.operations)} opérations)")
            return False
        else:
            print(f"  ROLLBACK {self.nom} (erreur: {exc_val})")
            self.operations = []
            return True  # Supprime l'exception

    def execute(self, sql):
        self.operations.append(sql)
        print(f"    → {sql}")


print("Transaction réussie :")
with Transaction("tx1") as tx:
    tx.execute("INSERT INTO users VALUES (1, 'Alice')")
    tx.execute("UPDATE accounts SET balance = 100")

print("\nTransaction échouée :")
with Transaction("tx2") as tx:
    tx.execute("INSERT INTO users VALUES (2, 'Bob')")
    raise ValueError("Erreur simulée")
    tx.execute("Cette ligne n'est pas atteinte")

print("  Le programme continue normalement")
