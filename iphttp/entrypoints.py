import argparse
import asyncio

from iphttp import client


def run():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--kubo-maddr',
        dest='maddr',
        default='/ip4/127.0.0.1/tcp/5001'
    )
    parser.add_argument(
        nargs='*',
        dest='urlparts'
    )

    asyncio.run(client.execute(parser.parse_args()))
