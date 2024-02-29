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




if __name__ == "__main__":
    df = pd.read_csv("../csv/text.csv").drop(columns=["Unnamed: 0"])
    # df = df[~df.isna().any(axis=1)]
    df["Email"] = df["Text"].apply(find_email)
    df["Phone"] = df["Text"].apply(find_phone)