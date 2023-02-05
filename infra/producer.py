import asyncio


class Producer:
    def __init__(self, queue: asyncio.Queue):
        self._bulk_producer = None
        self._producer = None

        self._queue_to_produce = queue

    @property
    def bulk_producer(self):
        if self._bulk_producer is None:
            self._initialize_bulk_producer()
        return self

    def _initialize_bulk_producer(self):
        self._bulk_producer = asyncio.Event()
        self._bulk_producer.clear()

    async def wait_for_produce_bulk(self):
        await self._bulk_producer.wait()

    async def produce_bulk(
            self,
            data: list
    ):
        for data_record in data:
            await self._queue_to_produce.put(data_record)

        self._bulk_producer.set()

    async def produce(self, data):
        await self._queue_to_produce.put(data)
