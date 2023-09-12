import socket

from packet_constants import *

from tkinter import *
from tkinter import ttk
from tkinter import StringVar

from client_sender import Sender
from client_listener import Listener


class Manager():
    def __init__(self):
        self.conn = None
        self.ready = False

    def connect(self):
        print(f"connecting with ip: {hostname.get()}, port: {port.get()}")
        self.conn = socket.create_connection((hostname.get(), int(port.get())))
        self.conn.send(
            bytes([NEW_CONNECTION, len(username.get())]) + username.get().encode())
        listener = Listener(self.conn, self)
        listener.daemon = True
        listener.start()
        connector.destroy()

    def add_chat(self, msg: str):
        print(f'add_chat called, message: {msg}')
        chat_history.set(chat_history.get() + f'\n{msg}')

    def send_chat(self):
        if self.ready:
            self.conn.send(bytes([BROADCAST_MESSAGE, len(chat.get())]) +
                           chat.get().encode('ascii'))
            chat.set('')  # clear sendbox after sending a message
        else:
            print('not ready')


manager = Manager()

root = Tk()
root.geometry('800x600')

hostname = StringVar()  # input("Enter the IP:")
port = StringVar()  # int(input("Enter the port:"))
username = StringVar()  # input("Enter a username:")

chat_history = StringVar()
chat = StringVar()

connector = Toplevel(root, name='connect', padx=10, pady=10)
ttk.Label(connector, text="IP: ").grid(column=0, row=0)
ttk.Entry(connector, textvariable=hostname).grid(column=1, row=0)
ttk.Label(connector, text="Port: ").grid(column=0, row=1)
ttk.Entry(connector, textvariable=port).grid(column=1, row=1)
ttk.Label(connector, text="Username: ").grid(column=0, row=2)
ttk.Entry(connector, textvariable=username).grid(column=1, row=2)
ttk.Button(connector, command=manager.connect,
           text="Connect").grid(column=0, row=3)

main = ttk.Frame(root, padding=10)
main.grid()
ttk.Label(main, textvariable=chat_history).grid(column=0, row=0)
ttk.Entry(main, textvariable=chat).grid(column=0, row=1)
ttk.Button(main, command=manager.send_chat, text="Send").grid(column=1, row=1)

connector.attributes('-topmost', True)
root.mainloop()
