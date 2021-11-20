#!/usr/bin/python3
"""
Définit les bases permettant de fire un quiz
"""
import platform
import random
import time

from modules import colors, timed

if platform.system() == "Windows":
    timed_input = timed.windows
else:
    timed_input = timed.unix_like


def question(word, solution, sleep_time=10, prompts=("\n", "➜ "), ends=(" ?", "")):
    """Affiche une question à l'utilisateur et renvoie son score"""
    prompt1, prompt2 = prompts
    end1, end2 = ends
    print(f"{prompt1}{word}{end1}")
    perf = round(timed_input(timeout=sleep_time), 5)
    if sleep_time - perf < 0.05:
        time.sleep(sleep_time)
        perf = 0.0
    print(f"{prompt2}{solution}{end2}")

    if perf != 0.0:
        print(f"{colors.GREEN}+ {perf}{colors.NULL}")
        return perf
    return 0.0


def quiz(dictionnary, sleep_time=7):
    """
    Interroge l'utilisateur sur une liste choisie et détermine un score
    en utilisant les fonctions définies auparavant
    """
    score = 0
    dic_list = list(dictionnary.keys())
    dic_len = len(dic_list)
    score_min = dic_len * sleep_time / 4
    while len(dic_list) > 0:
        key = dic_list.pop(random.randint(0, len(dic_list) - 1))
        if random.randint(0, 1) == 1:
            score += question(
                key,
                dictionnary[key],
                sleep_time=sleep_time,
                prompts=(f"\n({dic_len-len(dic_list)}/{dic_len}) ", "➜ "),
            )
        else:
            score += question(
                dictionnary[key],
                key,
                sleep_time=sleep_time,
                prompts=(f"\n({dic_len-len(dic_list)}/{dic_len}) ", "➜ "),
            )
        time.sleep(3)
    score = round(score, 5)
    if score < score_min:
        color = colors.RED
    else:
        color = colors.GREEN
    print(f"score: {color}{score}{colors.NULL} (min {score_min})")
