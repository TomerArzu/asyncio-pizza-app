import asyncio
from datetime import datetime

from infra.consumer import Consumer
from infra.producer import Producer


class OvenUseCase:
    def __init__(
            self,
            oven_consumer: Consumer,
            oven_producer: Producer,
    ):
        super().__init__()
        self._oven_consumer = oven_consumer
        self._oven_producer = oven_producer

    async def execute(self, oven_id: str):
        while True:
            print(f"'{oven_id}' says: consuming orders...")
            order = await self._oven_consumer.consume()
            if order is None:
                print(f"'{oven_id}' says: order is None")
                break
            start_time_snapshot = datetime.now()
            print(f"'{oven_id}' says: order consumed! order.id={order.id}")
            print(f"'{oven_id}' says: order consumed at {start_time_snapshot} order.id={order.id}")
            await asyncio.sleep(10)
            end_time_snapshot = datetime.now()
            order.assign_timestamp(start_time_snapshot, end_time_snapshot)
            order.move_to_next_step()
            await self._oven_producer.produce(order)
            print(f"'{oven_id}' says: order has been placed in Waiters queue! order.id={order.id}")
            print(f"'{oven_id}' says: order produced at {end_time_snapshot} order.id={order.id}")
            await self._oven_consumer.task_done()
