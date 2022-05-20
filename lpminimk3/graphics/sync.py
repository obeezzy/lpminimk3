import asyncio
import websockets
import json
import sys
from collections import namedtuple
from argparse import ArgumentParser
from functools import partial
from lpminimk3 import find_launchpads, Mode
from lpminimk3.graphics import Frame


async def handler(lps, websocket, path):
    if path == "/sync":
        while True:
            data = await websocket.recv()
            json_data = json.loads(data)
            for lp in lps:
                lp.grid.render(Frame(json_data))
            await websocket.send(data)


async def sync_with_sketch(lps, host, port):
    async with websockets.serve(partial(handler, lps), host, port):
        await asyncio.Future()


def find_lps():
    lps = []
    for lp in find_launchpads():
        lp.open()
        lp.mode = Mode.PROG
        lps.append(lp)
    return lps


async def main(*, ip="localhost", port=7654, allow_all_hosts=False):
    Args = namedtuple("Args", ["ip", "port", "all"])
    args = Args(ip, port, allow_all_hosts)
    try:
        if len(sys.argv) > 1:
            parser = ArgumentParser(description="Sync server for lpminimk3")
            parser.add_argument("-a",
                                "--all",
                                action="store_true",
                                metavar="ALL_HOSTS",
                                help="Listen for all hosts (on '0.0.0.0')")
            parser.add_argument("-i",
                                "--ip",
                                help="IP to serve on (Default: localhost)")
            parser.add_argument("-p",
                                "--port",
                                type=int,
                                help="Port to bind to (Default: 7654)")
            parser.add_argument("--version",
                                action="version",
                                version="%(prog) 0.1")
            args = parser.parse_args(sys.argv[1:])
            if args.ip and args.all:
                raise RuntimeError("Can't set both '--ip' and '--all'.")
        lps = find_lps()
        ip = "localhost" if not args.ip else args.ip
        ip = "0.0.0.0" if args.all else ip
        port = args.port if args.port else port
        await sync_with_sketch(lps, ip, port)
    except KeyboardInterrupt:
        return 1


if __name__ == "__main__":
    asyncio.run(main())
