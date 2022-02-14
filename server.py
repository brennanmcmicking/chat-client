import datetime
import socket
import select
import threading
from time import sleep
from packet_constants import *


class ConnectionExistsError(Exception):
    def __init__(self):
        pass


class NewConnectionListener(threading.Thread):
    def __init__(self, server):
        self.server = server
        super(NewConnectionListener, self).__init__()
        self.setDaemon(True)

    def run(self):
        while True:
            new_conn = self.server.serv.accept()
            ready = select.select([new_conn[0]], [], [], 1)
            if ready:
                packet = new_conn[0].recv(4096)
                print(f'new connection heard. first packet: {packet}')
                if packet is not None:
                    if packet[0] == NEW_CONNECTION:
                        self.server.handle_new_connection(packet, new_conn)
            else:
                self.server.handle_disconnect(packet, new_conn)


class Server:
    def __init__(self):
        self.port = int(input("Enter a port:"))
        self.addr = ("", self.port)
        self.serv = socket.create_server(self.addr)

        self.conns = []

        self.serv.listen()

    def handle_new_connection(self, packet, new_conn):
        n = packet[1]
        username = packet[2:n + 2].decode('ascii')
        for uname, conn, lastkeepalive in self.conns:
            if username == uname:
                new_conn[0].sendall(
                    bytes([NEW_CONNECTION, NEW_CONN_BAD_USERNAME]))
                return

        self.conns.append([username, new_conn, datetime.datetime.now()])
        new_conn[0].sendall(bytes([NEW_CONNECTION, NEW_CONN_ACCEPT]))

    def handle_packet(self, packet, username, conn):
        if packet[0] == NEW_CONNECTION:
            print(
                "Fatal error: already-initialized connection sent a NEW_CONNECTION packet")
            raise ConnectionExistsError
        if packet[0] == BROADCAST_MESSAGE:
            end = int(packet[1]) + 2
            msg = packet[2:end].decode('ascii')
            message = f'{username}: {msg}'
            for uname, conn, lastseen in self.conns:
                conn[0].sendall(
                    bytes([BROADCAST_MESSAGE, len(message)]) + message.encode('ascii'))

        if packet[0] == TERMINATE_CONNECTION:
            self.handle_disconnect(packet, conn)

    def handle_disconnect(self, packet, dead_conn):
        for uname, conn, lastseen in self.conns:
            if conn == dead_conn:
                self.conns.remove((uname, conn, lastseen))
                dead_conn[0].shutdown()
                dead_conn[0].close()

    def start(self):
        while True:
            for uname, conn, lastseen in self.conns:
                ready = select.select([conn[0]], [], [], 1)
                if ready[0]:
                    try:
                        data = conn[0].recv(4096)
                    except ConnectionResetError:
                        self.handle_disconnect(None, conn)
                    if data:
                        loc = self.conns.index([uname, conn, lastseen])
                        self.conns[loc][2] = datetime.datetime.now()
                        self.handle_packet(data, uname, conn)


class ServerKeepAlive(threading.Thread):
    def __init__(self, server: Server):
        self.server: Server = server
        super(ServerKeepAlive, self).__init__()
        self.setDaemon(True)

    def run(self):
        while True:
            for username, conn, lastkeepalive in self.server.conns:
                if datetime.datetime.now() - lastkeepalive > datetime.timedelta(seconds=120):
                    self.server.handle_disconnect(None, conn)

                # ping each connection in conn
                conn[0].sendall(bytes([KEEPALIVE_COMM]))

            sleep(60)


server = Server()
new_conn_thread = NewConnectionListener(server)
keep_alive_thread = ServerKeepAlive(server)
new_conn_thread.start()
keep_alive_thread.start()

server.start()
