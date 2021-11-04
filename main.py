#!/usr/bin/python3

import os
import time
import json
import random
import pyttsx3
import platform
import subprocess
from playsound import playsound

engine = pyttsx3.init()
engine.setProperty("rate", 125)

if platform.system() == "Windows":
    import msvcrt

try:
    import enquiries

    choose = enquiries.choose
except:  # On offre une autre option si le module enquiries n'est pas installé
    # ce module n'étant pas compatible égaleent sur toutes les plateformes
    def choose(query, options):
        print(query)
        print(
            "\n".join(["{}. {}".format(i + 1, options[i]) for i in range(len(options))])
        )
        response = int(input("> "))
        return options[response - 1]


def timed(timeout=10):
    start_time = time.time()
    if platform.system() != "Windows":
        if subprocess.call(f"read -t {timeout}", shell=True) == 0:
            return start_time - time.time() + timeout
    else:
        endtime = time.monotonic() + timeout
        while time.monotonic() < endtime:
            if msvcrt.kbhit():
                if result[-1] == "\r":
                    return timeout - (time.time() - start_time)
            time.sleep(0.04)
    return 0


def pronounce(raw_word):
    """pronounces the given word"""
    word = ""
    for i in raw_word:
        if i in "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz":
            word += i.lower()
        else:
            word += " "

    if " " in word:
        split_word = word.split(" ")
        for i in split_word:
            pronounce(i)
    else:
        if word != "" and word not in blacklist:
            url = "https://howjsay.com/mp3/" + word + ".mp3"
            playsound(url)


def speak(word):
    """says the selected word using pyttsx3 module"""
    engine.say(word)
    engine.runAndWait()


def question(
    word, solution, sleep_time=10, prompt1="\n", prompt2="➜ ", end1=" ?", end2=""
):
    print(f"{prompt1}{word}{end1}")
    perf = round(timed(timeout=sleep_time), 5)
    if sleep_time - perf < 0.05:
        time.sleep(sleep_time)
        perf = 0.0
    print(f"{prompt2}{solution}{end2}")

    if perf != 0.0:
        print(f"\x1b[0;32;40m+ {perf}\x1b[0m")
        return perf
    return 0.0


def quiz(dictionnary, sleep_time=7):
    score = 0
    dic_list = list(dictionnary.keys())
    l = len(dic_list)
    while len(dic_list) > 0:
        key = dic_list.pop(random.randint(0, len(dic_list) - 1))
        if random.randint(0, 1) == 1:
            score += question(
                key,
                dictionnary[key],
                sleep_time=sleep_time,
                prompt1=f"\n({l-len(dic_list)}/{l}) ",
            )
        else:
            score += question(
                dictionnary[key],
                key,
                sleep_time=sleep_time,
                prompt1=f"\n({l-len(dic_list)}/{l}) ",
            )
        time.sleep(4)
    if score < l * sleep_time / 5:
        color = "\x1b[0;31;40m"
    else:
        color = "\x1b[0;32;40m"
    print(f"score: {color}{score}\x1b[0m")


def linea_quiz(dictionnary):
    score = 0
    for key in dictionnary.keys():
        score += question(dictionnary[key], key, sleep_time=6)
        time.sleep(4)
    print(f"score: {score}")


try:
    with open("blacklist", "r") as f:
        blacklist = f.read().split("\n")
    if blacklist[-1] == "":
        blacklist = blacklist[:-1]
except:
    print("Can't find 'blacklist' file")
    blacklist = []

json_files = [i for i in os.listdir("listes") if ".json" in i]

chosen_file = choose("Which word list do you want to work ?", json_files)

with open("listes/" + chosen_file) as f:
    json_data = json.load(f)

    theme = choose("Which part do you want to work ?", json_data.keys())
    print("\t===\t", theme, "\t===")
    # speak(theme)
    words_list = json_data[theme]
    f.close()

quiz(words_list)
# linea_quiz(words_list)
"""
for k in words_list.keys() :
    print(k, '\n➜', words_list[k])
    speak(words_list[k])
    speak(k)
    time.sleep(3)
"""
