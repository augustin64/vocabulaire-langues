#!/usr/bin/python3
"""
Script Python pour s'entraîner sur des listes de mots,
de vocabulaire par exemple
"""
import json
import os
from modules import quiz
# from modules import pronounce
# import time

try:
    import enquiries

    choose = enquiries.choose
except ModuleNotFoundError:

    def choose(query, options):
        """Prompt alternatif si le module enquiries n'est pas installé"""
        print(query)
        print(
            "\n".join(["{}. {}".format(i + 1, options[i]) for i in range(len(options))])
        )
        response = int(input("> "))
        return options[response - 1]

def choose_list(json_files):
    """Fonction d'initialisation du programme,
    durant laquelle l'utilisateur choisit la liste qu'il souhaite"""
    chosen_file = choose("Which word list do you want to work ?", json_files)
    with open("listes/" + chosen_file) as file:
        json_data = json.load(file)

        chosen_theme = choose("Which part do you want to work ?", json_data.keys())

        words_list = json_data[chosen_theme]
        file.close()
        return (chosen_theme, words_list)


lists = [i for i in os.listdir("listes") if ".json" in i]

theme, wordlist = choose_list(lists)
print(f"\t{'='*5}\t{theme}\t{'='*5}")

quiz.quiz(wordlist)

"""
for k in wordlist.keys():
    print(k, "\n➜", wordlist[k])
    pronounce.tts(wordlist[k])
    pronounce.tts(k)
    time.sleep(3)
"""
