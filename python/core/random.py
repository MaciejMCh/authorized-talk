import uuid


class Random:
    async def generate(self) -> bytes:
        raise Exception('dont use this base class')


class BuiltInRandom(Random):
    async def generate(self) -> bytes:
        return uuid.uuid4().bytes
