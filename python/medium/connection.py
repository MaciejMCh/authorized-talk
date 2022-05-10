class Connection:
    pass


class SslConnection(Connection):
    def __init__(self, url: str):
        self.url = url
