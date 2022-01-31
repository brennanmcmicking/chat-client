import socket
import select
import threading
from time import sleep

port = int(input("Enter a port:"))
addr = ("", port)
serv = socket.create_server(addr)
serv.listen()

conns = []


def listen_new_conns():
    while True:
        new_conn = serv.accept()
        print(new_conn)
        if not new_conn in conns:
            conns.append(new_conn)
            new_conn[0].sendall('Hello, World!'.encode('ascii'))


def keep_alive():
    while True:
        for conn in conns:
            # ping each connection in conn, if it times out then close/remove it
            pass
        sleep(1)


new_conn_thread = threading.Thread(target=listen_new_conns, daemon=True)
keep_alive_thread = threading.Thread(target=keep_alive, daemon=True)
new_conn_thread.start()
keep_alive_thread.start()

while True:
    for conn in conns:
        ready = select.select([conn[0]], [], [], 1)
        if ready[0]:
            try:
                data = conn[0].recv(4096)
            except ConnectionResetError:
                data = 'User left'.encode('ascii')
                conns.remove(conn)
            if data:
                for receiver in conns:
                    """
                    if receiver is not conn:
                        receiver[0].sendall(data)
                    """
                    receiver[0].sendall(data)
                print(data)
