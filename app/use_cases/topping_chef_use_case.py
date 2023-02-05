import asyncio
from datetime import datetime

from infra.consumer import Consumer
from infra.producer import Producer


class ToppingsChefUseCase:
    def __init__(
            self,
            toppings_chefs_consumer: Consumer,
            toppings_chefs_producer: Producer,
            oven_producer: Producer,

    ):
        self._toppings_chefs_consumer = toppings_chefs_consumer
        self._toppings_chefs_producer = toppings_chefs_producer
        self._oven_producer = oven_producer

    async def execute(self, chef_id):
        while True:
            print(f"'{chef_id}': is attempting to get from order from queue...")
            order = await self._toppings_chefs_consumer.consume()
            if order is None:
                print(f"'{chef_id}': order is None - Breaking")
                break
            start_time_snapshot = datetime.now()
            print(f"'{chef_id}': order consumed! order_id={order.id}")
            pizza_toppings_list = order.toppings
            handled_toppings = 0
            print(f"'{chef_id}': there are {len(pizza_toppings_list)} toppings requested! order_id={order.id}\n{pizza_toppings_list}")
            while pizza_toppings_list and handled_toppings < 2:
                handled_toppings = handled_toppings + 1
                pizza_toppings_list.pop(0)
                await asyncio.sleep(4)
            if pizza_toppings_list:
                print(f"'{chef_id}': there are more {len(pizza_toppings_list)} toppings order_id={order.id}\npublish to toppings chefs again")
                await self._toppings_chefs_producer.produce(order)
            else:
                end_time_snapshot = datetime.now()
                order.assign_timestamp(start_time_snapshot, end_time_snapshot)
                order.move_to_next_step()
                # Produce to oven
                await self._oven_producer.produce(order)
                print(f"'{chef_id}' says: order has been placed in Oven queue! order.id={order.id}")
                print(f"'{chef_id}' says: order produced at {end_time_snapshot} order.id={order.id}")
            await self._toppings_chefs_consumer.task_done()