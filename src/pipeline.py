from read import read, remove_tmp_files
from preprocess import preprocess
from extract_features import extract_features
from export import export
# from extractors.extract_country_city import extract_geo

class Pipeline():
    def run_all(self):
        tmp_files, df = read()
        df = preprocess(df)
        df = extract_features(df)
        # df = extract_geo(df)
        export(df)
        remove_tmp_files(tmp_files)


if __name__ == "__main__":
    pipeline = Pipeline()
    pipeline.run_all()
