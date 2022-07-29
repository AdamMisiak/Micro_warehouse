# pylint: disable=C0103
# invalid-name
from typing import List

import localstack_client.session as boto3
from app.domain import schemas
from app.utils import settings
from fastapi import APIRouter

router = APIRouter(
    prefix="/api/v1/utils",
    tags=["Utils"],
    responses={404: {"description": "Not found"}},
)


@router.get("/queues", response_model=List[schemas.Queue])
def read_queues():
    sqs_client = boto3.client("sqs", region_name=settings.REGION)
    queues = sqs_client.list_queues().get("QueueUrls")
    results = [{"url": queue} for queue in queues]
    return results


@router.get("/messages", response_model=List[schemas.Message])
def read_messages():
    sqs_resource = boto3.resource("sqs", region_name=settings.REGION)
    queue = sqs_resource.get_queue_by_name(QueueName=settings.QUEUE_NAME)
    messages = queue.receive_messages(MessageAttributeNames=["All"], MaxNumberOfMessages=10, WaitTimeSeconds=1)
    results = [
        {"id": message.message_id, "body": message.body, "attributes": message.message_attributes}
        for message in messages
    ]
    # for message in messages:
    #     print(f"Received message: {message.message_id}, {message.body}, {message.message_attributes}")
    # message.delete()
    # print(message.delete())
    return results


@router.delete("/messages", response_model=List[schemas.Message])
def delete_all_messages():
    sqs_resource = boto3.resource("sqs", region_name=settings.REGION)
    queue = sqs_resource.get_queue_by_name(QueueName=settings.QUEUE_NAME)
    queue.purge()
    messages = queue.receive_messages(MessageAttributeNames=["All"], MaxNumberOfMessages=10, WaitTimeSeconds=1)
    results = [
        {"id": message.message_id, "body": message.body, "attributes": message.message_attributes}
        for message in messages
    ]
    return results


# TODO zamienic zeby uzywac tego modelu events tutaj faktyfcznie, sprawdz jak to robili w ksiazce
# a potem druga apka
