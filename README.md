InterPlanetary Tunnel Toolkit
=============================

Provides tools to communicate with existing network protocols over
IPFS tunnels (libp2p streams).

- *iphttp*: Command-line iphttp client
- *iphttpd*: iphttp server (can serve *aiohttp* apps or just forward to an
  existing HTTP service)

```sh
pip install .
```

iphttp
======

*iphttp* is the command-line client. Pass the PeerId with the HTTP path:

```sh
iphttp QmQPeNsJPyVWPFDVHb77w8G42Fvo15z4bG2X8D2GhfbSXc/doc.txt
```

Interactive mode: just pass a PeerId and all requests in the CLI
session will be based on that peer.

```sh
iphttp -i QmQPeNsJPyVWPFDVHb77w8G42Fvo15z4bG2X8D2GhfbSXc
```

Commands supported in interactive mode:

- get(path: str, q={}): HTTP GET request on path *path* with query *q*
- post(path: str, data={}, q={}): HTTP POST request on path with post data *data*
  and HTTP query *q* (dict)

```python
get('/')
get('/', q={'arg1': 4})

post('/form', data={'message': 'Form field data'})
```

iphttpd
=======

*iphttpd* allows you to register an IPFS P2P service for an
already running HTTP server, or to serve an HTTP application
from a Python module (only *aiohttp* apps supported right now).

Example 1
---------

Serve **http://localhost:7000** on protocol **/x/ipfs-http/80/1.0**

```sh
iphttpd -l localhost:7080
```

Example 2
---------

Serve **http://localhost:8080** on protocol **/x/ipfs-http/8000/1.0**

```sh
iphttpd --public-port 8000 -l localhost:8080
```

Example 3
---------

Serve an aiohttp application from Python module
**iphttpd_apps.helloworld**:

```sh
iphttpd --serve-aiohttp iphttpd_apps.helloworld
```

Your module should implement the coroutine **create_app(args)** and return
an *aiohttp.web.Application* instance that will be used to run the service
(see the *helloworld* service).

License
=======

**God bless HTTP, and God bless IPFS** license.
