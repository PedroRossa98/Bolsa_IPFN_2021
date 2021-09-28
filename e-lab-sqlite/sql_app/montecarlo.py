from datetime import datetime
import random
import math
import time

from pydantic import BaseModel

import crud

# =========================== Monte Carlo =================================

FORMAT = 'utf-8'
NAME_EXP = "Monte Carlo"
serial_port = None
size = 10
n_points = 20
first = 1
i = 0
total_in = 0



def receive_data_from_exp():
    global serial_port
    global first 
    global i 
    global total_in
    
    if first == 1:
        first = 0
        return "DATA_START"
    if int(i) > int(n_points):
        time.sleep(0.01)
        print("Pi: %lf"%(float(total_in)*4/float(n_points)))
        return "DATA_END"
    time.sleep(0.01)
    
    x = random.random()*float(size)
    y = random.random()*float(size)
    if math.sqrt(x*x+y*y) <=int(size):
        c_in = 1
        total_in = total_in + 1
    else:
        c_in = 0
    pic_message = {
      "Sample_number": i,
      "eX": x,
      "eY": y,
      "circ": c_in
      }
    print (i)
    i=i+1
    return pic_message
    
    
# JSON = '{"experiment_name": "Cavidade", "config_experiment": {"R":'+ String(R)+', "Iteration":'+String(Iteration)+'}}'

class ExperimentModel(BaseModel):
    R: str
    Iteration: str

class ConfigExperimentModel(BaseModel):
    experiment_name: str
    config_experiment: ExperimentModel


def do_config(config_json) :
    global serial_port

    global size
    global n_points
    

    print(config_json)
    size = config_json["config_experiment"]["R"]
    n_points = config_json["config_experiment"]["Iteration"]

    print("Size :")
    print(size)
    print("\n")
    print("Número de pontos :")
    print(n_points)


    return  config_json,True

def configure_start_experiment(user_json):
    do_config(user_json)
    return ''


def config_experiment_data(user: ConfigExperimentModel):
    global i
    global first

    i = 0
    first = 1

    print(user)
    user_json = user.dict()
    print(type(user))
    print(type(user_json))
    configure_start_experiment(user_json)
    return {'JSON Enviado': user_json , 'result': 'OK!'}


def resultpoint_data(db):
    global i

    send_data = {}
    exp_data = receive_data_from_exp()

    # print('receive_data_from_exp : ', str(exp_data))
    if exp_data == "DATA_START":
        send_data =  {
          "msg_id": i,
          "timestamp": time.time_ns(),
          "status": "Experiment Started",
          "Data": exp_data
        }
    elif exp_data == "DATA_END":
        send_data = {
          "msg_id": i,
          "timestamp": time.time_ns(),
          "status": "Experiment Ended",
          "Data": exp_data
          }
    else:
        send_data = {
          "msg_id": i,
          "timestamp": time.time_ns(),
          "status": "running",
          "Data": exp_data
        }

    crud.add_temperature(db, send_data)

    print('Send Data : ', send_data,'\n',datetime.now())

    return send_data


def resultlist_data(db, limit: int = 10):
    return crud.get_temperature_list(db, limit)