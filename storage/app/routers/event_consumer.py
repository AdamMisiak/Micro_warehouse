import localstack_client.session as boto3
from app.utils import settings


def main():
    print("Event consumer started")
    sqs_resource = boto3.resource("sqs", region_name=settings.REGION)
    queue = sqs_resource.get_queue_by_name(QueueName=settings.QUEUE_NAME)
    messages = queue.receive_messages(MessageAttributeNames=["All"], MaxNumberOfMessages=10, WaitTimeSeconds=1)
    results = [
        {"id": message.message_id, "body": message.body, "attributes": message.message_attributes}
        for message in messages
    ]
    print(results)


if __name__ == "__main__":
    main()
