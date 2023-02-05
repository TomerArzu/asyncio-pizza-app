import asyncio
from datetime import datetime

from infra.consumer import Consumer
from infra.producer import Producer


class WaiterUseCase:
    def __init__(
            self,
            waiters_consumer: Consumer,
            waiters_producer: Producer
    ):
        self._waiters_consumer = waiters_consumer
        self._waiters_producer = waiters_producer

    async def execute(self, waiter_id):
        while True:
            print(f"'{waiter_id}' says: consuming orders...")
            order = await self._waiters_consumer.consume()
            if order is None:
                print(f"'{waiter_id}' says: order is None")
                break
            start_time_snapshot = datetime.now()
            print(f"'{waiter_id}' says: order consumed! order.id={order.id}")
            print(f"'{waiter_id}' says: order consumed at {start_time_snapshot} order.id={order.id}")
            await asyncio.sleep(5)
            end_time_snapshot = datetime.now()
            order.assign_timestamp(start_time_snapshot, end_time_snapshot)
            order.end_time_total = end_time_snapshot
            order.move_to_next_step()
            await self._waiters_producer.produce(order)
            print(f"'{waiter_id}' says: order has been placed in Completed Pizzas queue! order.id={order.id}")
            print(f"'{waiter_id}' says: order produced at {end_time_snapshot} order.id={order.id}")
            await self._waiters_consumer.task_done()
