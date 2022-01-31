from email import message
import threading
import queue


class Sender(threading.Thread):
    def __init__(self, conn, message_queue: queue.PriorityQueue):
        self.conn = conn
        self.message_queue = message_queue
        super(Sender, self).__init__()

    def send(self, message):
        self.conn.send(message.encode('ascii'))
