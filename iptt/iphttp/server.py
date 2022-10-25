import asyncio
import ipaddress
import traceback
import importlib

from aiologger import Logger

from aioipfs import AsyncIPFS
from aioipfs import APIError
from aiohttp import web

from ..cli import embed_cli


log = Logger.with_default_handlers(name='iphttpd')


async def serve_app(args,
                    host: str,
                    port: str,
                    appmod: str):
    try:
        mod = importlib.import_module(appmod)

        app = await mod.create_app(args)
        runner = web.AppRunner(app)

        await runner.setup()

        site = web.TCPSite(runner, host, port)
        await site.start()

        if args.interactive:
            await embed_cli(_locals=locals())
        else:
            while True:
                await asyncio.sleep(5)
    except KeyboardInterrupt:
        raise
    except asyncio.CancelledError:
        pass
    except Exception:
        await log.warning(
            f'Error running app from: {appmod}: {traceback.format_exc()}'
        )

        raise


async def iphttpd(client: AsyncIPFS, args):
    alistening = False
    proto = f'/x/ipfs-http/{args.httpd_public_port}/1.0'

    try:
        host, port = args.httpd_listen_addr.split(':')
        assert host
        assert port
        addr = ipaddress.ip_address(host)
        maddr = f'/ip{addr.version}/{host}/tcp/{port}'
    except AssertionError:
        raise
    except ValueError:
        maddr = f'/dns4/{host}/tcp/{port}'

    try:
        for listener in await client.p2p.listeners():
            if listener['Protocol'] == proto:
                if listener['TargetAddress'] == maddr:
                    # Same protocol with the same TargetAddress: no worries
                    alistening = True

                    await log.info(
                        f'Already listening on multiaddr: {maddr}')
                else:
                    # Same protocol but different TargetAddress: close it
                    await client.p2p.listener_close(proto)

                    await log.debug(
                        f"Closed old listener: {listener['TargetAddress']}"
                    )

        if not alistening:
            await client.p2p.listener_open(proto, maddr)

        await log.info(f'Now listening on multiaddr: {maddr}')

        appmod = args.serve_aiohttp_app
        if appmod is not None:
            try:
                await serve_app(args, host, port, appmod)
            except Exception:
                raise

            # Exited the application: close the listener
            await client.p2p.listener_close(proto)
    except Exception as err:
        await log.warning(f'iphttpd error: {err}')

        traceback.print_exc()
    except APIError as err:
        await log.warning(f'iphttpd IPFS error: {err.message}')

    await log.info('iphttpd exit')


async def start(args):
    async with AsyncIPFS(maddr=args.maddr) as client:
        await iphttpd(client, args)
