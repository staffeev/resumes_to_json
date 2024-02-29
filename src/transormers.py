from sentence_transformers import SentenceTransformer
from sentence_transformers.util import cos_sim
import pandas as pd
from time import time


LABELS_FOR_BLOCKS = ["Education", "Skills", "Experience", "Languages", "Personal", "Good day"]





def find_most_similar_labels(blocks):


sentences = ["This is an example sentence", "Each sentence is converted"]

model = SentenceTransformer('sentence-transformers/average_word_embeddings_glove.6B.300d')
embeddings = model.encode(sentences)


start = time()
for i in range(1000):
    embeddings = model.encode(sentences)
print(time() - start)