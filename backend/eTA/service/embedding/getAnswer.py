from gensim.models.doc2vec import Doc2Vec
from nltk.tokenize import word_tokenize
import json
import os
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


def find_similar_questions(test_sentence, topK = 3):
    current_dir = os.path.dirname(__file__)
    model_path = os.path.join(current_dir, 'src', 'qa_embeddings.npy')
    model_path = os.path.normpath(model_path)

    map_path = os.path.join(current_dir, 'src', 'EE450Piazza.json')
    map_path = os.path.normpath(map_path)
    # given_sentence = "How to calculate CSMA/CD?"
    # given_sentence = "When TCP encounters a datagram that exceeds the MTU size, does it fragment the original data into several TCP segments?"
    qa_embeddings = np.load(model_path)
    model = SentenceTransformer('all-MiniLM-L6-v2')
    test_sentence_embedding = model.encode([test_sentence])

    similarities = cosine_similarity(test_sentence_embedding, qa_embeddings)

    most_similar_indices = np.argsort(similarities[0])[::-1][:topK]

    # print("Indices of the most similar Q&A pairs:", most_similar_indices)
    for idx in most_similar_indices:
        print(f"Similarity Score: {similarities[0][idx]:.4f}, Index: {idx}")

    with open(map_path, 'r') as file:
        index_to_question = json.load(file)

    similar_questions = []
    for i, idx in enumerate(most_similar_indices, start=1):
        question = index_to_question.get(str(idx), "Question not found.")
        similarity_score = similarities[0][idx]
        formatted_question = f"pair {i}: Similarity Score: {similarity_score:.4f}, Question: {question}\n"
        similar_questions.append(formatted_question)

    return similar_questions


if __name__ == '__main__':
    # Example usage:
    test_sentence = "How to calculate CSMA/CD?"
    similar_questions = find_similar_questions(test_sentence)
    for question in similar_questions:
        print(question)
