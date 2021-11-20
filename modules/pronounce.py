#!/usr/bin/python3
"""
Module containing ways of pronouncing a word,
using howjsay website (online) and pyttsx3 (local)
"""
from playsound import playsound
import pyttsx3

engine = pyttsx3.init()
engine.setProperty("rate", 125)

try:
    with open("blacklist", "r") as f:
        blacklist = f.read().split("\n")
    if blacklist[-1] == "":
        blacklist = blacklist[:-1]
except FileNotFoundError:
    print("Can't find 'blacklist' file")
    blacklist = []


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


def tts(word):
    """says the selected word using pyttsx3 module"""
    engine.say(word)
    engine.runAndWait()
