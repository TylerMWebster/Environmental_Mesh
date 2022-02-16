from serial_processor import *
from multiprocessing import Process, Queue
from utils import *
from datetime import date
import time
import sys
import json
import ast
import numpy as np

FAST_RATE = 1000
SLOW_RATE = 360000

first_run = True
set_slow = False
start_time = time.time()

ports = list_ports()
print(ports)

today = date.today()
file_name = today.strftime("%m_%d_%Y") + "_0"
file_name = next_log(file_name, '.csv')

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
               
                if first_run:
                    make_csv(file_name, line_dict)
                    first_run = False
                else:
                    straight_to_csv(file_name, line_dict)
            except:
                print("fail")
        else:
            print(line)
        if((time.time() - start_time) >= 15 and not set_slow):
            print('Setting slow rate')
            try:
                sp.sendMessage(SLOW_RATE)
                sp.sendMessage(SLOW_RATE)
                sp.sendMessage(SLOW_RATE)
                set_slow = True
            except: 
                print('Could not set polling rate')
        
except KeyboardInterrupt:
    print('Terminated')

sp.quit()
