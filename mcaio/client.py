from asyncio import open_connection as aiocon, StreamReader, StreamWriter


class AIOConnection(object):

    reader: StreamReader
    writer: StreamWriter

    def __init__(self, host: str, port: int) -> None:
        self.host = host
        self.port = port

    async def __aenter__(self) -> "AIOConnection":
        self.reader, self.writer = await aiocon(self.host, self.port)
        return self

    async def __aexit__(self) -> None:
        self.writer.close()
        await self.writer.wait_closed()

    async def send(self, msg: str) -> None:
        if self.writer:
            self.writer.write(msg.encode())
            await self.writer.drain()
        raise ConnectionRefusedError

    async def receive(self) -> str:
        if self.reader:
            resp = await self.reader.read(100)
            return resp.decode()
        raise ConnectionRefusedError
