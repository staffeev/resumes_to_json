from geotext import GeoText
import pandas as pd


def anal_geo(text):
    places = GeoText(text=text)
    cities = places.cities + [None]
    countries = places.countries
    if not countries:
        code = places.country_mentions[1]
    return cities[0], countries[0]


def extract_geo(df):
    df["City"], df["Country"] = zip(*df["Text"].apply(anal_geo))
    return df

# f = open("/home/dima/Downloads/Albina Batmanova.txt")
# f = f.read()
# g = {"Text": [f, ""]}
# df = pd.DataFrame.from_dict(g)
# df = extract_geo(df)

# # print(anal_geo(f))
# print(df) 