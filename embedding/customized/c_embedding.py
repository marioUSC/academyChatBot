import json
from gensim.models import Word2Vec
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer


def average_word_embedding():
    def load_preprocessed_data(filepath):
        with open(filepath, 'r', encoding='utf-8') as file:
            data = json.load(file)
        processed_texts = [value.split() for value in data.values()]
        return processed_texts


    def document_vector(word2vec_model, doc):
        doc = [word for word in doc if word in word2vec_model.wv.index_to_key]
        if len(doc) == 0:
            return np.zeros(word2vec_model.vector_size)
        return np.mean(word2vec_model.wv[doc], axis=0)
    file_path = 'preprocessed_new_input.json'
    processed_texts = load_preprocessed_data(file_path)

    model = Word2Vec(sentences=processed_texts, vector_size=100, window=5, min_count=1, workers=4)

    doc_vectors = [document_vector(model, doc) for doc in processed_texts]

    model.save("word2vec_model.model")
    np.save('doc_vectors.npy', np.array(doc_vectors))

def TF_IDF():
    def load_preprocessed_data(filepath):
        with open(filepath, 'r', encoding='utf-8') as file:
            data = json.load(file)
        processed_texts = [value.split() for value in data.values()]
        return processed_texts, list(data.values())

    file_path = 'preprocessed_new_input.json'
    processed_texts, original_texts = load_preprocessed_data(file_path)

    model = Word2Vec(sentences=processed_texts, vector_size=100, window=5, min_count=1, workers=4)

    # 计算TF-IDF权重
    tfidf_vectorizer = TfidfVectorizer(analyzer=lambda x: x)
    tfidf_matrix = tfidf_vectorizer.fit_transform([' '.join(text) for text in processed_texts])

    # 获取词汇和IDF值
    feature_names = tfidf_vectorizer.get_feature_names_out()
    word2weight = dict(zip(feature_names, tfidf_vectorizer.idf_))

    def document_vector_tfidf(word2vec_model, doc_words, word2weight):
        # 初始化一个空向量
        doc_vector = np.zeros(word2vec_model.vector_size, dtype=np.float32)
        weight_sum = 0
        
        for word in doc_words:
            if word in word2vec_model.wv.key_to_index and word in word2weight:
                word_vector = word2vec_model.wv[word]
                word_idf = word2weight[word]
                
                # 更新文档向量
                doc_vector += word_vector * word_idf
                weight_sum += word_idf
        
        if weight_sum > 0:
            doc_vector /= weight_sum
        return doc_vector

    # 为每个文档生成加权平均向量
    doc_vectors_tfidf = [document_vector_tfidf(model, doc, word2weight) for doc in processed_texts]

    model.save("word2vec_model_tfidf.model")
    np.save('doc_vectors_tfidf.npy', np.array(doc_vectors_tfidf))

TF_IDF()