# import os

# import boto3
import localstack_client.session as boto3
from app.database import Base
# from app.domain import events
from app.utils import exceptions, settings
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

# from . import events

# sns_url = 'http://%s:4575' % os.environ['LOCALSTACK_HOSTNAME']
sqs_client = boto3.client("sqs", region_name="eu-west-1")
# FOR BASIC BOTO3 version
# sqs_resource = boto3.resource("sqs", region_name="eu-west-1", endpoint_url="http://host.docker.internal:4566")
sqs_resource = boto3.resource("sqs", region_name="eu-west-1")


class Order(Base):
    __tablename__ = "order"

    id = Column(Integer, primary_key=True)
    sku = Column(String, default=None)
    quantity = Column(Integer, default=10)
    batch_id = Column(Integer, ForeignKey("batch.id"))
    batch = relationship("Batch", back_populates="order")

    def is_allocated(self) -> bool:
        return self.batch is not None


class Batch(Base):
    __tablename__ = "batch"

    id = Column(Integer, primary_key=True, index=True, nullable=True, default=None)
    sku = Column(String, default=None)
    reference = Column(String, default=None)
    quantity = Column(Integer, default=10)
    eta = Column(DateTime, nullable=True)
    order = relationship("Order", back_populates="batch")

    def can_allocate(self, line: Order) -> bool:
        # TODO needs to be splittied into -> out of stock and wrong sku
        return self.sku == line.sku and int(self.quantity) >= int(line.quantity)

    def allocate(self, line: Order):
        # print(events.OutOfStock)
        # LIST QUEUEUES
        # print(sqs_resource.queues.all())
        # sqs_queues = []
        # for queue in sqs_resource.queues.all():
        #     sqs_queues.append(queue)

        # LIST QUEUEUES
        # queues = sqs_client.list_queues()
        # print(queues)
        # print('--'*50)

        # GET QUEUE
        # queue = sqs_resource.get_queue_by_name(QueueName=settings.QUEUE_NAME)
        # print(queue)
        # print("--" * 50)

        # SEND MESSAGE TO QUEUE - NOT SURE IF IT WORKS
        # response = queue.send_message(
        #     MessageAttributes={
        #         "Type": {"DataType": "String", "StringValue": "OutOfStock"},
        #         "Sku": {"DataType": "String", "StringValue": "BIG-TABLE"},
        #     },
        #     MessageBody="OutOfStock",
        # )
        # print(response)
        # print(response.get("MessageId"))
        # print(response.get("MD5OfMessageBody"))

        # response = queue.send_message(
        #     # QueueUrl='string',
        #     MessageBody='string',
        #     DelaySeconds=123,
        #     MessageAttributes={
        #         'Type': {
        #             'DataType': 'String',
        #             'StringValue': 'out_of_stock'
        #         }
        #     },
        #     MessageSystemAttributes={
        #         'Type': {
        #             'DataType': 'String',
        #             'StringValue': 'out_of_stock'
        #         },
        #     },
        # )

        # TODO oczyscic cala kolejke zeby byla pusta
        # TODO sprawdzic czemu jest tylko 1 wiadmosc w kolejce
        # TODO na atrybuty sprawdz metode z tego: https://boto3.amazonaws.com/v1/documentation/api/latest/guide/sqs.html

        # GET MESSAGES
        # print("MESSAGES:")
        # messages = queue.receive_messages(MessageAttributeNames=["All"], MaxNumberOfMessages=10, WaitTimeSeconds=1)
        # for message in messages:
        #     print(f"Received message: {message.message_id}, {message.body}, {message.message_attributes}")

        # DELETE MESSAGE
        # print(message.delete())

        # CREATTE QUUEUE- CHYBA DZIALA - MOZE TEST FIFO?
        # print(sqs_resource.create_queue(QueueName="micro-warehouse-external-queue",
        #                                      Attributes={
        #                                          'DelaySeconds': "0",
        #                                          'VisibilityTimeout': "60"
        #                                      }))

        # TODO try to add event to queue there
        # events.OutOfStock(line.sku)

        if self.can_allocate(line):
            self.quantity = int(self.quantity)
            self.quantity -= line.quantity
            line.batch = self
        else:
            print("ELSE")
            queue = sqs_resource.get_queue_by_name(QueueName=settings.QUEUE_NAME)
            queue.send_message(
                MessageAttributes={
                    "Type": {"DataType": "String", "StringValue": "OutOfStock"},
                    "Sku": {"DataType": "String", "StringValue": self.sku},
                },
                MessageBody="OutOfStock",
            )
            raise exceptions.OutOfStock(f"Out of stock {self.sku}")
            # TODO change to return
