from threading import Thread
from http.server import BaseHTTPRequestHandler, HTTPServer
from serial_processor import *
from multiprocessing import Process, Queue
from utils import *
from datetime import date
import time
import sys
import json
import ast
import numpy as np

# Setup sensor vars
FAST_RATE = '/tim/01000'
SLOW_RATE = '/tim/01000'
RESET_COMMAND = '/rst/99999'
END_OF_STARTUP = 30
TIMEOUT = 120
ACTUAL_SENSORS = 4
num_sensors = 0
all_found = False
first_run = True
set_slow = False
start_time = time.time()

# Setup file
today = date.today()
file_name = today.strftime("%m_%d_%Y") + "_0"
file_name = next_log(file_name, '.csv')

# Setup HTTP server
#HOST= "172.28.120.37"
HOST = "192.168.43.68"
PORT = 42069
data_json = None
class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/json")
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(bytes(f"{data_json}", "utf-8"))

def run_http(hostName, serverPort):
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except:
        pass

    webServer.server_close()
    print("Server stopped.")

http_thread = Thread(target=run_http, args=(HOST, PORT))
http_thread.start()
print("Server Running")


# Setup serial ports
ports = list_ports()
print(ports)
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
    http_thread.join()
    print('Terminated')

sp.quit()
