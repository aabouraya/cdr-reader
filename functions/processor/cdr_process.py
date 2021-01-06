import json
import boto3
import os
import logging
import time

dynamodb = boto3.resource('dynamodb')


def aggregate_cdrs(event, context):
    cdr = json.loads(event['Records'][0]['body'])

    if cdr is None:
        logging.error("Validation Failed")
        raise Exception("Couldn't create a cdr record.")

    table = dynamodb.Table(os.environ['CDR_TABLE'])

    timestamp = str(time.time())

    item = {
        'id': cdr['imsi'],
        'imei': cdr['imei'],
        'msisdn': cdr['msisdn'],
        'record_date': cdr['date'],
        'duration': cdr['duration'],
        'data_in': cdr['data_in'],
        'data_out': cdr['data_out'],
        'ip': cdr['ip'],
        'createdAt': timestamp,
        'updatedAt': timestamp,
    }
    table.put_item(Item=item)
