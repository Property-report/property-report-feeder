from src.dependencies.sqs import SqsPoller


def run():
    sqsPoller = SqsPoller()
    sqsPoller.startPoller()
