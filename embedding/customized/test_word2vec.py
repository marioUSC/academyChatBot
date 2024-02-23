import sys
from gensim.models import Word2Vec

def find_similar_words(keyword, model_path='word2vec_model.model', top_n=5):
    model = Word2Vec.load(model_path)
    
    similar_words = model.wv.most_similar(keyword, topn=top_n)
    
    return similar_words

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python test_word2vec.py <keyword>")
        sys.exit(1)
    
    keyword = sys.argv[1]
    similar_words = find_similar_words(keyword)
    
    print(f"Top {len(similar_words)} words similar to '{keyword}':")
    for word, similarity in similar_words:
        print(f"{word}: {similarity}")
