import socket
import json
import time

HOST = "172.28.120.37"  # Standard loopback interface address (localhost)
HOST = "192.168.43.68"
PORT = 65432  # Port to listen on (non-privileged ports are > 1023)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

while True:
    s.send('go'.encode("utf-8"))
    data = s.recv(1024).decode("utf-8")
    data = json.loads(data)

    print(f"Received {data}")
    time.sleep(1)