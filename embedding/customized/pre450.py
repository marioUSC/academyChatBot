import json
import re
from gensim.models.doc2vec import Doc2Vec, TaggedDocument
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer, PorterStemmer
from bs4 import BeautifulSoup
import nltk

# nltk.download('punkt')
# nltk.download('stopwords')
# nltk.download('wordnet')

def preprocess_text(text):
    text = BeautifulSoup(text, 'html.parser').get_text()
    
    text = text.lower()
    
    words = word_tokenize(text)
    
    stop_words = set(stopwords.words('english'))
    custom_stop_words = ['i', 'the']  
    all_stop_words = stop_words.union(custom_stop_words)
    words = [w for w in words if w not in all_stop_words]
    stemmer = PorterStemmer()
    stemmed = [stemmer.stem(w) for w in words]
    return ' '.join(stemmed)

def preprocess_qa_pairs(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as file:
        data = json.load(file)
    
    preprocessed_data = {}
    
    for index, item in enumerate(data):
        combined_text = 'Questions: ' + item['detail']['subject'] + ' ' + item['detail']['content'] + 'Answer: '
        for answer in item['answers']:
            combined_text += ' ' + answer['content']
        
        preprocessed_text = preprocess_text(combined_text)
        preprocessed_data[str(index)] = preprocessed_text
        
    with open(output_file, 'w', encoding='utf-8') as file:
        json.dump(preprocessed_data, file, ensure_ascii=False, indent=4)

input_file = 'raw_post_450.json'  
output_file = 'preprocessed_new_input.json'  

preprocess_qa_pairs(input_file, output_file)