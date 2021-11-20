#!/usr/bin/python3
"""
Définit des couleurs basiques à utiliser lors de l'affichage dans le terminal
"""
import platform

if platform.system() == "Windows":
    RED = ""
    GREEN = ""
    BLUE = ""
    NULL = ""
else:
    RED = "\x1b[0;31;40m"
    GREEN = "\x1b[0;32;40m"
    BLUE = ""
    NULL = "\x1b[0m"
