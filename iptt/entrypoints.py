import argparse
import asyncio
import os.path
import sys
import uvloop

from iptt.iphttp import client
from iptt.iphttp import server


def parser_common():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--kubo-maddr',
        dest='maddr',
        default='/ip4/127.0.0.1/tcp/5001'
    )
    parser.add_argument(
        '-i',
        dest='interactive',
        action='store_true',
        default=False
    )

    return parser


def iphttp_run():
    parser = parser_common()

    parser.add_argument(
        '--history',
        action='store_true',
        default=False,
        dest='Keep a history of the requests'
    )
    parser.add_argument(
        '--history-path',
        '-hp',
        dest='history_path',
        help='Path to the history file',
        default=os.path.expanduser("~/.iphttp_history")
    )
    parser.add_argument(
        nargs='+',
        dest='params'
    )

    try:
        uvloop.install()
        asyncio.run(client.execute(parser.parse_args()))
    except KeyboardInterrupt:
        sys.exit(1)


def iphttpd_run():
    parser = parser_common()

    parser.add_argument(
        '--listen',
        '-l',
        dest='httpd_listen_addr',
        default='127.0.0.1:8000',
        help='The listening HTTP server address (host:port)'
    )
    parser.add_argument(
        '--public-port',
        dest='httpd_public_port',
        help='The advertised HTTP port',
        default=80
    )
    parser.add_argument(
        '--serve-aiohttp',
        dest='serve_aiohttp_app',
        help='Serve an aiohttp application from this module',
        default=None
    )

    try:
        uvloop.install()
        asyncio.run(server.start(parser.parse_args()))
    except KeyboardInterrupt:
        pass
