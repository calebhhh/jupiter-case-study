import logging

import azure.functions as func


# Boarding Pass Generator

import time
import os
import json
import random
import string
import pickle


def get_boarding_passcode():
    return ''.join(random.choice(string.ascii_uppercase)for i in range(6))

def get_gate_number():
    key = ''
    key = ''.join(random.choice(string.ascii_uppercase)for i in range(2))
    key += key.join(random.choice(string.digits))
    return key

start_time = time.time()

to_send_message_cnt = 5000
bytes_per_message = 256

def generate(length=to_send_message_cnt) -> list:
    boardingpassnumbers=[]
    for i in range(length):
        boardingpassnumbers.append(get_boarding_passcode())

    return boardingpassnumbers


#

import time
import os, uuid
import json
import random
import string
import pickle
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient, __version__
from datetime import datetime
# import boardingPassGen

# from azure.eventhub import EventHubProducerClient, EventData
# Endpoint=sb://hub10001.servicebus.windows.net/;SharedAccessKeyName=publish;SharedAccessKey=lkdv/O87CQi5SvZVfhvb1AUXs94byHbVWyrKlVvhqqM=;EntityPath=hub1
# Endpoint=sb://airportoperationssensor.servicebus.windows.net/;SharedAccessKeyName=publish;SharedAccessKey=ThtuhomNvzUFqBHzahyZuWmn1Fs8xKcIIDV2pVtfDVA=;EntityPath=boardingpass
# Endpoint=sb://demoeventhubforairportevents.servicebus.windows.net/;SharedAccessKeyName=key1;SharedAccessKey=6iDP9b4B9bW93swcFFOxmfxVa+gmQ4xWzQTosqoDPCc=;EntityPath=hub1
# CONNECTION_STR = 'Endpoint=sb://hub10001.servicebus.windows.net/;SharedAccessKeyName=publish;SharedAccessKey=lkdv/O87CQi5SvZVfhvb1AUXs94byHbVWyrKlVvhqqM='
# EVENTHUB_NAME = 'hub1'


blob_connection_string='DefaultEndpointsProtocol=https;AccountName=stadlsdevjupitereus01;AccountKey=exJbSnZIcb/q7ncBLJi3oSHR7EhUHmC9lyLf4P6dCoxEoL/SNxiv7SUgGfKIm/GYHXZi0Krz3HzEvL8rNHYMZg==;EndpointSuffix=core.windows.net'
blob_service_client = BlobServiceClient.from_connection_string(blob_connection_string)
container_name = 'checkin-dryrun'


def get_boarding_passcode():
    return ''.join(random.choice(string.ascii_uppercase)for i in range(12))

def get_gate_number():
    key = ''
    key = ''.join(random.choice(string.ascii_uppercase)for i in range(2))
    key += key.join(random.choice(string.digits))
    return key

start_time = time.time()

# producer = EventHubProducerClient.from_connection_string(
#     conn_str=CONNECTION_STR,
#     eventhub_name=EVENTHUB_NAME
# )

terminals=['1','1A','1B','2','3','4','5','5T']
# sleep_intervals=[1,2,3,4,5,6,7,8,9,10]
# to_send_message_cnt = 5

def runCheckIn(length):
    boardingpass_list = generate(length)
    terminals=['1','1A','1B','2','3','4','5','5T']
    for i in range(length):
        # event_data_batch = producer.create_batch()
        # for batch in range(to_send_message_cnt):
            json_obj={"GateNumber":get_gate_number(), "BoardingPassNumber":boardingpass_list[i], "Terminal":random.choice(terminals),"EventTime":datetime.now()}
            data=json.dumps(json_obj, default=str)
            local_file_name = "/dev-01/" + str(uuid.uuid4()) + ".json"
            blob_client = blob_service_client.get_blob_client(container=container_name, blob=local_file_name)
            blob_client.upload_blob(data)
            # time.sleep(random.choice([.2,.3,.4]))
    print("Sent {} messages in {} seconds.".format(i,time.time() - start_time))

## MAIN FUNCTION

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    name = int(req.params.get('length'))
    if not name:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            name = req_body.get('length')

    if name:
        runCheckIn(length=name)
        return func.HttpResponse(f"This HTTP triggered function executed successfully. {name} boarding passes were issued")
    else:
        return func.HttpResponse(
             "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
             status_code=200
        )
