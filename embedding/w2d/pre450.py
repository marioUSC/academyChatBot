import json
import re
from gensim.models.doc2vec import Doc2Vec, TaggedDocument
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from bs4 import BeautifulSoup, MarkupResemblesLocatorWarning
import nltk
import warnings
# nltk.download('punkt')
# nltk.download('stopwords')
# nltk.download('wordnet')

def preprocess_text(text):
    warnings.filterwarnings("ignore", category=MarkupResemblesLocatorWarning)
    text = BeautifulSoup(text, 'html.parser').get_text()
    return text
    # words = word_tokenize(text)
    
    # stop_words = set(stopwords.words('english'))
    # words = [w for w in words if not w in stop_words]
    
    # lemmatizer = WordNetLemmatizer()
    # lemmatized = [lemmatizer.lemmatize(w) for w in words]
    
    # return ' '.join(lemmatized)


def preprocess_qa_pairs(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as file:
        data = json.load(file)
    
    preprocessed_data = {}
    
    for index, item in enumerate(data):
        combined_text = 'Question: ' + item['detail']['subject'] + ' ' + item['detail']['content'] + ' Answer: '
        for answer in item['answers']:
            combined_text += ' ' + answer['content']
        
        preprocessed_text = preprocess_text(combined_text)
        preprocessed_data[str(index)] = preprocessed_text
        
        # preprocessed_data[str(index)] = combined_text
    with open(output_file, 'w', encoding='utf-8') as file:
        json.dump(preprocessed_data, file, ensure_ascii=False, indent=4)

input_file = 'raw_post_450.json'  
output_file = 'preprocessed_new_input.json'  

preprocess_qa_pairs(input_file, output_file)
