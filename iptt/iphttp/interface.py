import os.path
import traceback

from .request import iphttp_request_path


async def cli_req(ctx, *params):
    pass


async def cli_get(ctx, *params):
    if not ctx.peer_id_current:
        raise ValueError('No peer set')

    path = ctx.peer_id_current

    for param in params:
        path = os.path.join(path, param.lstrip('/'))

    await iphttp_request_path(ctx.client, path)


async def cli_post(ctx, *params, **kwargs):
    if not ctx.peer_id_current:
        raise ValueError('No peer set')

    q = kwargs.pop('q', {})
    path = ctx.peer_id_current
    data = {}

    for param in params:
        if isinstance(param, str):
            path = os.path.join(path, param.lstrip('/'))
        elif isinstance(param, dict):
            data.update(**param)

    try:
        return await iphttp_request_path(ctx.client, path,
                                         data=data,
                                         params=q,
                                         method='POST')
    except Exception:
        traceback.print_exc()
