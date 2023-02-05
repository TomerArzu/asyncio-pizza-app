from app.restaurant import Restaurant
from app.use_cases.dough_chef_use_case import DoughChefUseCase
from app.use_cases.oven_use_case import OvenUseCase
from app.use_cases.report_use_case import ReportUseCase
from app.use_cases.topping_chef_use_case import ToppingsChefUseCase
from app.use_cases.waiter_use_case import WaiterUseCase
from domian.queues import Queues
from infra.consumer import Consumer
from infra.mongodb_repository import MongoDBRepository
from infra.producer import Producer

from flask_restful import Api
from flask import Flask

from infra.resources.orders_resource import OrdersResource

app = Flask(__name__)
api = Api(app)

# producer-consumer queues
queues = Queues()

# producers
orders_bulk_producer = Producer(queue=queues.dough_chefs_queue).bulk_producer
dough_chefs_producer = Producer(queues.toppings_chefs_queue)
toppings_chefs_re_producer = Producer(queues.toppings_chefs_queue)
toppings_chefs_producer = Producer(queues.oven_queue)
oven_producer = Producer(queues.waiters_queue)
waiters_producer = Producer(queues.completed_queue)

# consumers
dough_chefs_consumer = Consumer(queues.dough_chefs_queue)
toppings_chefs_consumer = Consumer(queues.toppings_chefs_queue)
oven_consumer = Consumer(queues.oven_queue)
waiters_consumer = Consumer(queues.waiters_queue)
completed_orders_consumer = Consumer(queues.completed_queue)

# repo

db_repository = MongoDBRepository()

# use case
dough_chef_use_case = DoughChefUseCase(
    dough_chef_consumer=dough_chefs_consumer,
    toppings_chefs_producer=dough_chefs_producer,
)
toppings_chef_use_case = ToppingsChefUseCase(
    toppings_chefs_consumer=toppings_chefs_consumer,
    toppings_chefs_producer=toppings_chefs_re_producer,
    oven_producer=toppings_chefs_producer,
)
oven_use_case = OvenUseCase(
    oven_consumer=oven_consumer,
    oven_producer=oven_producer,
)
waiter_use_case = WaiterUseCase(
    waiters_consumer=waiters_consumer,
    waiters_producer=waiters_producer
)
report_use_case = ReportUseCase(
    complete_orders_consumer=completed_orders_consumer,
    repository=db_repository
)

# app
restaurant = Restaurant(
    queues=queues,
    orders_bulk_producer=orders_bulk_producer,
    dough_chef_use_case=dough_chef_use_case,
    toppings_chef_use_case=toppings_chef_use_case,
    oven_use_case=oven_use_case,
    waiter_use_case=waiter_use_case,
    report_use_case=report_use_case
)

api.add_resource(
    OrdersResource,
    '/api/pizza/order',
    resource_class_kwargs={
        "handler": restaurant
    }
)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
    # from data_samples import order_doc
    # restaurant.post_orders(order_doc)
