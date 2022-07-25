# pylint: disable=C0103
# invalid-name

import localstack_client.session as boto3
from app.database import get_db
from app.utils import settings
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/api/v1/utils",
    tags=["Utils"],
    responses={404: {"description": "Not found"}},
)


@router.get("/messages")
def read_messages():
    sqs_resource = boto3.resource("sqs", region_name=settings.REGION)
    queue = sqs_resource.get_queue_by_name(QueueName=settings.QUEUE_NAME)
    messages = queue.receive_messages(MessageAttributeNames=["All"], MaxNumberOfMessages=10, WaitTimeSeconds=1)
    for message in messages:
        print(f"Received message: {message.message_id}, {message.body}, {message.message_attributes}")
        # message.delete()
        # print(message.delete())
    return "test"
