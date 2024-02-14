import json
import boto3
import os
import uuid
from Response import success_response,error_response

s3_client = boto3.client('s3')
db = boto3.resource('dynamodb')


def create_message_handler(event, context):

    if ('body' not in event or event['httpMethod'] != "POST"):
        return error_response(400, "Bad Request!")

    request = json.loads(event['body'])

    if ('metadata' not in request):
        return error_response(400, "Metadata is required!")

    if not all(key in request['metadata'] for key in ('message_time', 'company_id', 'message_id')):
        return error_response(400, "All the fileds in metadata is required!")

    try:

        meta_data = request['metadata']
        data = request['data']

        save_json_file_to_s3(meta_data, data)
        save_data_to_database(meta_data, data)

        return success_response(201, "Message Created Successfully!")

    except Exception as e:
        print(e)
    finally:
        print("Finally block executed!")


def save_data_to_database(meta_data, data):
    data_set = {'id': str(uuid.uuid4()), 'message_id': meta_data['message_id'], 'company_id': meta_data['message_id'], 'order_id': data['order_id'],
                'order_amount': data['order_amount'], 'message_time': meta_data['message_time'], 'order_time': data['order_time']}

    table_name = os.environ.get('MESSAGE_TABLE')
    table = db.Table(table_name)
    table.put_item(TableName=table_name, Item=data_set)


def save_json_file_to_s3(meta_data, data):

    json_data = {
        "metadata": meta_data,
        "data": data
    }
    company_id = meta_data['company_id']
    message_id = meta_data['message_id']
    json_string = json.dumps(json_data)
    file_name = f"{company_id}/{message_id}.json"
    bucket_name = os.environ.get('S3_BUCKET_NAME')

    s3_client.put_object(Bucket=bucket_name,
                         Key=file_name, Body=json_string)
