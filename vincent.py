import inspect

def get_caller_name():
    return inspect.currentframe().f_back.f_back.f_code.co_name

def fonction_a():
    fonction_b()

def fonction_b():
    print(f"Appelée par : {get_caller_name()}")

fonction_a()  # Appelée par : fonction_a



import inspect

def log(message):
    caller = inspect.currentframe().f_back.f_code.co_name
    print(f"[{caller}] {message}")

def process_data():
    log("Début du traitement")
    log("Fin du traitement")

process_data()
