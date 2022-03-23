from threading import TIMEOUT_MAX
from serial_processor import *
from multiprocessing import Process, Queue
from utils import *
from datetime import date
import time
import sys
import json
import ast
import numpy as np
import socket
import random
import json
from threading import Thread


FAST_RATE = '/tim/01000'
SLOW_RATE = '/tim/01000'
RESET_COMMAND = '/rst/99999'
END_OF_STARTUP = 30
TIMEOUT = 120
ACTUAL_SENSORS = 2
num_sensors = 0
all_found = False

data_json = {}

first_run = True
set_slow = False
start_time = time.time()

ports = list_ports()
print(ports)

today = date.today()
file_name = today.strftime("%m_%d_%Y") + "_0"
file_name = next_log(file_name, '.csv')

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
                conn.sendall(bytes(data_json, encoding="utf-8"))
        conn.close()

HOST = "192.168.43.68"
PORT = 65432  # Port to listen on (non-privileged ports are > 1023)

socket_thread = Thread(target=run_socket, args=(HOST, PORT))
socket_thread.start()
print("Server Running")

sp = SerialProcessor(ports[0], 9600, 'test')
sp.go()
try:
    print('Setting fast rate')
    sp.sendMessage(FAST_RATE)
except:
    print('Could not set polling rate')


try:
    while sp.is_running:
        line =  str(sp.queue.get())
        if "{" in line:
            try:
                line_dict = ast.literal_eval(line)
                try:
                    data_json = json.dumps(line_dict)
                except:
                    print('Failed to convert data to JSON format')
                if first_run:
                    make_csv(file_name, line_dict)
                    first_run = False
                else:
                    straight_to_csv(file_name, line_dict)
            except:
                print("fail")

        elif "network: " in line:
            num_sensors = int(line[-2] + line[-1])
            if num_sensors != ACTUAL_SENSORS and not all_found:
                if (time.time() - start_time) < TIMEOUT:
                    print(f'{num_sensors} found out of {ACTUAL_SENSORS} expected.')
                    print("Reseting Sensors")
                    sp.sendMessage(RESET_COMMAND)
                    time.sleep(2)
                else: 
                    print('System discovery timeout reached')
                    sp.sendMessage(RESET_COMMAND)
                    time.sleep(2)
                    all_found = True
            else:
                all_found = True
                
        else:
            print(line)
        if((time.time() - start_time) >= END_OF_STARTUP and not set_slow and all_found):
            print('Setting slow rate')
            try:
                sp.sendMessage(SLOW_RATE)
                set_slow = True
            except: 
                print('Could not set polling rate')
        
except KeyboardInterrupt:
    socket_thread.join()
    print('Terminated')

sp.quit()
