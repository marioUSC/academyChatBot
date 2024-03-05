import json 
from eTA.service.embedding.dynamoDB import (
    create_new_table, create_new_table, check_table_exists,
    scan_items
)
from eTA.service.embedding.sBert import encode_text


def handleUpload(data, courseID, fileID):
    if not check_table_exists(courseID):
        create_new_table(courseID)
    return encode_text(data, courseID, fileID)

def handleScan(courseID, start_key=None, limit=2):
    if not check_table_exists(courseID):
        message = {'message': 'Table not exist'} 
        message = json.dumps(message, default=str)
        return jsonify({'message': 'Table not exist'})
    return scan_items(courseID, start_key, limit)