import pandas as pd
from nltk.stem import PorterStemmer

ps = PorterStemmer()

def stem(text):
    return [ps.stem(word) for word in text.split()]

def preprocess(df):
    df["Stemmed"] = df["Text"].apply(stem)
    return df
