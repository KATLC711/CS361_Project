import socket
import json

HEADERSIZE = 10

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((socket.gethostname(), 1234))



full_msg = ''
new_msg = True
while True:
    msg = s.recv(16)
    if new_msg:
        print(f"new message length: {msg[:HEADERSIZE]}")
        msglen = int(msg[:HEADERSIZE])
        new_msg = False


    full_msg += msg.decode("utf-8")

    if len(full_msg) - HEADERSIZE == msglen:
        print("full msg received")

        d = json.loads(full_msg[HEADERSIZE:])
        print(d)

        new_msg = True
        full_msg = ''
        break



print(full_msg)

