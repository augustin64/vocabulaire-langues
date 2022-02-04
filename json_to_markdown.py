#!/usr/bin/python3
"""Converts a bunch of json files to markdown"""
import os
import sys
import json
import requests
from bs4 import BeautifulSoup

OUT = "md"

def get_phonetic(word, language, variant="UK") :
    """
    Search a word's phonetic in 'WordReference'.
    You can use 'English' language and two variants are available : 'US' and 'UK'
    It will return you a string containing the phonetic transcription of the word pronunciation
    """

    lang_from = ""
    lang_to = ""

    if language == "English":
        lang_from = "en"
        lang_to = "fr"

    page = requests.get(f"https://www.wordreference.com/{lang_from}{lang_to}/{word}")
    soup = BeautifulSoup(page.content, 'html.parser')

    pronuncation = soup.find("div", {"id":"pronunciation_widget"}).text

    if variant == "US" and "US" in pronuncation.split('/')[2]:
        return pronuncation.split('/')[3]
    return pronuncation.split('/')[1]

def phonetic(word):
    """Récupère la phonétique dans le cache ou depuis l'API"""
    if " " in word:
        return " ".join([ phonetic(i) for i in word.split(" ") ])
    if "/" in word:
        return "/".join([ phonetic(i) for i in word.split("/")])

    if word in phonetic_data :
        return phonetic_data[word]
    try :
        phonetic_data[word] = get_phonetic(word, "English")
        return phonetic_data[word]
    except :
        return ""

def json_to_md(file_path):
    """Converts a json file to markdown"""
    filename = file_path.split("/")[-1]
    outfile = os.path.join(OUT, ".".join(filename.split(".")[:-1])+".md")
    lang = filename.split("_")[1]
    with open(file_path, "r", encoding="utf8") as file:
        in_content = json.load(file)

    out_content = ""
    out_content += "# "+(".".join(filename.split(".")[:-1])).replace("_", " ") + "\n"
    print(f"Converting {filename}")
    length = sum([ len(in_content[i].keys()) for i in in_content.keys()])
    current = 0
    for title in in_content.keys():
        if lang == "anglais":
            out_content += f"## {title}\n||||\n|:---|:---|:---|\n"
        else:
            out_content += f"## {title}\n|||\n|:---|:---|\n"
        for line in in_content[title]:
            current += 1
            if lang == "anglais":
                out_content += f"| {line} | {in_content[title][line]} | {phonetic(line)} |\n"
                print(f"{filename}: ({current}/{length})")
            else:
                out_content += f"| {line} | {in_content[title][line]} |\n"
    with open(outfile, "w", encoding="utf8") as file:
        file.write(out_content)

if len(sys.argv) == 1 :
    files = [ "listes/" + i for i in os.listdir("listes")]
else :
    files = sys.argv[1:]

with open(".phonetic_cache.json", "r") as f:
    phonetic_data = json.load(f)

for file in files :
    json_to_md(file)

with open(".phonetic_cache.json", "w") as f:
    json.dump(phonetic_data, f)
