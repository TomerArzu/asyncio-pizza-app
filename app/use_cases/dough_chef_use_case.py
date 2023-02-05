import asyncio
from datetime import datetime

from infra.consumer import Consumer
from infra.producer import Producer


class DoughChefUseCase:
    def __init__(
            self,
            dough_chef_consumer: Consumer,
            toppings_chefs_producer: Producer,
    ):
        self._dough_chef_consumer = dough_chef_consumer
        self._toppings_chefs_producer = toppings_chefs_producer

    async def execute(self, chef_id):
        while True:
            print(f"'{chef_id}' says: consuming orders...")
            order = await self._dough_chef_consumer.consume()
            if order is None:
                print(f"'{chef_id}' says: order is None")
                break
            start_time_snapshot = datetime.now()
            print(f"'{chef_id}' says: order consumed! order.id={order.id}")
            print(f"'{chef_id}' says: order consumed at {start_time_snapshot} order.id={order.id}")
            await asyncio.sleep(7)
            end_time_snapshot = datetime.now()
            order.assign_timestamp(start_time_snapshot, end_time_snapshot)
            order.move_to_next_step()
            order.start_time_total = start_time_snapshot
            await self._toppings_chefs_producer.produce(order)
            print(f"'{chef_id}' says: order has been placed in Toppings chef queue! order.id={order.id}")
            print(f"'{chef_id}' says: order produced at {end_time_snapshot} order.id={order.id}")
            await self._dough_chef_consumer.task_done()
