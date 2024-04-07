from sentence_transformers import SentenceTransformer
# from eTA.service.embedding.dynamoDB import create_new_table, put_new_items
import numpy as np
import json
import boto3
import datetime

MODEL = 'msmarco-distilbert-base-v4'

def store_items_to_cloud(table_name, texts, embeddings, file_name, item_type = 'Q&A'):
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
            'CreatedTime': timestamp,
            'itemType': item_type
        }
        items.append(item)
    return items
    # return put_new_items(table_name, items)

def store_vedio_to_cloud(table_name, timestamps, texts, embeddings, frameURLs, file_name, item_type = 'vedio'):
    items = []
    for timestamp, text, embedding, frameURL in zip(timestamps, texts, embeddings, frameURLs):
        timestamp = datetime.datetime.now().isoformat()
        item = {
            'ID': str(hash(text)), 
            'timeInterval': timestamp,
            'OriginalText': text,
            'Embedding': embedding,
            'frameURL': frameURL,
            'UploadSource': file_name,
            'CreatedTime': timestamp,
            'itemType': item_type
        }
        items.append(item)
    return items

# def encode_text(data, courseID, fileID):
def encode_text(text_list):
    """
    Encodes text data to embeddings using sBert and saves to DynamoDB.
    
    Args:
    - data (dict): Input data in JSON format where the values are the text to be encoded.
    - courseID (str): table name
    
    Returns:
    - str: status message
    """
    # Initialize the model for asymmetric query encoding
    model = SentenceTransformer(MODEL)

    # Encode the original texts to embeddings
    qa_embeddings = model.encode(text_list)
    
    # Initialize a list to hold the string representation of each embedding
    embeddings_str_list = []
    
    # Convert each embedding to a JSON string and add it to the list
    for embedding in qa_embeddings:
        embedding_str = json.dumps(embedding.tolist())  # Convert the NumPy array to a list and then to a JSON string
        embeddings_str_list.append(embedding_str)

    # Store the encoded embeddings and original texts in DynamoDB and return the status
    return embeddings_str_list

def encode_single_text(data):
    model = SentenceTransformer(MODEL)
    qa_embeddings = model.encode(data)
    return str(qa_embeddings.tolist())
