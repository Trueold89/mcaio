from asyncio import open_connection as aiocon, StreamReader, StreamWriter
from abc import ABC, abstractmethod
from collections.abc import Iterable
from struct import pack as struct_pack
from json import loads as jl


class AIOConnection(object):
    reader: StreamReader
    writer: StreamWriter

    def __init__(self, host: str, port: int) -> None:
        self.host = host
        self.port = port

    async def __aenter__(self) -> "AIOConnection":
        self.reader, self.writer = await aiocon(self.host, self.port)
        return self

    async def __aexit__(self, exc_type, exc, tb) -> None:
        self.writer.close()
        await self.writer.wait_closed()

    async def send(self, msg: bytes) -> None:
        if not self.writer:
            raise ConnectionRefusedError
        self.writer.write(msg)
        await self.writer.drain()

    async def receive(self, n: int) -> bytes:
        if not self.reader:
            raise ConnectionRefusedError
        resp = await self.reader.read(n)
        return resp


class IMCServer(ABC):

    def __init__(self, host: str, port: int) -> None:
        """
        :param host: Minecraft server ip or hostname
        :param port: Minecraft server port
        """
        self.host = host
        self.port = port

    @property
    @abstractmethod
    async def players_count(self) -> int | None:
        """
        Returns current number of players on server

        :return: Number of players on server
        """
        raise NotImplementedError

    @property
    @abstractmethod
    async def name(self) -> str | None:
        """
        Returns server core name

        :return: Server name
        """
        raise NotImplementedError

    @property
    @abstractmethod
    async def maxplayers(self) -> int | None:
        """
        Returns max number of players available on server

        :return: Max number of players
        """
        raise NotImplementedError

    @property
    @abstractmethod
    async def motd(self) -> str | None:
        """
        Returns Message of the day

        :return: Server motd
        """
        raise NotImplementedError

    @property
    @abstractmethod
    async def players_list(self) -> Iterable:
        """
        Returns iterable object with online players nicknames

        :return: Players nicknames iterable object
        """
        raise NotImplementedError

    @property
    @abstractmethod
    async def all_info(self) -> dict:
        """
        Returns dict with all information about server

        :return: All information about server
        """
        raise NotImplementedError


class AIOMCServer(IMCServer):

    _name: str | None
    _max: int | None
    _count: int | None
    _motd: str | None
    _data: bytes
    _players: Iterable

    def __init__(self, host: str, port: int) -> None:
        super().__init__(host, port)
        self._data = self._pack_data(
                b"\x00\x00" + self._pack_data(self.host.encode('utf8')) + self.
                _pack_port(self.port) + b"\x01")
        self.clean()

    @staticmethod
    async def _unpack_varint(s):
        d = 0
        for i in range(5):
            b = ord(await s.receive(1))
            d |= (b & 0x7F) << 7 * i
            if not b & 0x80:
                break
        return d

    @staticmethod
    def _pack_varint(d):
        o = b""
        while True:
            b = d & 0x7F
            d >>= 7
            o += struct_pack("B", b | (0x80 if d > 0 else 0))
            if d == 0:
                break
        return o

    def _pack_data(self, d):
        h = self._pack_varint(len(d))
        if isinstance(d, str):
            d = bytes(d, "utf-8")
        return h + d

    def clean(self) -> None:
        self._name = None
        self._motd = None
        self._max = None
        self._count = None
        self._players = ()

    @staticmethod
    def _pack_port(i):
        return struct_pack('>H', i)

    async def _get_data(self) -> dict:
        async with AIOConnection(self.host, self.port) as socket:
            await socket.send(self._data)
            await socket.send(self._pack_data("\x00"))
            await self._unpack_varint(socket)
            await self._unpack_varint(socket)
            lent = await self._unpack_varint(socket)
            d = b""
            while len(d) < lent:
                d += await socket.receive(1024)
            return jl(d.decode('utf8'))

    async def update(self) -> None:
        data = await self._get_data()
        self.clean()
        self._name = data["version"]["name"]
        self._motd = data["description"]
        if isinstance(self._motd, dict):
            self._motd = self._motd["text"]
        players = data["players"]
        self._count = int(players["online"])
        self._max = int(players["max"])
        if "sample" in tuple(players.keys()):
            self._players = tuple(map(lambda player: player["name"],
                                      players["sample"]))

    @property
    async def players_count(self) -> int | None | None:
        await self.update()
        return self._count

    @property
    async def name(self) -> str | None | None:
        await self.update()
        return self._name

    @property
    async def maxplayers(self) -> int | None | None:
        await self.update()
        return self._max

    @property
    async def motd(self) -> str | None | None:
        await self.update()
        return self._motd

    @property
    async def players_list(self) -> Iterable:
        await self.update()
        return self._players

    @property
    async def all_info(self) -> dict:
        await self.update()
        return {
                "name": self._name,
                "motd": self._motd,
                "players": {
                    "max": self._max,
                    "online": self._count,
                    "list": self._players
                    }
                }
