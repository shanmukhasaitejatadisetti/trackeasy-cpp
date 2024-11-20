# sqs_handler/sqs_handler.py

import boto3
import json

class SQSHandler:
    def __init__(self, region_name):
        self.sqs = boto3.client('sqs', region_name=region_name)

    def send_message(self, queue_url, message_body, message_attributes=None):
        """
        Send a message to an SQS queue.

        :param queue_url: The SQS queue URL.
        :param message_body: The body of the message as a dictionary.
        :param message_attributes: Additional message attributes as a dictionary (optional).
        :return: Response from the SQS send_message call.
        """
        try:
            response = self.sqs.send_message(
                QueueUrl=queue_url,
                MessageBody=json.dumps(message_body),
                MessageAttributes=message_attributes or {}
            )
            return response
        except Exception as e:
            raise RuntimeError(f"Failed to send message: {str(e)}")

    def receive_messages(self, queue_url, max_number=1, wait_time=0):
        """
        Receive messages from an SQS queue.

        :param queue_url: The SQS queue URL.
        :param max_number: The maximum number of messages to receive (default: 1).
        :param wait_time: Wait time for the receive operation (default: 0 seconds).
        :return: List of messages.
        """
        try:
            response = self.sqs.receive_message(
                QueueUrl=queue_url,
                MaxNumberOfMessages=max_number,
                WaitTimeSeconds=wait_time
            )
            return response.get('Messages', [])
        except Exception as e:
            raise RuntimeError(f"Failed to receive messages: {str(e)}")
