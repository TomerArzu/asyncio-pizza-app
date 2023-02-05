import asyncio


class Consumer:
    def __init__(self, queue: asyncio.Queue):
        self._consume_queue = queue

    async def consume(self):
        data = await self._consume_queue.get()
        return data

    async def join(self):
        await self._consume_queue.join()

    async def task_done(self):
        self._consume_queue.task_done()
