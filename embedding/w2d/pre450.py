import json
import re
from gensim.models.doc2vec import Doc2Vec, TaggedDocument
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from bs4 import BeautifulSoup
import nltk

# 假设NLTK数据已经下载
# nltk.download('punkt')
# nltk.download('stopwords')
# nltk.download('wordnet')

def preprocess_text(text):
    # 移除HTML标签
    text = BeautifulSoup(text, 'html.parser').get_text()
    
    # 分词
    words = word_tokenize(text)
    
    # 转换为小写并移除标点符号/数字和停用词
    stop_words = set(stopwords.words('english'))
    words = [w for w in words if w.isalpha() and not w in stop_words]
    
    # 词形还原
    lemmatizer = WordNetLemmatizer()
    lemmatized = [lemmatizer.lemmatize(w) for w in words]
    
    return ' '.join(lemmatized)

def preprocess_qa_pairs(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as file:
        data = json.load(file)
    
    preprocessed_data = {}
    
    for index, item in enumerate(data):
        # 组合主题、内容和答案
        combined_text = item['detail']['subject'] + ' ' + item['detail']['content']
        for answer in item['answers']:
            combined_text += ' ' + answer['content']
        
        # 预处理组合文本
        preprocessed_text = preprocess_text(combined_text)
        
        preprocessed_data[str(index)] = preprocessed_text
    
    with open(output_file, 'w', encoding='utf-8') as file:
        json.dump(preprocessed_data, file, ensure_ascii=False, indent=4)

# 替换'input.json'为你的实际输入文件路径，'preprocessed_qa.json'为你希望输出的文件名
input_file = 'raw_post_450.json'  # 新的输入文件名
output_file = 'preprocessed_new_input.json'  # 输出文件名

preprocess_qa_pairs(input_file, output_file)
