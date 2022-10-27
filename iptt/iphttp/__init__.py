class IpfsHttpError(Exception):
    pass


class IpfsHttpServerError(Exception):
    def __init__(self, status_code: int):
        self.http_status = status_code
