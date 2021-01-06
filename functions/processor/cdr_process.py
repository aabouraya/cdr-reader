import json
from decimal import Decimal

import boto3
import os
import logging
import datetime
import uuid

dynamodb = boto3.resource('dynamodb')


def aggregate_cdrs(event, context):
    cdr = json.loads(event['Records'][0]['body'])

    if cdr is None:
        logging.error("Validation Failed")
        raise Exception("Couldn't create a cdr record.")

    table = dynamodb.Table(os.environ['CDR_TABLE'])

    now = datetime.now().strftime("%d/%m/%Y, %H:%M:%S")

    data_in = float(cdr['data_in']) / 1024
    data_out = float(cdr['data_out']) / 1024
    
    item = {
        'id': str(uuid.uuid1()),
        'imsi': cdr['imsi'],
        'imei': cdr['imei'],
        'msisdn': cdr['msisdn'],
        'record_date': cdr['date'],
        'duration': cdr['duration'],
        'data_in': Decimal(str(data_in)),
        'data_out': Decimal(str(data_out)),
        'ip': cdr['ip'],
        'createdAt': now,
        'updatedAt': now,
    }
    table.put_item(Item=item)
