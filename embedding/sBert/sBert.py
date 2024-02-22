from sentence_transformers import SentenceTransformer
import numpy as np
import json

# 加载数据
def load_data(filepath):
    with open(filepath, 'r', encoding='utf-8') as file:
        data = json.load(file)
    qa_pairs = [value for value in data.values()]  # 直接使用已合并的Q&A对
    return qa_pairs

# 初始化SBERT模型
model = SentenceTransformer('all-MiniLM-L6-v2')

# 加载Q&A对
qa_pairs = load_data('preprocessed_new_input.json')

# 编码Q&A对
qa_embeddings = model.encode(qa_pairs)

# 保存编码结果
np.save('qa_embeddings.npy', qa_embeddings)
