import boto3
import json
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

    table.meta.client.get_waiter('table_exists').wait(TableName='MyOnDemandTable')

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
        'items': items
    }
    result_json = json.dumps(result, default=str)
    # print(result_json)
    return result_json

def main():
    return

if __name__ == '__main__':
    main()