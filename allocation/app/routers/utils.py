# pylint: disable=C0103, W0703
# invalid-name, broad-except

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


@router.get("/queue/{queue_name}")
def read_queue(queue_name: str):
    sqs_resource = boto3.resource("sqs", region_name=settings.REGION)
    try:
        queue = sqs_resource.get_queue_by_name(QueueName=queue_name)
        return {"url": queue.url, "attributes": queue.attributes}
    except Exception as exc:
        return {"error": "queue_does_not_exist", "msg": exc}


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


@router.post("/queues", response_model=schemas.Queue)
def create_queue(queue: schemas.QueueCreate):
    sqs_resource = boto3.resource("sqs", region_name=settings.REGION)
    queue = sqs_resource.create_queue(
        QueueName=queue.name, Attributes={"DelaySeconds": str(queue.delay), "VisibilityTimeout": str(queue.visibility)}
    )
    return queue
