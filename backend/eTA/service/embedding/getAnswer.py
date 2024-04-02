from gensim.models.doc2vec import Doc2Vec
from nltk.tokenize import word_tokenize
import json
import os
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from scipy.spatial import distance
from scipy.spatial.distance import cosine

from eTA.service.embedding.dynamoDB import (scan_items, scan_all_items)

def find_similar_questions_backup(test_sentence, topK = 3):
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

def find_similar_questions(test_sentence, table_name, topK=3):
    items = scan_all_items(table_name)  # Assuming scan_all_items is defined elsewhere
    model = SentenceTransformer('msmarco-distilbert-base-v4')
    test_sentence_embedding = model.encode([test_sentence])  # This is 2-D

    # Calculate similarity and keep related info
    items_with_similarity = []
    for item in items:
        # Assuming item['Embedding'] is a string representation of the embedding
        item_embedding_str = item['Embedding']
        item_embedding = np.array(eval(item_embedding_str))
        
        # Ensure the embeddings are 1-D for the cosine function
        similarity = 1 - cosine(test_sentence_embedding[0], item_embedding)
        items_with_similarity.append((item, similarity))

    # Sort by similarity and get topK items
    items_with_similarity.sort(key=lambda x: x[1], reverse=True)
    top_similar_items = items_with_similarity[:topK]

    # Prepare the final result
    similar_questions = []
    for i, (item, similarity) in enumerate(top_similar_items, start=1):
        question = item.get('OriginalText', 'Question not found.')
        formatted_question = f"pair {i}: Similarity Score: {similarity:.4f}, Question: {question}\n"
        similar_questions.append(formatted_question)

    return similar_questions

if __name__ == '__main__':
    # Example usage:
    test_sentence = "How to calculate CSMA/CD?"
    similar_questions = find_similar_questions(test_sentence, "EE450", 3)
    for question in similar_questions:
        print(question)
