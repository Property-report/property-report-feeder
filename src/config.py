import os

try:
    LOCALSQS = os.environ['LOCALSQS']
except:
    LOCALSQS = "false"

APP_NAME = os.environ['APP_NAME']
doc_location = "/opt/src/views/"

SQS_QUEUE_NAME = os.environ['SQS_QUEUE_NAME']
AWS_ACCESS_KEY = os.environ['AWS_ACCESS_KEY']
aws_access_key_id = os.environ['AWS_ACCESS_KEY']
AWS_SECRET_KEY = os.environ['AWS_SECRET_KEY']
aws_secret_access_key = os.environ['AWS_SECRET_KEY']


BUCKET_ID = os.environ['BUCKET_ID']
created_doc_folder = os.environ['created_doc_folder']
BUCKET_NAME = os.environ['BUCKET_NAME']

POLLING_INTERVAL = int(os.environ['POLLING_INTERVAL'])

POLLING_STATUS = False

email = os.environ['email']
email_pass = os.environ['email_pass']

CDN_URL = os.environ['CDN_URL']


property_information_api_url = os.environ['property_information_api_url']
ACCOUNT_API_URL = os.environ['ACCOUNT_API_URL']

website_url_cdn = os.environ['website_url_cdn']
