from nltk import ne_chunk, pos_tag, word_tokenize, download 
from nltk.tree import Tree
import pandas as pd
import re


def find_email(text):
    als = "[a-zA-Z0-9.-_]"
    found = re.findall(rf"{als}+@{als}+\.{als}+", text)
    if not found:
        return None
    return found[0]


def check_if_duration(text):
    return re.fullmatch(r"\s*\d{4}\s*-\s*\d{4}\s*", text) is not None


def find_phone(text, lb=11):
    found = re.findall(r"[ 0-9-_\+\(\)]+", text)
    rb = 15
    for i in sorted(found, key=len, reverse=True):
        if lb <= len(re.findall(r"\d", i)) <= rb and not check_if_duration(i):
            return i
    return None


# text - all text from a block of resume
# name_surname - list [name, surname] (most of the times :) )
def extract_name_an_surname(text):
    nltk_results = ne_chunk(pos_tag(word_tokenize(text)))
    name_surname = []
    for nltk_result in nltk_results:
        if len(name_surname) < 2:
            if type(nltk_result) == Tree:
                name = ''
                for nltk_result_leaf in nltk_result.leaves():
                    name += nltk_result_leaf[0] + ' '
                if nltk_result.label()=="PERSON":
                    for word in name.split():
                        # print(word)
                        name_surname.append(word)
        else:
            break
    return name_surname


def extract_features(df):
    df["Email"] = df["Text"].apply(find_email)
    df["Phone"] = df["Text"].apply(find_phone)
    df["NameSurname"] = df["Text"].apply(extract_name_an_surname)
    return df
