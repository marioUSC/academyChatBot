import boto3
import json
import time
from flask import Flask, request, jsonify
dynamodb = boto3.resource('dynamodb')
def create_new_table(name):
    table = dynamodb.create_table(
        TableName=name,
        KeySchema=[
            {
                'AttributeName': 'ID',
                'KeyType': 'HASH'  
            },
            {
                'AttributeName': 'CreatedTime',
                'KeyType': 'RANGE' 
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'ID',
                'AttributeType': 'S'  
            },
            {
                'AttributeName': 'CreatedTime',
                'AttributeType': 'S'  
            }
        ],
        BillingMode='PAY_PER_REQUEST'
    )

    table.meta.client.get_waiter('table_exists').wait(TableName=name)

    print(f"Table {table.table_name} created successfully in On-Demand mode.")
    return

def put_new_items(table_name, items):
    if not check_table_exists(table_name):
        err = f"Table {table_name} does not exist or error occurred."
        print(err)
        return err

    table = dynamodb.Table(table_name)
    with table.batch_writer() as batch:
        for item in items:
            batch.put_item(Item=item)

    status = f"Table {table_name} write finished."
    print(status)
    return status

def check_table_exists(table_name):
    try:
        table = dynamodb.Table(table_name)
        _ = table.table_status  
        return True  
    except dynamodb.meta.client.exceptions.ResourceNotFoundException:
        return False
    except Exception:
        return False

def query_items(table_name, partition_key_value, limit=2, start_key=None):
    """
    Query items from a DynamoDB table in descending order based on a timestamp sort key.
    
    Args:
    - table_name (str): Name of the DynamoDB table.
    - partition_key_value (str): Value of the partition key to query.
    - limit (int): Maximum number of items to return.
    - start_key (dict): The starting point for the query (exclusive), provided as the
                        last evaluated key from a previous query. None starts from the latest item.
    
    Returns:
    - dict: Contains the queried items and the last evaluated key for pagination.
    """
    table = dynamodb.Table(table_name)
    
    query_params = {
        'KeyConditionExpression': 'ID = :pk',
        'ExpressionAttributeValues': {
            ':pk': partition_key_value
        },
        'ScanIndexForward': False,  
        'Limit': limit
    }
    
    if start_key:
        query_params['ExclusiveStartKey'] = start_key

    response = table.query(**query_params)

    # Extracting items and the last evaluated key for further pagination
    items = response.get('Items', [])
    last_evaluated_key = response.get('LastEvaluatedKey')

    return {
        'Items': items,
        'LastEvaluatedKey': last_evaluated_key
    }

def scan_items(table_name, start_key=None, limit=2):
    table = dynamodb.Table(table_name)

    scan_kwargs = {
        'Limit': limit
    }

    if start_key:
        scan_kwargs['ExclusiveStartKey'] = start_key

    response = table.scan(**scan_kwargs)

    items = response['Items']
    start_key = response.get('LastEvaluatedKey', None)

    result = {
        'returned_count': len(items),
        'startKey': start_key,
        'items': items,
        'message': 'scan successful',
        'status': 200
    }

    return result

def get_and_print_item(table_name, primary_key):
    table = dynamodb.Table(table_name)
    try:
        response = table.get_item(
            Key=primary_key
        )
        item = response.get('Item', None)
        if item:
            data = item
            message = 'Item found'
            status = 200
        else:
            data = 'None'
            message = 'Item not exist'
            status = 404
        
        result = {
            'status': status,
            'message': message, 
            'data' : data
        }
        # result = json.dumps(result, default=str)
        return result
        
    except Exception as e:
        print("Error getting item:", e)
        result = {
            'status': 500,
            'message': 'Exception catached', 
            'data' : 'None'
        }
        # result = json.dumps(result, default=str)
        return result

def delete_item(table_name, primary_key):
    table = dynamodb.Table(table_name)
    try:
        response = table.delete_item(
            Key=primary_key
        )
        result = {
            'status': 200,
            'message': 'Deleted successfully', 
            'data' : 'None'
        }
        return result
    except Exception as e:
        result = {
            'status': 400,
            'message': 'Exception catached when deleting the item', 
            'data' : 'None'
        }
        return result

def scan_all_items(table_name):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(table_name)

    scan_kwargs = {}
    items = []

    while True:
        response = table.scan(**scan_kwargs)
        items.extend(response['Items'])

        if 'LastEvaluatedKey' not in response:
            break  

        scan_kwargs['ExclusiveStartKey'] = response['LastEvaluatedKey']
        # break

    return items

def update_single_item(table_name, primary_key, original_text, embedding):
    table = dynamodb.Table(table_name)

    update_expression = 'SET OriginalText = :originalText, Embedding = :embedding'

    try:
        table.update_item(
            Key=primary_key,
            UpdateExpression=update_expression,
            ExpressionAttributeValues={
                ':originalText': original_text,
                ':embedding': embedding
            },
            ReturnValues="UPDATED_NEW"
        )
        return {'status': 200, 'message': 'Item updated successfully'}
    except Exception as e:
        return {'status': 400, 'message': str(e)}

def list_dynamodb_tables(region_name='us-west-1'):
    """
    List all tables in DynamoDB for the specified region.

    :param region_name: AWS region name as a string.
    :return: List of DynamoDB table names.
    """
    # Initialize the DynamoDB client for the specified region
    dynamodb = boto3.client('dynamodb', region_name=region_name)

    # Get and return the list of table names
    return dynamodb.list_tables()['TableNames']

def main():
    print(list_dynamodb_tables())
    return

if __name__ == '__main__':
    main()