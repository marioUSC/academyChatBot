from sentence_transformers import SentenceTransformer
import numpy as np
import json
import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('e-TA')
table.put_item(
   Item={
        'CourseNumber': 'test101',
        'embedding': 0
    }
)
def store_data(content):
    return

def load_data(filepath):
    with open(filepath, 'r', encoding='utf-8') as file:
        data = json.load(file)
    qa_pairs = [value for value in data.values()]  # 直接使用已合并的Q&A对
    return qa_pairs

# 初始化SBERT模型
# model = SentenceTransformer('all-MiniLM-L6-v2')

# This model is designed for asysmetric query 
model = SentenceTransformer('msmarco-distilbert-base-v4')
# 加载Q&A对
qa_pairs = load_data('preprocessed_new_input.json')

# 编码Q&A对
qa_embeddings = model.encode(qa_pairs)

# 保存编码结果
np.save('qa_embeddings.npy', qa_embeddings)
