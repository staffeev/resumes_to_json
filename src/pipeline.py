from read import read
from preprocess import preprocess
from extract_features import extract_features
from export import export

class Pipeline():
    def run_all(self):
        df = read()
        df = preprocess(df)
        df = extract_features(df)
        export(df)
