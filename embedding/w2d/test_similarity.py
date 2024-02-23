# test_similarity.py
from gensim.models import Word2Vec
import json
from nltk.tokenize import word_tokenize
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

# Function to generate a document embedding
def document_embedding(model, doc_tokens):
    embeddings = [model.wv[word] for word in doc_tokens if word in model.wv]
    if not embeddings:
        return np.zeros(model.vector_size)
    return np.mean(embeddings, axis=0)

# Load the trained Word2Vec model
model = Word2Vec.load("word2vec_model.model")

# Load the preprocessed Q&A data
with open('EE450_Piazza.json', 'r') as file:
    preprocessed_data = json.load(file)

# Generate embeddings for all documents
doc_embeddings = np.array([document_embedding(model, word_tokenize(doc.lower())) for doc in preprocessed_data.values()])

# Define a test sentence and generate its embedding
# test_sentence = "Where should I return Gateway?"
test_sentence = "What type of formula sheet can we use?"
test_embedding = document_embedding(model, word_tokenize(test_sentence.lower()))

# Find the 3 most similar Q&A pairs
similarity_scores = cosine_similarity([test_embedding], doc_embeddings)[0]
top_3_indices = similarity_scores.argsort()[-3:][::-1]  # Get indices of top 3 scores

# Print the 3 most similar Q&A pairs
for index in top_3_indices:
    key = list(preprocessed_data.keys())[index]
    similarity = similarity_scores[index]
    print(f"Key: {key}, Similarity: {similarity:.4f}, Q&A Pair: {preprocessed_data[key]}")
