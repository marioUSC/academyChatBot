import json
import re
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from bs4 import BeautifulSoup
import nltk

# Download necessary NLTK data
# nltk.download('punkt')
# nltk.download('stopwords')
# nltk.download('wordnet')

def preprocess_text(text):
    # Remove HTML tags
    # text = BeautifulSoup(text, 'html.parser').get_text()
    
    # # Tokenize
    # words = word_tokenize(text)
    
    # # Lowercase and remove punctuation/numbers and stop words
    # # words = [word.lower() for word in words if word.isalpha()]
    # stop_words = set(stopwords.words('english'))
    # words = [w for w in words if not w in stop_words]
    
    # # Lemmatize
    # lemmatizer = WordNetLemmatizer()
    # lemmatized = [lemmatizer.lemmatize(w) for w in words]
    
    # return ' '.join(lemmatized)
    return text

def preprocess_qa_pairs(input_file, output_file):
    with open(input_file, 'r') as file:
        data = json.load(file)
    
    preprocessed_data = {}
    
    index = 0
    for key, value in data.items():
        # Combine subject, content, and answers
        combined_text = value['detail']['subject'] + ' ' + value['detail']['content']
        for answer in value['answers'].values():
            combined_text += ' ' + answer
        
        # Preprocess combined text
        preprocessed_text = preprocess_text(combined_text)
        
        preprocessed_data[index] = preprocessed_text
        index += 1
    
    with open(output_file, 'w') as file:
        json.dump(preprocessed_data, file, indent=4)

# Replace 'input.json' with the path to your actual input file and 'preprocessed_qa.json' with your desired output file name
input_file = 'raw_post_450.json'
output_file = 'preprocessed_post_450.json'

preprocess_qa_pairs(input_file, output_file)
