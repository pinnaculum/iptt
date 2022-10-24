import json
import re
import sys
import traceback
from yarl import URL

from aioipfs import AsyncIPFS
from aioipfs.helpers import peerid_base36

from .request import request as iphttp_request


async def iphttp_main(client: AsyncIPFS, args):
    try:
        peer_id = (await client.core.id())['ID']
        assert peer_id
    except Exception:
        print(f'Cannot connect to kubo node: {args.maddr}',
              file=sys.stderr)
        sys.exit(1)

    for url in args.urlparts:
        try:
            parts = url.strip().split('/')
            peerid = parts[0]

            if len(parts) > 1:
                path = '/' + parts[1]
            else:
                path = '/'
        except Exception as err:
            print(err)
            continue

        if re.search(r'[A-Z]+', peerid):
            # base58 => base36
            peerid = peerid_base36(peerid)
            if not peerid:
                print(f'Invalid peerid: {peerid}')
                sys.exit(2)

        url = URL.build(
            host=peerid,
            scheme='ipfs+http',
            path=path
        )

        try:
            data, ctype = await iphttp_request(
                client,
                str(url)
            )
        except Exception:
            traceback.print_exc()
            sys.exit(1)

        if not data:
            print(f'Empty reply from: {peerid}')
            sys.exit(2)

        if ctype == 'application/json':
            obj = json.loads(data.getvalue())

            print(json.dumps(obj, indent=4))
        else:
            print(data.getvalue().decode())


async def execute(args):
    async with AsyncIPFS(maddr=args.maddr) as client:
        await iphttp_main(client, args)
