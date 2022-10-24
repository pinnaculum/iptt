import asyncio
import traceback

from io import BytesIO
from typing import Union

import aiohttp
from aiohttp.client_exceptions import ServerDisconnectedError
from aiohttp.web_exceptions import HTTPOk
from yarl import URL

from aioipfs import AsyncIPFS
from aioipfs.helpers import peerid_base58

from . import IpfsHttpError
from . import IpfsHttpServerError

try:
    from PyQt5.QtCore import QIODevice
except ImportError:
    pass


async def request(client: AsyncIPFS,
                  url: Union[str, URL],
                  buffer: BytesIO = None,
                  chunkSize: int = 65535,
                  allowedMethods: list = ['GET', 'POST'],
                  method='GET') -> tuple:
    """
    Run a request

    :param str url: URL
    :param BytesIO buffer: Optional: buffer to write the response to
    :param str method: HTTP method (GET, POST)
    :rtype: tuple (fd, mimetype)
    """

    rUrl = url if isinstance(url, URL) else URL(url)
    hostb36 = rUrl.host
    port = rUrl.port if rUrl.port else 80

    if not buffer:
        buffer = BytesIO()

    if method not in allowedMethods:
        raise IpfsHttpError(f'Unsupported http method: {method}')

    try:
        # base36/base32 => cidv0 (base58) (cached conversion)
        peerId = peerid_base58(hostb36)
        assert peerId is not None
    except Exception:
        traceback.print_exc()
        raise IpfsHttpError(f'Invalid peerid: {rUrl.host}')

    if rUrl.scheme == 'ipfs+http':
        protoName = 'ipfs-http'
        port = rUrl.port if rUrl.port else 80
    elif rUrl.scheme == 'ipfs+https':
        protoName = 'ipfs-https'
        port = rUrl.port if rUrl.port else 443
    else:
        raise IpfsHttpError('Invalid scheme')

    # ipfs-http P2P endpoint address
    p2pEndpoint = f'/p2p/{peerId}/x/{protoName}/{port}/1.0'

    try:
        # Tunnel
        async with client.p2p.dial_endpoint(p2pEndpoint,
                                            allow_loopback=True) as dial:
            if dial.failed:
                raise Exception(f'Dialing {peerId} failed')

            url = dial.httpUrl(
                rUrl.path,
                query=rUrl.query,
                fragment=rUrl.fragment
            )

            async with aiohttp.ClientSession() as sess:
                async with sess.get(url) as resp:
                    if resp.status != HTTPOk.status_code:
                        raise IpfsHttpServerError(resp.status)

                    ctyper = resp.headers.get('Content-Type',
                                              'application/octet-stream')

                    if isinstance(buffer, BytesIO):
                        async for chunk in resp.content.iter_chunked(
                                chunkSize):
                            buffer.write(chunk)

                            await asyncio.sleep(0)
                    else:
                        # Assume QIODevice (used from galacteek)
                        buffer.open(QIODevice.WriteOnly)

                        async for chunk in resp.content.iter_chunked(
                                chunkSize):
                            buffer.write(chunk)

                            await asyncio.sleep(0)

                        buffer.close()

            ctype = ctyper.split(';')[0]

            return buffer, ctype
    except ServerDisconnectedError as sderr:
        raise sderr
    except IpfsHttpServerError as herr:
        raise herr
    except Exception as err:
        raise err