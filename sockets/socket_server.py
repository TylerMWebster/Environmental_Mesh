import socket
import random
import json
from threading import Thread

def run_socket(HOST , PORT):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT))
    s.listen()
    while True:
        conn, addr = s.accept()
        print(f"Connected by {addr}")
        while True: 
            recieved = conn.recv(1024).decode("utf-8")
            if not recieved:
                print('Client disconnected')
                break
            if recieved in ('go'):
                conn.sendall(bytes(generate_data(4), encoding="utf-8"))
        conn.close()
            

def generate_data(length):
    data = {}
    for i in range(0, length):
        data[f'address{i}'] =  round(random.uniform(30.5, 95.5), 2)
    data = json.dumps(data)
    return data


#print(json.loads(generate_data(4)))

#HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
#HOST = "172.28.120.37"
HOST = "192.168.43.68"
PORT = 65432  # Port to listen on (non-privileged ports are > 1023)

socket_thread = Thread(target=run_socket, args=(HOST, PORT))
socket_thread.start()
print("Server Running")