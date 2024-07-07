from mcaio.client import AIOMCServer
from os import environ
from sys import argv
from asyncio import run as aiorun


def get_env(key: str) -> str:
    val = environ.get(key)
    if val is None:
        raise ValueError
    return val


def arg() -> str:
    if len(argv) != 2:
        raise RuntimeError
    return argv[1]


async def get_name(server: AIOMCServer) -> str:
    return await server.name


async def get_motd(server: AIOMCServer) -> str:
    return await server.motd


async def get_count(server: AIOMCServer) -> int:
    return await server.players_count


async def get_max(server: AIOMCServer) -> int:
    return await server.players_count


async def action() -> None:
    try:
        HOST, PORT = get_env("MC_HOST"), int(get_env("MC_PORT"))
        server = AIOMCServer(HOST, PORT)
        match arg():
            case 'name':
                out = get_name(server)
            case 'pmax':
                out = get_max(server)
            case 'pcount':
                out = get_count(server)
            case 'motd':
                out = get_motd(server)
            case _:
                raise RuntimeError
        print(await out)
    except ValueError or TypeError:
        print("ERROR: BAD ENV VARS")
    except RuntimeError:
        print("Bad args")
    except ConnectionRefusedError:
        print("Connection error")


def main():
    aiorun(action())


if __name__ == "__main__":
    main()
