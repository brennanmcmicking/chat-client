import threading


class Listener(threading.Thread):
    def __init__(self, conn, add_chat):
        self.conn = conn
        self.add_chat = add_chat
        super(Listener, self).__init__()

    def run(self):
        while True:
            data = self.conn.recv(4096)
            if data:
                msg = data.decode('ascii')
                print(msg)
                self.add_chat(msg)
