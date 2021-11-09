import socket
import json

keyword = "Falcons"

HEADERSIZE = 10

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((socket.gethostname(), 1234))

s.send(keyword.encode("utf-8"))

full_msg = ''
new_msg = True
while True:
    msg = s.recv(16)
    if new_msg:
        msglen = int(msg[:HEADERSIZE])
        new_msg = False

    full_msg += msg.decode("utf-8")

    if len(full_msg) - HEADERSIZE == msglen:
        d = json.loads(full_msg[HEADERSIZE:])
        new_msg = True
        full_msg = ''
        break


print(d)