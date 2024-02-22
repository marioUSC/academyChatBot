import json
import numpy as np
import pandas as pd
from openai import OpenAI

client = OpenAI()

def get_embedding(text, model="text-embedding-3-small"):
    text = text.replace("\n", " ")
    response = client.embeddings.create(input=[text], model=model)
    return response.data[0].embedding

def process_and_store_embeddings(json_file, embeddings_file):
    with open('notPre450.json', 'r') as f:
        qa_pairs = json.load(f)

    df = pd.DataFrame(list(qa_pairs.items()), columns=['id', 'combined'])
    
    df['embedding'] = df['combined'].apply(lambda x: get_embedding(x, model='text-embedding-ada-002'))
    
    embeddings = np.array(df['embedding'].tolist())
    np.save(embeddings_file, embeddings)

process_and_store_embeddings('qa_pairs.json', 'embeddings.npy')
