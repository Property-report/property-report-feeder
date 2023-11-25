from src import config
import boto3
import json
import time

from src.controllers.new_doc_sqs import NewDocSqs


class SqsPoller(object):
    def __init__(self):
        if config.LOCALSQS == "true":
            self.sqs = boto3.resource('sqs',
                                      endpoint_url='http://sqs:9324',
                                      region_name='elasticmq',
                                      aws_secret_access_key=config.AWS_ACCESS_KEY,
                                      aws_access_key_id=config.AWS_SECRET_KEY,
                                      use_ssl=False)
        else:
            self.sqs = boto3.resource('sqs',
                                      region_name='eu-west-2',
                                      aws_access_key_id=config.AWS_ACCESS_KEY,
                                      aws_secret_access_key=config.AWS_SECRET_KEY)

    def __open_sqs_connection(self):
        self.queue = self.sqs.get_queue_by_name(
            QueueName=config.SQS_QUEUE_NAME)

    def get_messages(self):
        self.__open_sqs_connection()
        messages = self.queue.receive_messages()
        if len(messages) == 0:
            return None
        else:
            message = messages[0].body
            messages[0].delete()
            return message

    def startPoller(self):
        self.__open_sqs_connection()
        print("Waiting for messages...", flush=True)

        while True:
            messages = self.queue.receive_messages(
                WaitTimeSeconds=20,  # Wait for up to 20 seconds for new messages
                MaxNumberOfMessages=1  # Receive one message at a time
            )

            if len(messages) > 0:
                for message in messages:
                    print("Handling message: {}".format(
                        message.body), flush=True)
                    start_time = time.time()  # Start timing
                    NewDocSqs(json.loads(message.body))
                    end_time = time.time()  # Stop timing
                    duration = end_time - start_time
                    print(
                        "Message processed in {:.2f} seconds".format(duration), flush=True)
                    message.delete()
            else:
                print("No message found. Waiting for new messages...", flush=True)
