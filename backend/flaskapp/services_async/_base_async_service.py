import asyncio
from abc import ABCMeta, abstractmethod
from asyncio import Queue, Task
from typing import Iterator, Optional, Tuple, Union, List


class _AsyncQueueAbstract(metaclass=ABCMeta):

    def __init__(self, maxsize=4):
        self.consumers: Optional[Tuple[Task]] = None
        self.queue: Optional[Queue] = None  # must be initialized in an async method
        self.maxsize = maxsize

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    @abstractmethod
    def run_tasks(self, *args, **kwargs):
        raise NotImplementedError()

    @abstractmethod
    async def produce(self, *args) -> None:
        raise NotImplementedError()

    @abstractmethod
    async def consume(self) -> None:
        raise NotImplementedError()

    def cancel_consumers(self):
        if not self.consumers:
            return

        for c in self.consumers:
            c.cancel()

    def close(self):
        self.cancel_consumers()

    @abstractmethod
    async def create_tasks(self, *args):
        raise NotImplementedError()


class AsyncQueue(_AsyncQueueAbstract):

    MAX_NUMBER_OF_PRODUCERS = 500

    def run_tasks(self, work_load: Union[List, Tuple]):
        max_size = AsyncQueue.MAX_NUMBER_OF_PRODUCERS
        for _ids in (work_load[n: n + max_size] for n in range(0, len(work_load), max_size)):
            asyncio.run(self.create_tasks(_ids))

    @abstractmethod
    async def produce(self, *args) -> None:
        raise NotImplementedError()

    @abstractmethod
    async def consume(self) -> None:
        raise NotImplementedError()

    async def create_tasks(self, tasks: Iterator):
        self.queue = Queue(maxsize=self.maxsize)
        # run to all images
        producers = (asyncio.create_task(self.produce(task)) for task in tasks)
        self.consumers = tuple(asyncio.create_task(self.consume()) for _ in range(self.queue.maxsize))
        await asyncio.gather(*producers)
        await self.queue.join()


class AsyncQueueOneProducer(_AsyncQueueAbstract):

    def run_tasks(self):
        asyncio.run(self.create_tasks())

    @abstractmethod
    async def produce(self, *args) -> None:
        raise NotImplementedError()

    @abstractmethod
    async def consume(self) -> None:
        raise NotImplementedError()

    async def create_tasks(self):
        self.queue = Queue(maxsize=self.maxsize)
        # run to all images
        self.consumers = tuple(asyncio.create_task(self.consume()) for _ in range(self.queue.maxsize))
        await self.produce()
        await self.queue.join()