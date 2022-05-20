import sys
import asyncio
import json
from collections import namedtuple
from argparse import ArgumentParser
from websockets import connect
from lpminimk3 import find_launchpads, Mode
from lpminimk3.graphics import Frame


def find_lps():
    lps = []
    for lp in find_launchpads():
        lp.open()
        lp.mode = Mode.PROG
        lps.append(lp)
    return lps


async def sync_with_server(lps, host, port):
    uri = f"ws://{host}:{port}/sync"
    while True:
        async with connect(uri) as websocket:
            data = await websocket.recv()
            data = json.loads(data)
            for lp in lps:
                lp.grid.render(Frame(data))


async def main(*, ip=None, port=7654):
    Args = namedtuple("Args", ["ip", "port"])
    args = Args(ip, port)
    try:
        if len(sys.argv) > 1 or not ip:
            parser = ArgumentParser(description="Sync client for lpminimk3")
            parser.add_argument("-i",
                                "--ip",
                                required=True,
                                help="IP to serve on (Default: localhost)")
            parser.add_argument("-p",
                                "--port",
                                type=int,
                                help="Port to bind to (Default: 7654)")
            args = parser.parse_args(sys.argv[1:])
        lps = find_lps()
        ip = args.ip if args.ip else ip
        port = args.port if args.port else port
        if args.ip:
            await sync_with_server(lps, ip, port)
        else:
            print("No IP provided.")
            parser.print_help()
            return 1
    except KeyboardInterrupt:
        return 1


if __name__ == "__main__":
    asyncio.run(main())
