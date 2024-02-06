from gensim.models.doc2vec import Doc2Vec
from nltk.tokenize import word_tokenize
import json
import os

def find_similar_questions(test_sentence, topK = 3):
    current_dir = os.path.dirname(__file__)
    model_path = os.path.join(current_dir, 'src', 'd2v.model')
    model_path = os.path.normpath(model_path)
    # Load the model
    model = Doc2Vec.load(model_path)
    
    # Tokenize the test sentence
    test_data = word_tokenize(test_sentence.lower())
    v1 = model.infer_vector(test_data)

    # Load the mapping from the tags to the original texts
    map_path = os.path.join(current_dir, 'src', 'tag_to_text_map.json')
    map_path = os.path.normpath(map_path)
    with open(map_path, 'r', encoding='utf-8') as file:
        tag_to_text = json.load(file)

    # Find the most similar documents
    similar_docs = model.dv.most_similar([v1], topn = topK)
    similar_questions = []

    for i, (tag, similarity) in enumerate(similar_docs, start=1):
        indicator = f"pair {i}"
        question_with_indicator = f"{indicator}: {tag_to_text[str(tag)]}\n"  
        similar_questions.append(question_with_indicator)

    return similar_questions

if __name__ == '__main__':
    # Example usage:
    test_sentence = "where should I return the gateway"
    similar_questions = find_similar_questions(test_sentence)
    for question in similar_questions:
        print(question)
