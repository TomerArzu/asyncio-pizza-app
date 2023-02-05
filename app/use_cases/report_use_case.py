from datetime import datetime

from domian import PizzaInOrder
from domian.order_report import OrderReport, SinglePizzaReport
from domian.pizza_in_order import Orders
from domian.repository import DatabaseRepository
from infra.consumer import Consumer


class ReportUseCase:
    def __init__(
            self,
            complete_orders_consumer: Consumer,
            repository: DatabaseRepository
    ):
        self._complete_orders_consumer = complete_orders_consumer
        self._pizzas_in_order_report = []
        self._complete_report = None
        self._repository = repository

    async def execute(self, reporter_id):
        while True:
            print(f"'{reporter_id}' says: consuming orders...")
            order = await self._complete_orders_consumer.consume()
            if order is None:
                print(f"'{reporter_id}' says: order is None")
                break
            await self.prepare_report_for_single_order(order)
            await self._complete_orders_consumer.task_done()

    async def prepare_report_for_single_order(self, pizza_in_order: PizzaInOrder):
        start_time = datetime.fromtimestamp(pizza_in_order.start_time_total.timestamp())
        end_time = datetime.fromtimestamp(pizza_in_order.end_time_total.timestamp())
        total_time_in_seconds = end_time - start_time
        single_pizza_report = SinglePizzaReport(pizza_in_order.id, total_time_in_seconds.total_seconds())
        self._pizzas_in_order_report.append(single_pizza_report)
        print(f"Order id {single_pizza_report.id} completed in {single_pizza_report.total_preparation_time} ! "
              f"Bon Appetite")

    def _prepare_complete_report(self, order: Orders):
        total_preparation_time = \
            datetime.fromtimestamp(order.end_preparation_time) - datetime.fromtimestamp(order.start_preparation_time)
        total_report = OrderReport(
            id=order.id,
            saved_at=datetime.now(),
            total_preparation_time=total_preparation_time.total_seconds(),
            pizzas_in_order=self._pizzas_in_order_report
        )
        self._complete_report = total_report

    def export_total_orders_report(self, order: Orders):
        self._prepare_complete_report(order)
        self._repository.save(self._complete_report)
        self._pizzas_in_order_report.clear()
        self._complete_report = None