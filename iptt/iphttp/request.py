import asyncio
import json
import re
import traceback

from io import BytesIO
from typing import Union

import aiohttp
from aiohttp.client_exceptions import ServerDisconnectedError
from aiohttp.web_exceptions import HTTPOk
from yarl import URL

from aioipfs import AsyncIPFS
from aioipfs.helpers import peerid_base58
from aioipfs.helpers import peerid_base36

import async_timeout
import attr

from . import IpfsHttpError
from . import IpfsHttpServerError

try:
    # galacteek passes a QIODevice
    from PyQt5.QtCore import QIODevice
except ImportError:
    pass


@attr.s(auto_attribs=True)
class IpHttpResponse:
    data: BytesIO
    content_type: str = None


allowedMethods: list = ['GET',
                        'POST',
                        'DELETE',
                        'PATCH']


async def iphttp_request(client: AsyncIPFS,
                         url: Union[str, URL],
                         buffer: BytesIO = None,
                         data: dict = {},
                         params: dict = {},
                         headers: dict = {},
                         chunkSize: int = 65535,
                         method='GET') -> IpHttpResponse:
    """
    Run a request

    :param str url: URL
    :param BytesIO buffer: Optional: buffer to write the response to
    :param str method: HTTP method (GET, POST)
    :param dict data: POST data
    :param dict params: query
    :param dict headers: HTTP headers to pass
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
        # base36/base32 => base58
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

        with async_timeout.timeout(60):
            async with client.p2p.dial_endpoint(p2pEndpoint,
                                                allow_loopback=True) as dial:
                if dial.failed:
                    raise Exception(f'Dialing {peerId} failed')

                url = dial.httpUrl(
                    rUrl.path,
                    query=rUrl.query,
                    fragment=rUrl.fragment
                )

                async with aiohttp.ClientSession(headers=headers) as sess:
                    async with sess.request(method,
                                            url,
                                            params=params,
                                            data=data) as resp:
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

                return IpHttpResponse(
                    data=buffer,
                    content_type=ctype
                )
    except ServerDisconnectedError as sderr:
        raise sderr
    except IpfsHttpServerError as herr:
        raise herr
    except Exception as err:
        raise err


async def iphttp_request_path(client, path: str,
                              data: dict = {},
                              params: dict = {},
                              headers: dict = {},
                              method: str = 'GET'):
    try:
        parts = path.strip().split('/')
        peerid = parts[0]

        if len(parts) > 1:
            path = '/' + parts[1]
        else:
            path = '/'
    except Exception:
        return None, None

    if re.search(r'[A-Z]+', peerid):
        # base58 => base36
        peerid = peerid_base36(peerid)
        if not peerid:
            print(f'Invalid peerid: {peerid}')
            return None, None

    try:
        assert peerid
        response = await iphttp_request(
            client,
            URL.build(
                host=peerid,
                scheme='ipfs+http',
                path=path
            ),
            method=method,
            data=data,
            params=params,
            headers=headers
        )
    except Exception:
        traceback.print_exc()
        return None

    if not response.data:
        print(f'Empty reply from: {peerid}')
        return None

    if response.content_type == 'application/json':
        obj = json.loads(response.data.getvalue())

        print(json.dumps(obj, indent=4))
    else:
        print(response.data.getvalue().decode())

    return response
