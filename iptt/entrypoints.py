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
        '--maddr',
        '-m',
        dest='maddr',
        default='/ip4/127.0.0.1/tcp/5001',
        help="kubo node's RPC API multiaddr"
    )
    parser.add_argument(
        '-i',
        dest='interactive',
        action='store_true',
        default=False
    )
    parser.add_argument(
        '-s',
        '--ssl',
        dest='ssl',
        action='store_true',
        default=False,
        help='Use SSL encryption'
    )
    parser.add_argument(
        '--ca-cert',
        dest='ca_cert',
        default='ca.crt',
        help='SSL Certificate authority'
    )

    return parser


def iphttp_run():
    parser = parser_common()

    parser.add_argument(
        '--history',
        action='store_true',
        default=False,
        dest='Keep a history of the requests made in the interactive mode'
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
        dest='params',
        help='iphttp request path. format: PeerId/path'
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
        '--public-port-ssl',
        dest='httpd_public_port_ssl',
        help='The advertised HTTPs port',
        default=443
    )

    parser.add_argument(
        '--serve-aiohttp',
        dest='serve_aiohttp_app',
        help='Serve an aiohttp application from a Python module',
        default=None
    )

    parser.add_argument(
        '--ssl-cert',
        '--cert',
        dest='ssl_cert',
        help='SSL certificate path (PEM)',
        default=None
    )
    parser.add_argument(
        '--ssl-key',
        '--key',
        dest='ssl_key',
        help='SSL key path',
        default=None
    )

    try:
        uvloop.install()
        asyncio.run(server.start(parser.parse_args()))
    except KeyboardInterrupt:
        pass
