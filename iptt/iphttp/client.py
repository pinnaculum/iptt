import asyncio
import attr
import functools
import sys
import traceback
import os.path
import ssl

from aioipfs import AsyncIPFS
from iptt import peerid_valid

from ptpython import embed

from ..cli import configure as cli_configure
from .interface import cli_get
from .interface import cli_post
from .request import iphttp_request_path


async def iphttp_main(client: AsyncIPFS, args):
    req_peerid: str = None
    path: str = ''

    try:
        peer_id = (await client.core.id())['ID']
        assert peer_id
    except Exception:
        print(f'Cannot connect to the kubo RPC API: {args.maddr}',
              file=sys.stderr)
        sys.exit(1)

    for raw in args.params:
        for param in raw.split('/'):
            pclean = param.rstrip('/')

            if peerid_valid(pclean) and not path:
                req_peerid = pclean
                path = os.path.join(path, req_peerid)
            else:
                path = os.path.join(path, param)

    try:
        ssl_context = None
        if args.ca_cert:
            ssl_context = ssl.create_default_context(
                purpose=ssl.Purpose.CLIENT_AUTH,
                cafile=args.ca_cert
            )

        assert path
        response = await iphttp_request_path(client, path,
                                             ssl_context=ssl_context,
                                             ssl=args.ssl)
    except AssertionError:
        sys.exit(2)
    except Exception:
        traceback.print_exc()
        raise

    if not response:
        print(f'Empty reply from: {peer_id}')
        sys.exit(2)


def wrap(coro, *args, **kw):
    asyncio.ensure_future(coro(*args, **kw))


@attr.s(auto_attribs=True)
class Context:
    # Current PeerId
    peer_id_current: str = None

    # Params
    params: list = []

    # Client
    client: AsyncIPFS = None


async def execute(args):
    ctx = Context(params=args.params)

    if args.interactive:
        # Interactive mode
        try:
            if len(args.params) > 0 and peerid_valid(args.params[0]):
                ctx.peer_id_current = args.params[0]

            clocals = locals()
            clocals.update({
                'get': functools.partial(wrap, cli_get, ctx),
                'post': functools.partial(wrap, cli_post, ctx)
            })

            async with AsyncIPFS(maddr=args.maddr) as client:
                ctx.client = client

                await embed(
                    globals={},
                    locals=clocals,
                    return_asyncio_coroutine=True,
                    patch_stdout=True,
                    configure=cli_configure,
                    history_filename=args.history_path
                )
        except EOFError:
            pass
        except Exception:
            raise
    else:
        # Non-interactive mode

        async with AsyncIPFS(maddr=args.maddr) as client:
            await iphttp_main(client, args)
