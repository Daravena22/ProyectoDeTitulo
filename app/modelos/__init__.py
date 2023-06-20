import logging, os
from importlib import import_module

MODELOS_PATH = "app/modelos"

def importar_modelos():
    
    for modelos in os.listdir(MODELOS_PATH):
        if modelos.startswith("__"): continue
        import_module(
            f"{MODELOS_PATH.replace('/', '.')}.{modelos.split('.')[0]}",
            "*"
        )