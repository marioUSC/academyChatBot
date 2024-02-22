from sklearn.metrics.pairwise import cosine_similarity
import json
import numpy as np
import pandas as pd
from openai import OpenAI

client = OpenAI()

def get_embedding(text, model="text-embedding-3-small"):
    text = text.replace("\n", " ")
    response = client.embeddings.create(input=[text], model=model)
    return response.data[0].embedding

def find_top_similarities(question, embeddings_file, qa_json_file, top_n=3):
    # 获取问题的嵌入
    question_embedding = get_embedding(question)
    
    # 加载之前存储的嵌入向量
    embeddings = np.load(embeddings_file)
    
    # 计算与每个Q&A对的相似度
    similarities = cosine_similarity([question_embedding], embeddings)[0]
    
    # 获取最相似的top_n个索引
    top_indices = np.argsort(similarities)[-top_n:][::-1]
    
    # 加载原始的Q&A对
    with open(qa_json_file, 'r') as f:
        qa_pairs = json.load(f)
    
    # 打印最相似的Q&A对
    for idx in top_indices:
        print(f"Similarity: {similarities[idx]:.2f}, Index: {str(idx)} Q&A Pair: {qa_pairs[str(idx)]}")

question = "Question about answer to problem 40 For Problem 40 j), the congestion window is 1 at the 17th round, 2 at the 18th round, shouldn't it be 4 at the 19th round? Why is it 1?For k), can someone explains why does it send 21 packets at the round 22? I didn't get where the 21 come from?  I would really appreciate it. for k, I believe the 21 is due to it hitting the SS threshold and switching to CA.my guess for j is that it's one of the typo's the prof men"
find_top_similarities(question, 'embeddings.npy', 'notPre450.json')
