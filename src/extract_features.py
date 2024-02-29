from nltk import ne_chunk, pos_tag, word_tokenize, download 
from nltk.tree import Tree
import pandas as pd
import locationtagger
import fitz
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


def reg_find_url(string):
    regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
    url = re.findall(regex, string)
    return [x[0] for x in url]


def find_substring_in_string(sub, text, save="postf"):
    ix_pref = text.find(sub)
    if ix_pref == -1:
        return None
    if save == "postf":
        return text[ix_pref + len(sub):]
    elif save == "pref":
        return text[:ix_pref]


def process_url(link_pref, text, keywords):
    f = find_substring_in_string
    keyword, mode = keywords[0]
    res = f(keyword, text, mode)
    if res is None:
        return None
    for keyword, mode in keywords[1:]:
        value = f(keyword, res, mode)
        if value is None:
            break
        res = value
    return link_pref + res


def filter_nans_in_urls(df):
    return df.apply(lambda row: ([x for x in row if x is not None] + [None])[0])


def get_links_from_pdf(filename):
    links = []
    for page in fitz.open(filename):
        links.extend([obj["uri"] for obj in page.get_links()])
    return links


def find_links_for_resume(df):
    urls = df.apply(lambda x: reg_find_url(x["Text"]) + get_links_from_pdf("../" + x["UsedFilename"]), axis=1)
    github_urls = urls.apply(
        lambda row: [process_url("https://github.com/", x, \
        [("github", "postf"), ("/", "postf"), ("/", "pref")]) for x in row])\
        .apply(lambda row: ([x for x in row if x is not None] + [None])[0])
    linkedin_urls = urls.apply(
        lambda row: [process_url("https://www.linkedin.com/", x, \
        [("linkedin", "postf"), ("/", "postf"), ("/", "postf")]) for x in row])\
        .apply(lambda row: ([x for x in row if x is not None] + [None])[0])
    # linkedin.com/in/renat
    return urls, github_urls, linkedin_urls


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
    return name_surname if name_surname else None


def extract_location(x):
    return locationtagger.find_locations(text=" ".join(x) if x else " ")


def extract_country(location_obj):
    return location_obj.countries[0] if location_obj.countries else None


def extract_city(location_obj):
    return location_obj.cities[0] if location_obj.cities else ""


def extract_geo_information(df):
    loc = df["Stemmed"].apply(extract_location)
    countries = loc.apply(extract_country)
    print("Field `Country` extracted")
    cities = loc.apply(extract_city)
    print("Field `City` extracted")
    return countries, cities


def extract_features(df):
    df["Email"] = df["Text"].apply(find_email)
    print("Field `Email` extracted")
    df["Phone"] = df["Text"].apply(find_phone)
    print("Field `Phone` extracted")
    df["NameSurname"] = df["Text"].apply(extract_name_an_surname)
    print("Field `NameSurname` extracted")
    df["Country"], df["City"] = extract_geo_information(df)
    return df
