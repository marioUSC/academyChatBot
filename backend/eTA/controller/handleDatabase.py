import json 
from eTA.service.embedding.dynamoDB import (
    create_new_table, create_new_table, check_table_exists,
    scan_items, get_and_print_item
)
from eTA.service.embedding.sBert import encode_text


def handleUpload(data, courseID, fileID):
    if not check_table_exists(courseID):
        create_new_table(courseID)
    return encode_text(data, courseID, fileID)

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

