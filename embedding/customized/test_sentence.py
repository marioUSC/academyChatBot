import numpy as np
from gensim.models import Word2Vec
from scipy.spatial.distance import cosine
from bs4 import BeautifulSoup
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import nltk

from sklearn.feature_extraction.text import TfidfVectorizer
import json


def test_average_word():
    def preprocess_text(text):
        text = BeautifulSoup(text, 'html.parser').get_text()
        
        text = text.lower()
        
        words = word_tokenize(text)
        
        stop_words = set(stopwords.words('english'))
        custom_stop_words = ['i', 'the']  
        all_stop_words = stop_words.union(custom_stop_words)
        
        words = [w for w in words if w.isalpha() and w not in all_stop_words]
        
        stemmer = PorterStemmer()
        stemmed = [stemmer.stem(w) for w in words]
        
        return ' '.join(stemmed)

    def document_vector(model, doc):
        doc = [word for word in doc if word in model.wv.index_to_key]
        if not doc:
            return np.zeros(model.vector_size)
        return np.mean(model.wv[doc], axis=0)

    model = Word2Vec.load("word2vec_model.model")
    doc_vectors = np.load('doc_vectors.npy')

    custom_sentence = "calculate csma/cd"
    preprocessed_sentence = preprocess_text(custom_sentence)

    custom_vector = document_vector(model, preprocessed_sentence)

    similarities = [1 - cosine(custom_vector, doc_vector) for doc_vector in doc_vectors]

    most_similar_idx = np.argsort(similarities)[-5:]

    print("Indices of the most similar sentences:", most_similar_idx)
    print("Similarities of the most similar sentences:", [similarities[i] for i in most_similar_idx])

def test_TF_IDF():
    model = Word2Vec.load("word2vec_model_tfidf.model")
    doc_vectors = np.load('doc_vectors_tfidf.npy')

    def load_preprocessed_data(filepath):
        with open(filepath, 'r', encoding='utf-8') as file:
            data = json.load(file)
        processed_texts = [value.split() for value in data.values()]
        return processed_texts, list(data.values())

    file_path = 'preprocessed_new_input.json'
    processed_texts, original_texts = load_preprocessed_data(file_path)

    tfidf_vectorizer = TfidfVectorizer(analyzer=lambda x: x)
    tfidf_vectorizer.fit([' '.join(text) for text in processed_texts])

    def document_vector_tfidf(word2vec_model, doc, tfidf_vectorizer):
        response = tfidf_vectorizer.transform([' '.join(doc)])
        feature_names = tfidf_vectorizer.get_feature_names_out()
        tfidf_scores = dict(zip(feature_names, response.toarray()[0]))
        
        weighted_doc_vector = np.zeros(word2vec_model.vector_size, dtype=np.float32)
        weight_sum = 0
        
        for word, score in tfidf_scores.items():
            if word in word2vec_model.wv:
                weighted_doc_vector += word2vec_model.wv[word] * score
                weight_sum += score
        
        if weight_sum > 0:
            weighted_doc_vector /= weight_sum
        
        return weighted_doc_vector

    def preprocess_text(text):
        text = BeautifulSoup(text, 'html.parser').get_text()
        
        text = text.lower()
        
        words = word_tokenize(text)
        
        stop_words = set(stopwords.words('english'))
        custom_stop_words = ['i', 'the']  
        all_stop_words = stop_words.union(custom_stop_words)
        
        words = [w for w in words if w.isalpha() and w not in all_stop_words]
        
        stemmer = PorterStemmer()
        stemmed = [stemmer.stem(w) for w in words]
        
        return stemmed

    custom_sentence = "throughput csma/cd csma/ca look discussion-9 slide , still confus cacul throughput csma/cd csma/ca."
    custom_sentence_processed = preprocess_text(custom_sentence)  
    custom_vector = document_vector_tfidf(model, custom_sentence_processed, tfidf_vectorizer)

    similarities = [1 - cosine(custom_vector, doc_vector) if not np.all(doc_vector == 0) else -1 for doc_vector in doc_vectors]
    most_similar_idx = np.argsort(similarities)[-5:]

    print("Indices of the most similar sentences:", most_similar_idx)
    for idx in most_similar_idx:
        print(f"Document {idx} Similarity: {similarities[idx]}")
        print(original_texts[idx])

test_TF_IDF()