#!/usr/bin/python3
"""
Définit des fonctions permettant une entrée avec timout de l'utilisateur
"""
import sys
import time
import platform

if platform.system() == "Windows":
    import msvcrt
else:
    from select import select


def windows(timeout=10):
    """Définit un input avec timeout pour les systèmes Windows (non testé)"""
    start_time = time.time()
    endtime = time.monotonic() + timeout
    result = []
    while time.monotonic() < endtime:
        if msvcrt.kbhit():
            result.append(msvcrt.getwche())
            if result[-1] == "\r":
                return timeout - (time.time() - start_time)
        time.sleep(0.04)
    return 0


def unix_like(timeout=10):
    """Définit un input avec timeout pour les systèmes de type Linux/macOS/BSD"""
    start_time = time.time()
    sys.stdin.flush()
    sys.stdout.flush()
    rlist, _, _ = select([sys.stdin], [], [], timeout)
    if rlist:
        _ = sys.stdin.readline()
        return timeout - (time.time() - start_time)
    return 0
