import asyncio
import uuid
from datetime import datetime
from app.use_cases.dough_chef_use_case import DoughChefUseCase
from app.use_cases.oven_use_case import OvenUseCase
from app.use_cases.report_use_case import ReportUseCase
from app.use_cases.topping_chef_use_case import ToppingsChefUseCase
from app.use_cases.waiter_use_case import WaiterUseCase
from const import NUM_OF_DOUGH_CHEFS, NUM_OF_TOPPINGS_CHEFS, NUM_OF_OVENS, NUM_OF_WAITERS
from domian import PizzaInOrder

from domian.pizza_in_order import Orders
from domian.queues import Queues
from infra.producer import Producer


class Restaurant:
    def __init__(
            self,
            queues: Queues,
            orders_bulk_producer: Producer,
            dough_chef_use_case: DoughChefUseCase,
            toppings_chef_use_case: ToppingsChefUseCase,
            oven_use_case: OvenUseCase,
            waiter_use_case: WaiterUseCase,
            report_use_case: ReportUseCase,
    ):
        self._queues = queues

        self._orders_bulk_producer = orders_bulk_producer

        self._start_time_for_orders = None
        self._end_time_for_orders = None

        self._dough_chef_use_case = dough_chef_use_case
        self._toppings_chef_use_case = toppings_chef_use_case
        self._oven_use_case = oven_use_case
        self._waiter_use_case = waiter_use_case
        self._report_use_case = report_use_case

    async def place_orders(self, orders: Orders):
        tasks = []

        await self.init_restaurant_workers(tasks)
        tasks.append(
            asyncio.create_task(self._orders_bulk_producer.produce_bulk(data=orders.pizzas_in_order))
        )

        await self._orders_bulk_producer.wait_for_produce_bulk()
        await self._queues.dough_chefs_queue.join()
        await self._queues.toppings_chefs_queue.join()
        await self._queues.oven_queue.join()
        await self._queues.waiters_queue.join()
        await self._queues.completed_queue.join()

        orders.end_preparation_time = datetime.now().timestamp()
        self._report_use_case.export_total_orders_report(orders)

    async def init_restaurant_workers(self, tasks):
        for i in range(NUM_OF_DOUGH_CHEFS):
            tasks.append(asyncio.create_task(self._dough_chef_use_case.execute(f"dough_chef-{i}")))
        for i in range(NUM_OF_TOPPINGS_CHEFS):
            tasks.append(asyncio.create_task(self._toppings_chef_use_case.execute(f"toppings_chef-{i}")))
        for i in range(NUM_OF_OVENS):
            tasks.append(asyncio.create_task(self._oven_use_case.execute(f"oven-{i}")))
        for i in range(NUM_OF_WAITERS):
            tasks.append(asyncio.create_task(self._waiter_use_case.execute(f"waiter-{i}")))
        tasks.append(
            asyncio.create_task(self._report_use_case.execute("reporter"))
        )

    def post_orders(self, orders):
        orders = self.prepare_orders(orders)
        asyncio.run(self.place_orders(orders))

    @staticmethod
    def prepare_orders(orders) -> Orders:
        print(orders)
        orders = orders.get("orders")
        pizzas_list = []
        for pizza in orders:
            toppings = pizza.get("toppings")
            if not toppings:
                pizza.update({"toppings": []})
            incoming_id = pizza.get("id")
            if not incoming_id:
                pizza.update({"id": str(uuid.uuid4())})

            pizzas_list.append(PizzaInOrder(**pizza))

        orders = Orders(
            id=str(uuid.uuid4()),
            start_preparation_time=datetime.now().timestamp(),
            pizzas_in_order=pizzas_list,
        )
        return orders

    @staticmethod
    async def assign_order_timestamp(order, start_time_snapshot, end_time_snapshot):
        if order.state == PizzaInOrder.OrderState.INCOMING_ORDER:
            order.start_time_total = start_time_snapshot
        elif order.state == PizzaInOrder.OrderState.DOUGH_CHEF:
            order.start_time_dough = start_time_snapshot
            order.end_time_dough = end_time_snapshot
        elif order.state == PizzaInOrder.OrderState.TOPPING_CHEF:
            order.start_time_toppings = start_time_snapshot
            order.end_time_toppings = end_time_snapshot
        elif order.state == PizzaInOrder.OrderState.OVEN:
            order.start_time_oven = start_time_snapshot
            order.end_time_oven = end_time_snapshot
        elif order.state == PizzaInOrder.OrderState.WAITER:
            order.start_time_serve = start_time_snapshot
            order.end_time_serve = end_time_snapshot
        elif order.state == PizzaInOrder.OrderState.COMPLETED:
            order.end_time_total = end_time_snapshot
