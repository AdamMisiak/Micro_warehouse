import os

# import boto3
import localstack_client.session as boto3
from app.database import Base
from app.utils import exceptions
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from . import events

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
        return self.sku == line.sku and int(self.quantity) >= int(line.quantity)

    def allocate(self, line: Order):
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
        queue = sqs_resource.get_queue_by_name(QueueName="micro-warehouse-external-queue")
        print(queue)
        print("--" * 50)

        response = queue.send_message(
            MessageAttributes={
                "Type": {"DataType": "String", "StringValue": "out_of_stock"},
                "Sku": {"DataType": "String", "StringValue": "BIG-TABLE"},
            },
            MessageBody="BIG-TABLE",
        )

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

        print(response)
        print(response.get("MessageId"))
        # print(response.get("MD5OfMessageBody"))

        # TODO oczyscic cala kolejke zeby byla pusta
        # TODO sprawdzic czemu jest tylko 1 wiadmosc w kolejce
        # TODO na atrybuty sprawdz metode z tego: https://boto3.amazonaws.com/v1/documentation/api/latest/guide/sqs.html

        for message in queue.receive_messages():
            print(message.body)
            print(message.message_attributes)
            print("--" * 50)
            # print(message.attributes)
            # print(dir(message))

        # print(sqs_resource.create_queue(QueueName="micro-warehouse-external-queue",
        #                                      Attributes={
        #                                          'DelaySeconds': "0",
        #                                          'VisibilityTimeout': "60"
        #                                      }))

        # TODO try to add event to queue there
        # events.OutOfStock(line.sku)

        # if self.can_allocate(line):
        #     self.quantity = int(self.quantity)
        #     self.quantity -= line.quantity
        #     line.batch = self
        # else:
        # raise exceptions.OutOfStock(f"Out of stock {self.sku}")
