from decimal import Decimal
import json
import boto3
import os
from Response import success_response, error_response
from boto3.dynamodb.conditions import Key

db = boto3.resource('dynamodb')


def get_single_message_handler(event, context):
    if (event['httpMethod'] != "GET"):
        return error_response(400, "Bad Request!")
    message_id = event['pathParameters']['id']
    if message_id is None:
        return error_response(400, "Message Id not missing!")
    try:
        table_name = os.environ.get('MESSAGE_TABLE')
        table = db.Table(table_name)
        response = table.query(KeyConditionExpression=Key('id').eq(message_id))
        return success_response(200, "Get message successfully", response)

    except Exception as e:
        print(e)
    finally:
        print("Finally block executed!")
