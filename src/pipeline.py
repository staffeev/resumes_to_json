from read import read
from preprocess import preprocess
from extract_features import extract_features
from export import export
from extractors.extract_country_city import extract_geo

class Pipeline():
    def run_all(self):
        df = read()
        df = preprocess(df)
        print(df)
        df = extract_features(df)
        # df = extract_geo(df)
        export(df)
