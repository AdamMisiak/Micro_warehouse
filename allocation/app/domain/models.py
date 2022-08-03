import localstack_client.session as boto3
from app.database import Base
from app.utils import settings
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

# sqs_client = boto3.client("sqs", region_name="eu-west-1")
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
            return None

        # print(asdict(events.OutOfStock(sku="BIG-TABLE")))
        queue = sqs_resource.get_queue_by_name(QueueName=settings.QUEUE_NAME)
        attributes = {
            "event_type": {"DataType": "String", "StringValue": "OutOfStock"},
            "sku": {"DataType": "String", "StringValue": self.sku},
        }
        body = "OutOfStock"
        queue.send_message(
            MessageAttributes=attributes,
            MessageBody=body,
        )
        return {"event_type": body, "sku": self.sku}
