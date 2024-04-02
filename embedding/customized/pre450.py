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
    
    # stop_words = set(stopwords.words('english'))
    # custom_stop_words = ['i', 'the']  
    # all_stop_words = stop_words.union(custom_stop_words)
    # words = [w for w in words if w not in all_stop_words]
    # stemmer = PorterStemmer()
    # stemmed = [stemmer.stem(w) for w in words]
    # return ' '.join(stemmed)
    return ' '.join(words)

def preprocess_qa_pairs(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as file:
        data = json.load(file)
    
    preprocessed_data = {}
    
    for index, item in enumerate(data):
        # Check if item itself is not None
        if item is not None:
            detail = item.get('detail')  # Use get to avoid KeyError
            subject = detail.get('subject', '') if detail else 'no detail'
            content = detail.get('content', '') if detail else 'provided'
            combined_text = f'Questions: {subject} {content} Answer: '

            # Check if 'answers' exists and has elements
            answers = item.get('answers')
            if answers:
                combined_text += ' '.join(answer['content'] for answer in answers)
            else:
                combined_text += 'no answer'
        else:
            combined_text = 'Questions: no item provided Answer: no answer'
        
        preprocessed_text = preprocess_text(combined_text)
        preprocessed_data[str(index)] = preprocessed_text
        
    with open(output_file, 'w', encoding='utf-8') as file:
        json.dump(preprocessed_data, file, ensure_ascii=False, indent=4)

input_file = 'ee599piazza_1.json'  
output_file = 'preprocessed_ee599.json'  

preprocess_qa_pairs(input_file, output_file)