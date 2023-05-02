"""Sync client for the Launchpad MK3.
"""

import sys
import asyncio
import json
from collections import namedtuple
from argparse import ArgumentParser
from websockets import connect
from lpminimk3 import find_launchpads, Mode
from lpminimk3.graphics import Frame


def _find_lps():
    lps = []
    for lp in find_launchpads():
        lp.open()
        lp.mode = Mode.PROG
        lps.append(lp)
    return lps


async def _sync_with_server(lps, host, port):
    uri = f"ws://{host}:{port}/sync"
    async with connect(uri) as websocket:
        while True:
            data = await websocket.recv()
            data = json.loads(data)
            for lp in lps:
                lp.grid.render(Frame(data))


def _init_parser(port):
    parser = ArgumentParser(description="Sync client example "
                                        "for lpminimk3")
    parser.add_argument("-i",
                        "--ip",
                        required=True,
                        help="Server IP")
    parser.add_argument("-p",
                        "--port",
                        type=int,
                        help=f"Server port (Default: {port})")
    return parser


async def main(*, ip=None, port=7654):
    """Runs script.

    Parameters
    ----------
    ip : str or None
        IP address to connect to.
    port : int
        Port to connect to.
    """
    Args = namedtuple("Args", ["ip", "port"])
    args = Args(ip, port)
    parser = _init_parser(port)
    try:
        if len(sys.argv) > 1 or not ip:
            args = parser.parse_args(sys.argv[1:])
        lps = _find_lps()
        ip = args.ip if args.ip else ip
        port = args.port if args.port else port
        if not ip:
            print("No IP provided.", file=sys.stderr)
            parser.print_help()
            return 1
        else:
            await _sync_with_server(lps, ip, port)
    except KeyboardInterrupt:
        return 1


if __name__ == "__main__":
    asyncio.run(main())
