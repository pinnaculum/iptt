import os.path

from . import IpfsHttpServerError
from .request import iphttp_request_path


async def cli_get(ctx, *params, q={}, **kwargs):
    if not ctx.peer_id_current:
        raise ValueError('No peer set')

    q = kwargs.pop('q', {})
    headers = kwargs.pop('h', {})
    path = ctx.peer_id_current

    for param in params:
        path = os.path.join(path, param.lstrip('/'))

    try:
        await iphttp_request_path(ctx.client,
                                  path,
                                  headers=headers,
                                  params=q)
    except IpfsHttpServerError:
        raise


async def cli_post(ctx, *params, **kwargs):
    if not ctx.peer_id_current:
        raise ValueError('No peer set')

    q = kwargs.pop('q', {})
    headers = kwargs.pop('h', {})
    user_data = kwargs.pop('data', {})
    path = ctx.peer_id_current
    data = {}

    for param in params:
        if isinstance(param, str):
            path = os.path.join(path, param.lstrip('/'))

    if isinstance(user_data, dict):
        data.update(user_data)

    try:
        return await iphttp_request_path(ctx.client,
                                         path,
                                         headers=headers,
                                         params=q,
                                         data=data,
                                         method='POST')
    except IpfsHttpServerError:
        raise
