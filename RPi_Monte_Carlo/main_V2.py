import socket
import json
import importlib
import threading
import time
import requests
import pprint

SERVER = "192.168.1.102"
MY_IP = "192.168.1.83"
SEGREDO = "estou bem"
CONFIG_OF_EXP = []
SEGREDO = "estou bem"

api_url = "http://"+SERVER+":8001/ConfigFile"
todo = {"id_RP": MY_IP, "segredo": SEGREDO}
response =  requests.post(api_url, json=todo)
CONFIG_OF_EXP = response.json()
print(json.dumps(CONFIG_OF_EXP['config_file'],indent=4))


# penso que isto devia ter um endpoint para o main server chamar quando for necessario 
# inicar a exp e a dar o status ? em vez de spamar o server com requests de 30ms em 30ms 