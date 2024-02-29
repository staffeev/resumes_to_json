from nltk import ne_chunk, pos_tag, word_tokenize, download 
from nltk.tree import Tree
import nltk
import pandas as pd


def extract(text):
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


if __name__ == "__main__":
    df = pd.read_csv("csv/text.csv").drop(columns=["Unnamed: 0"])
    df["Name"] = df["Text"].apply(extract)
    print(df)

