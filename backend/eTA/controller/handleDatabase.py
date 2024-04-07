import json 
from eTA.service.embedding.dynamoDB import (
    create_new_table, create_new_table, check_table_exists,
    scan_items, get_and_print_item, delete_item, update_single_item,
    put_new_items
)
from eTA.service.embedding.sBert import (
    encode_text, encode_single_text, store_items_to_cloud, store_vedio_to_cloud
)

def handleUpload(data, courseID, fileID):
    if not check_table_exists(courseID):
        create_new_table(courseID)
    text_list = list(data.values())
    embedding_list = encode_text(text_list)
    upload_items = store_items_to_cloud(courseID, text_list, embedding_list, fileID)
    return put_new_items(courseID, upload_items) 

def handleVedioUpload(data, courseID, fileID):
    if not check_table_exists(courseID):
        create_new_table(courseID)
    timestamp_list = []
    text_list = []
    keyframeURL_list = []
    
    for item in data:
        # Append the values to the respective lists
        timestamp_list.append(item['timestamp'])
        text_list.append(item['content'])
        keyframeURL_list.append(item['keyframe URL'])
    embedding_list = encode_text(text_list)
    upload_items = store_vedio_to_cloud(courseID, timestamp_list, text_list, 
        embedding_list, keyframeURL_list, fileID)

    return put_new_items(courseID, upload_items) 

def handleScan(courseID, start_key=None, limit=2):
    if not check_table_exists(courseID):
        # message = {'message': 'Table not exist'} 
        return {'message': 'Table not exist'}
    return scan_items(courseID, start_key, limit)

def handleItemSearch(courseID, primary_key):
    if not check_table_exists(courseID):
        return jsonify({
            'status': 500, 
            'message': 'Table not exist'})
    
    return get_and_print_item(courseID, primary_key)

def handleDelete(courseID, primary_key):
    if not check_table_exists(courseID):
        return jsonify({
            'status': 500, 
            'message': 'Table not exist'})
    
    return delete_item(courseID, primary_key)

def handleModifyItem(updatedText, courseID, primary_key):
    if not check_table_exists(courseID):
        return jsonify({
            'status': 500, 
            'message': 'Table not exist'})
    newEmbedding = encode_single_text(updatedText)
    return update_single_item(courseID, primary_key, updatedText, newEmbedding)

def main():
    print(handleModifyItem("Question: how old is Mario Answer: 23", 'EE450',{"ID": "-3985936073442209917", "CreatedTime":"2024-03-04T14:23:53.473395"}))

if __name__ == '__main__':
    main()