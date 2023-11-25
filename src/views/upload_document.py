from src import config
import boto
import boto3
from botocore.client import Config


keyId = config.aws_access_key_id
sKeyId = config.aws_secret_access_key
conn = boto.connect_s3(keyId, sKeyId, is_secure=False,
                       host='s3.eu-west-2.amazonaws.com')
boto.config.add_section('s3')
boto.config.set('s3', 'use-sigv4', 'True')
boto.config.set('s3', 'host', 's3.eu-west-2.amazonaws.com')

s3 = boto3.resource('s3',
                    aws_access_key_id=keyId,
                    aws_secret_access_key=sKeyId)

client = boto3.client('s3',
                      aws_access_key_id=keyId,
                      aws_secret_access_key=sKeyId,
                      config=Config(signature_version='s3v4'),
                      region_name='eu-west-2')

# this posts documents to amazon s3 folder


def document_upload(folder_name, document, doc_name, type):
    bucket = conn.get_bucket(config.BUCKET_ID, validate=False)
    key_pass = "0011223344556677"
    with open(document, 'rb') as f:
        file = f.read()
    print(config.BUCKET_ID)
    print(config.BUCKET_NAME)
    print(config.BUCKET_NAME + '/' + folder_name + '/' + doc_name+'.'+type)
    upload = client.put_object(Bucket=config.BUCKET_ID, Key=config.BUCKET_NAME +
                               '/' + folder_name + '/' + doc_name+'.'+type, Body=file)
    return "success"


def document_upload_pdf(folder_name, file, doc_name, type):
    bucket = conn.get_bucket(config.BUCKET_ID, validate=False)

    print(config.BUCKET_NAME + '/' + folder_name + '/' + doc_name+'.'+type)

    upload = client.put_object(Bucket=config.BUCKET_ID, Key=config.BUCKET_NAME +
                               '/' + folder_name + '/' + doc_name+'.'+type, Body=file)
    return "success"
