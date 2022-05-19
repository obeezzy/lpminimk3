import asyncio
import websockets
import json
import sys
from functools import partial
from lpminimk3 import find_launchpads, Mode
from lpminimk3.graphics import Frame


# Create handler for each connection
async def handler(lp, websocket, path):
    if path == "/sync":
        while True:
            data = await websocket.recv()
            data = json.loads(data)
            lp.grid.render(Frame(data))


def sync_with_sketch(lp):
    start_server = websockets.serve(partial(handler, lp), "localhost", 7654)
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()


def find_lp():
    lp = find_launchpads()[0]
    lp.open()
    lp.mode = Mode.PROG
    return lp


def main():
    try:
        lp = find_lp()
        sync_with_sketch(lp)
    except KeyboardInterrupt:
        print("Connection terminated.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
