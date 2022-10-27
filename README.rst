InterPlanetary Tunnel Toolkit
=============================

.. image:: https://gitlab.com/galacteek/iptt/iptt/-/raw/master/media/img/iptt-256.png
    :width: 128
    :height: 128

Provides tools to communicate with existing network protocols over
IPFS tunnels (libp2p streams).

- *iphttp*: Command-line iphttp client (supports SSL)
- *iphttpd*: iphttp server (can serve *aiohttp* apps or just forward to an
  existing HTTP service)

.. code-block:: bash

    pip install -U iptt

Checkout the documentation `here <https://iptt.readthedocs.io/en/latest>`_.

iphttp
======

*iphttp* is the command-line client. To make a simple GET request,
pass the PeerId with the HTTP path. Use *--ssl* (or *-s*) to use
SSL encryption:

.. code-block:: bash

    iphttp QmQPeNsJPyVWPFDVHb77w8G42Fvo15z4bG2X8D2GhfbSXc/doc.txt

    iphttp -s QmQPeNsJPyVWPFDVHb77w8G42Fvo15z4bG2X8D2GhfbSXc/doc.txt

Use *--maddr* to pass the RPC API multiaddr_ of your kubo_ node (the
default multiaddr is */ip4/127.0.0.1/tcp/5001*) :

.. code-block:: bash

    iphttp --maddr /dns4/localhost/tcp/5010 \
        QmQPeNsJPyVWPFDVHb77w8G42Fvo15z4bG2X8D2GhfbSXc/summary.html

Interactive mode: just pass a PeerId and all requests in the CLI
session will be based on that peer.

.. code-block:: bash

    iphttp -i QmQPeNsJPyVWPFDVHb77w8G42Fvo15z4bG2X8D2GhfbSXc

The following commands are supported in interactive mode:

- get(path: str, q={}, h={}): HTTP GET request on path *path* with query *q*
  and HTTP headers *h* (dict)

- post(path: str, q={}, data={}, h={}): HTTP POST request on path with post data *data*, HTTP query *q* (dict) and HTTP headers *h* (dict)

.. code-block:: python

    get('/')
    get('/', q={'arg1': 4})
    get('/', h={'X-Important-Header': 'some-value'})

    post('/form', q={'arg1': 2}, data={'message': 'Form field data'})
    post('/form', data={'message': 'Form field data'})

iphttpd
=======

*iphttpd* allows you to register an IPFS P2P service for an
already running HTTP server, and can also serve an HTTP application
from a Python module (only *aiohttp* apps are supported right now).

Example 1
---------

Serve **http://localhost:7000** for the P2P protocol **/x/ipfs-http/80/1.0**

.. code-block:: bash

    iphttpd -l localhost:80:7080

Example 2
---------

Serve **http://localhost:8080** for the P2P protocol **/x/ipfs-http/8000/1.0**

.. code-block:: bash

    iphttpd -l localhost:8000:8080

Example 3
---------

Serve an aiohttp application from Python module
**iphttpd_apps.helloworld**:

.. code-block:: bash

    iphttpd --serve-aiohttp iphttpd_apps.helloworld

Your module should implement the coroutine **create_app(args)** and return
an *aiohttp.web.Application* instance that will be used to run the service
(see the helloworld_ service).

Example 4
---------

Serve an application with SSL on port 8200:

.. code-block:: bash

    iphttpd -s --serve-aiohttp iphttpd_apps.helloworld --cert iphttpd.io.pem --key iphttpd.io-key.pem -l localhost:443:8200

Projects using iptt
===================

- galacteek_

License
=======

**God bless HTTP, and God bless IPFS** license.

.. _galacteek: https://gitlab.com/galacteek/galacteek
.. _helloworld: https://gitlab.com/galacteek/iptt/iptt/-/blob/master/iphttpd_apps/helloworld.py
.. _kubo: https://github.com/ipfs/kubo
.. _multiaddr: https://multiformats.io/multiaddr
