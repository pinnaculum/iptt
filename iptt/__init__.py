__version__ = '1.0.2'


def peerid_valid(peerid: str) -> bool:
    from cid import make_cid

    try:
        return make_cid(peerid) is not None
    except Exception:
        return False
