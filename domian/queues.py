import asyncio


class Queues:
    def __init__(self):
        self._dough_chefs_queue = asyncio.Queue()
        self._toppings_chefs_queue = asyncio.Queue()
        self._oven_queue = asyncio.Queue()
        self._waiters_queue = asyncio.Queue()
        self._completed_queue = asyncio.Queue()

    @property
    def dough_chefs_queue(self):
        return self._dough_chefs_queue

    @property
    def toppings_chefs_queue(self):
        return self._toppings_chefs_queue

    @property
    def oven_queue(self):
        return self._oven_queue

    @property
    def waiters_queue(self):
        return self._waiters_queue

    @property
    def completed_queue(self):
        return self._completed_queue
