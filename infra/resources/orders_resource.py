from flask import request
from flask_restful import Resource


class OrdersResource(Resource):
    def __init__(self, **kwargs):
        self._handler = kwargs['handler']

    def post(self):
        orders = request.get_json()
        self._handler.post_orders(orders)
        return 200  # always positive
