import localstack_client.session as boto3

# import boto3
# from app.utils import settings


def main():
    print("Event consumer started")
    sqs_resource = boto3.resource("sqs", region_name="eu-west-1")
    queue = sqs_resource.get_queue_by_name(QueueName="micro-warehouse-external-queue")
    messages = queue.receive_messages(MessageAttributeNames=["All"], MaxNumberOfMessages=10, WaitTimeSeconds=1)
    results = [
        {"id": message.message_id, "body": message.body, "attributes": message.message_attributes}
        for message in messages
    ]
    for message in results:
        print(message)
        # TODO add sending email
        # TODO why messages are in queue event after receiving?
        # TODO new branch testing? mailing?


if __name__ == "__main__":
    main()
