import nltk
import spacy
import os

nltk.downloader.download('maxent_ne_chunker')
nltk.downloader.download('words')
nltk.downloader.download('treebank')
nltk.downloader.download('stopwords')
nltk.downloader.download('maxent_treebank_pos_tagger')
nltk.downloader.download('punkt')
os.system("python -m spacy download en_core_web_sm")