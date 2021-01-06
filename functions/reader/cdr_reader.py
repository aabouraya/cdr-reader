import boto3
import os
import json

s3 = boto3.client('s3')
sqs = boto3.client('sqs')
queue_url = sqs.get_queue_url(QueueName=os.environ['CDR_QUEUE'])['QueueUrl']


def load_cdrs(bucket, key):
    response = s3.get_object(Bucket=bucket, Key=key)
    return response['Body'].iter_lines()


def publish_cdr(msg):
    response = sqs.send_message(
        QueueUrl=queue_url,
        MessageBody=msg
    )


def process_cdr(arr):
    data_set = {'imsi': arr[1], 'imei': arr[2], 'msisdn': arr[3], 'date': arr[4], 'duration': arr[6],
                'data_out': arr[11], 'data_in': arr[12], 'ip': arr[13]}
    return json.dumps(data_set)


def parse_cdr(event, context):
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']
    cdrs = load_cdrs(bucket, key)
    for cdr in cdrs:
        cdr_contents = cdr.decode('utf-8').split('|')
        msg = process_cdr(cdr_contents)
        publish_cdr(msg)
