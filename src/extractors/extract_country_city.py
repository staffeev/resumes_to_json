import locationtagger


def extract_geo(df):
    df["Location"] = df["Stemmed"].apply(lambda x: locationtagger.find_locations(text=" ".join(x) if x else "a"))
    df["Country"] = df["Location"].apply(lambda x: x.countries[0] if x.countries else "")
    df["City"] = df["Location"].apply(lambda x: x.cities[0] if x.cities else "")
    df = df.drop(columns=["Location"])
    return df

# text = "Pushkin Pavlovsk aaaaaaaaaaaaapoiaefpishfpihsri gggg "

# entities = locationtagger.find_locations(text = text)
# print(entities.cities)