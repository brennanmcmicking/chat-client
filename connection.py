from email.headerregistry import UniqueSingleAddressHeader


class Connection:
    def __init__(self, ip, name, conn):
        self.ip = ip
        self.name = name
        self.conn = conn
