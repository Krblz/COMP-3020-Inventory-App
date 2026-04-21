import subprocess
import sys
subprocess.call([sys.executable, "-m", "pip", "install", "python-ulid", "typing_extensions", "-t", "/tmp"])
sys.path.insert(0, "/tmp")

import json
import boto3
import os
from ulid import ULID
from decimal import Decimal

def lambda_handler(event, context):
    try:
        data = json.loads(event['body'])
    except KeyError:
        return {
            'statusCode': 400,
            'body': json.dumps("Bad request. Please provide the data.")
        }

    table_name = os.getenv('TABLE_NAME', 'Inventory')
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(table_name)

    unique_id = str(ULID())

    try:
        table.put_item(
            Item={
                'item_id': unique_id,
                'item_name': data['item_name'],
                'item_description': data['item_description'],
                'item_qty_on_hand': int(data['item_qty_on_hand']),
                'item_price': Decimal(str(data['item_price'])),
                'location_id': int(data['location_id'])
            }
        )
        return {
            'statusCode': 200,
            'body': json.dumps(f"Item with ID {unique_id} added successfully.")
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps(f"Error adding item: {str(e)}")
        }