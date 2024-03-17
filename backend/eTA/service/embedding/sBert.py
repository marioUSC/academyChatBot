from sentence_transformers import SentenceTransformer
from eTA.service.embedding.dynamoDB import create_new_table, put_new_items
import numpy as np
import json
import boto3
import datetime

def store_items_to_cloud(table_name, texts, embeddings, file_name):
    if len(texts) != len(embeddings):
        err = "Error: The number of texts and embeddings must be the same."
        print(err)
        return err

    items = []
    for text, embedding in zip(texts, embeddings):
        embedding_list = embedding
        timestamp = datetime.datetime.now().isoformat()
        item = {
            'ID': str(hash(text)),  
            'OriginalText': text,
            'Embedding': embedding_list,
            'UploadSource': file_name,
            'CreatedTime': timestamp
        }
        items.append(item)
    return put_new_items(table_name, items)
    
def encode_text(data, courseID, fileID):
    """
    Encodes text data to embeddings using sBert and saves to DynamoDB.
    
    Args:
    - data (dict): Input data in JSON format where the values are the text to be encoded.
    - courseID (str): table name
    
    Returns:
    - str: status message
    """
    # Initialize the model for asymmetric query encoding
    model = SentenceTransformer('msmarco-distilbert-base-v4')

    # Extract values (original texts) from the input data
    original_text = list(data.values())

    # Encode the original texts to embeddings
    qa_embeddings = model.encode(original_text)
    
    # Initialize a list to hold the string representation of each embedding
    embeddings_str_list = []
    
    # Convert each embedding to a JSON string and add it to the list
    for embedding in qa_embeddings:
        embedding_str = json.dumps(embedding.tolist())  # Convert the NumPy array to a list and then to a JSON string
        embeddings_str_list.append(embedding_str)

    # Store the encoded embeddings and original texts in DynamoDB and return the status
    return store_items_to_cloud(courseID, original_text, embeddings_str_list, fileID)

