import threading

from packet_constants import *


class Listener(threading.Thread):
    def __init__(self, conn, client):
        self.conn = conn
        self.client = client
        self.ready = False
        super(Listener, self).__init__()

    def run(self):
        while True:
            data = self.conn.recv(4096)
            if data:
                if data[0] == NEW_CONNECTION:
                    if data[1] == NEW_CONN_ACCEPT:
                        self.client.ready = True
                        print('received ack from server')
                    else:
                        print(f'failed to log in {data[1]}')
                if data[0] == BROADCAST_MESSAGE:
                    end = int(data[1]) + 2
                    msg = data[2:end].decode('ascii')
                    self.client.add_chat(msg)

                if data[0] == TERMINATE_CONNECTION:
                    pass

                if data[0] == KEEPALIVE_COMM:
                    print(f'received KEEPALIVE')
                    self.conn.sendall(bytes([KEEPALIVE_COMM]))
