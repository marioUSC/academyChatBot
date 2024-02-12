# build_model.py
from gensim.models import Word2Vec
import json
from nltk.tokenize import word_tokenize
import nltk

# Load preprocessed data
with open('EE450_Piazza.json', 'r') as file:
    preprocessed_data = json.load(file)

# Prepare data for Word2Vec training
tokenized_docs = [word_tokenize(doc.lower()) for doc in preprocessed_data.values()]

# Train Word2Vec model
model = Word2Vec(sentences=tokenized_docs, vector_size=100, window=5, min_count=1, workers=4)

# Save the model
model.save("word2vec_model.model")
