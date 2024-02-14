import json
import boto3
import os
import uuid


def create_message_handler(event, context):

    if ('body' not in event or event['httpMethod'] != "POST"):
        return {
            "statusCode": 400,
            "body": json.dumps({
                "error": "Bad Request!",
            }),
        }

    request_body = json.loads(event['body'])

    if ('metadata' not in request_body):
        return {
            "statusCode": 400,
            "body": json.dumps({
                "error": "metadata is required",
            }),
        }

    # if not all(key in request_body for key in ('message_time', 'company_id', 'message_id')):
    #     return {
    #         "statusCode": 400,
    #         "body": json.dumps({
    #             "error": "All the fileds in metadata is required",
    #         }),
    #     }
    
    try:
        request = json.loads(event['body'])
        meta_data = request['metadata']
        data = request['data']
        data_set = {'message_id': meta_data['message_id'], 'company_id': meta_data['message_id'], 'order_id': data['order_id'],
                    'order_amount': data['order_amount'], 'message_time': meta_data['message_time'], 'order_time': data['order_time']}
        db = boto3.resource('dynamodb')
        table_name = os.environ.get('MESSAGE_TABLE')
        table = db.Table(table_name)
        response = table.put_item(TableName=table_name, Item=data_set)

        return {
            "statusCode": 201,
            "body": json.dumps({"success": "create successfully"}),
        }

    except Exception as e:
        print(e)
    finally:
        print("all done")
