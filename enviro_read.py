from SerialProcessor import *
from multiprocessing import Process, Queue
from utils import *
from datetime import date
import time
import sys
import json
import ast

ports = list_ports()
print(ports)

today = date.today()
file_name = today.strftime("%m_%d_%Y") + "_0"
file_name = next_log(file_name, '.csv')

sp = SerialProcessor(ports[0], 9600, 'test')
sp.go()

first_run = True
try:
    while sp.is_running:
        line =  str(sp.queue.get())
        if "{" in line:
            try:
                line_dict = ast.literal_eval(line)
                #print(line_dict)
                #dict_to_json(file_name, line_dict)
               
                if first_run:
                    make_csv(file_name, line_dict)
                    first_run = False
                else:
                    straight_to_csv(file_name, line_dict)
            except:
                print("fail")
        else:
            print(line)
        
except KeyboardInterrupt:
    print('Terminated')

sp.quit()
