"""
Sync server for controlling connected Launchpad Mini MK3 clients.
"""

import asyncio
import websockets
import json
import sys
from collections import namedtuple
from argparse import ArgumentParser
from functools import partial
from lpminimk3 import find_launchpads, Mode
from lpminimk3.graphics import Frame


_connected_clients = []


async def handler(lps, websocket, path):
    if path == "/sync":
        _connected_clients.append(websocket)
        try:
            while True:
                data = await websocket.recv()
                json_data = json.loads(data)
                for lp in lps:
                    lp.grid.render(Frame(json_data))
                websockets.broadcast(_connected_clients, data)
        finally:
            _connected_clients.remove(websocket)


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


def init_parser(ip, port):
    parser = ArgumentParser(description="Sync server for lpminimk3")
    parser.add_argument("-a",
                        "--all",
                        action="store_true",
                        help="Listen for all hosts (on 0.0.0.0)")
    parser.add_argument("-i",
                        "--ip",
                        help=f"IP to serve on (Default: {ip})")
    parser.add_argument("-p",
                        "--port",
                        type=int,
                        help=f"Port to bind to (Default: {port})")
    parser.add_argument("--version",
                        action="version",
                        version="%(prog) 0.1")
    return parser


async def main(*, ip="localhost", port=7654, allow_all_hosts=False):
    Args = namedtuple("Args", ["ip", "port", "all"])
    args = Args(ip, port, allow_all_hosts)
    parser = init_parser(ip, port)
    try:
        if len(sys.argv) > 1:
            args = parser.parse_args(sys.argv[1:])
        lps = find_lps()
        ip = "0.0.0.0" if args.all else args.ip
        ip = args.ip if args.ip else ip
        port = args.port if args.port else port
        if args.ip and args.all:
            print("Can't set both '--ip' and '--all'.", file=sys.stderr)
            parser.print_help()
            return 1
        else:
            await sync_with_sketch(lps, ip, port)
    except KeyboardInterrupt:
        return 1


if __name__ == "__main__":
    asyncio.run(main())
