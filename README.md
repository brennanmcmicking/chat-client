# chat-client

A simple chat client written in Python using Tkinter and sockets

## Data format

In general, packets are sent with the first byte denoting message type. Supported message types:

0x01 (from client): client announcing presence to server (hello)

0x01 (from server): acknowledging a client's connection initiation (hello)

0x02 (from client): client broadcast message

0x02 (from server): server broadcast message

0x03 (from client): client terminating connection with server (goodbye)

0x03 (from server): server terminating connection with client (goodbye)

0x04 (from client): keepalive response

0x04 (from server): keepalive request

### Opening A Connection

Client will send:
byte 0: 0x01
byte 1: username length in n bytes
bytes 2 to n + 2: username

Server replies with:
byte 0: 0x01
byte 1: 0x00 for accept, 0x01 for reject (possible that different rejection reasons will be stored in byte 1 hence why 0x00 is the 'accept' message)

### Sending a message

Client will send:
byte 0: 0x02
byte 1: message length in n bytes
byte 2 to n + 2: message contents

Server will send:
byte 0: 0x02
byte 1: message length in n bytes
byte 2 to n + 2: message contents

### Terminating a Connection

Client will send:
byte 0: 0x03

Server will send:
byte 0: 0x03

### Keepalive

The server will automatically terminate connections that stop responding

Server will send:
byte 0: 0x04

Client will reply:
byte 0: 0x04

If client does not reply after a certain amount of time, the server will termiante that client connection (sending a 0x03 packet)