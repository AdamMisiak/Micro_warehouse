import os

import boto3
from app.database import Base
from app.utils import exceptions
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from . import events

# sns_url = 'http://%s:4575' % os.environ['LOCALSTACK_HOSTNAME']
sqs_client = boto3.client("sqs", region_name="eu-west-1")
sqs_resource = boto3.resource("sqs", region_name="eu-west-1", endpoint_url="http://host.docker.internal:4566")


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
        print(sqs_resource.queues.all())
        sqs_queues = []
        for queue in sqs_resource.queues.all():
            sqs_queues.append(queue)

        # print(sqs_queues)
        # print(sqs_resource.queues.filter(
        #     QueueNamePrefix="micro-warehouse"))
        queue = sqs_resource.get_queue_by_name(QueueName="micro-warehouse-external-queue")
        print(queue)

        response = queue.send_message(MessageBody="world")
        print(response.get("MessageId"))
        print(response.get("MD5OfMessageBody"))

        for message in queue.receive_messages():
            print(message.body)

        # print(sqs_resource.create_queue(QueueName="micro-warehouse-external-queue",
        #                                      Attributes={
        #                                          'DelaySeconds': "0",
        #                                          'VisibilityTimeout': "60"
        #                                      }))

        # pobrac kolejke po nazwie i dodac do niej waidomosc, sprawdzic w konterze czy jest tam wiadomosc

        # TODO try to add event to queue there
        # events.OutOfStock(line.sku)

        # if self.can_allocate(line):
        #     self.quantity = int(self.quantity)
        #     self.quantity -= line.quantity
        #     line.batch = self
        # else:
        # raise exceptions.OutOfStock(f"Out of stock {self.sku}")
