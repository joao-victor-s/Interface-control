from paho.mqtt import client as mqtt_client
import json
import logging
import random
import time
from Control_Interface.controlInterface import controlInterface
import datetime
from influxdb import InfluxDBClient
import signal
import sys


host = '192.168.0.113'  
port = 8086         
dbname = 'telegraf'

client_influxdb = InfluxDBClient(host, port, database=dbname)

BROKER = 'broker.hivemq.com' 
PORT = 1883
TOPIC_SUB = "labrei-nhr-sub/#"
TOPIC_PUB = "labrei-nhr-pub"
CLIENT_ID = f'python-mqtt-{random.randint(0, 1000)}'


FIRST_RECONNECT_DELAY = 1 
RECONNECT_RATE = 2
MAX_RECONNECT_COUNT = 12
MAX_RECONNECT_DELAY = 60

FLAG_EXIT = False

interface = controlInterface()

print(interface.getListIp())
interface.newNhr("9410")
interface.newNhr("9430")

NHRs = {  
     "9410" : interface.getNhr9410()[0],
    #  "9430" : interface.getNhr9430()[0], 
}

def on_connect(client, userdata, flags, rc):
    if rc == 0 and client.is_connected():
        print("Connected to MQTT Broker!")
        client.subscribe(TOPIC_SUB)
    else:
        print(f'Failed to connect, return code {rc}')

def write_influxdb(method_name, args, result):
    data = [
        {
            "measurement": "method_call",
            "tags": {
                "method": method_name
            },
            "time": datetime.datetime.utcnow().isoformat(),
            "fields": {
                "arguments": str(args),
                "result": str(result)
            }
        }
    ]
    client_influxdb.write_points(data)



def on_disconnect(client, userdata, rc):
    logging.info("Disconnected with result code: %s", rc)
    reconnect_count, reconnect_delay = 0, FIRST_RECONNECT_DELAY
    while reconnect_count < MAX_RECONNECT_COUNT:
        logging.info("Reconnecting in %d seconds...", reconnect_delay)
        time.sleep(reconnect_delay)

        try:
            client.reconnect()
            logging.info("Reconnected successfully!")
            return
        except Exception as err:
            logging.error("%s. Reconnect failed. Retrying...", err)

        reconnect_delay *= RECONNECT_RATE
        reconnect_delay = min(reconnect_delay, MAX_RECONNECT_DELAY)
        reconnect_count += 1
    logging.info("Reconnect failed after %s attempts. Exiting...", reconnect_count)
    global FLAG_EXIT
    FLAG_EXIT = True


def on_message_set(client, userdata, message):
    print(f'Received `{message.payload.decode()}` from `{message.topic}` topic')
    splitted = message.topic.split('/')
    if len(splitted) != 3:
        print(f"not enough values o unpack. expected 3, got {len(splitted)}")
        return
    prefix, selector, fn = splitted
    
    # message = json.loads(message.payload.decode())
    
    # selector = message['selector']
    # fn = message['fn']
    # args = message.get('args', [])
    args = [message.payload.decode()]
    if args[0] == '.':
        del args[0]
    else:
        args[0] = float(args[0])

    # print(message['selector'])
    # nhr = NHRs[selector]
    nhr = NHRs.get(selector, False)
    if not nhr:
        return client.publish(TOPIC_PUB, json.dumps("NHR not found"))

    if not hasattr(nhr, fn):
        return client.publish(TOPIC_PUB, json.dumps("Method not found"))
    
    result = getattr(nhr, fn)(*args)

    write_influxdb(fn, args, result)

    client.publish(TOPIC_PUB, json.dumps(result))

def connect_mqtt():
    client = mqtt_client.Client(CLIENT_ID)
    client.on_connect = on_connect
    client.on_message = on_message_set
    client.connect(BROKER, PORT, keepalive=3)
    client.on_disconnect = on_disconnect
    return client


def on_message_get():
    while not FLAG_EXIT:
        nhr = NHRs.get("9410", False)
        values = {
            'NHR' : nhr, 
            'voltage': nhr.getVoltage(),
        }
        # values = json.dumps(values)
      
        write_influxdb('voltage', )
        time.sleep(1)

def run():
    logging.basicConfig(format='%(asctime)s - %(levelname)s: %(message)s',
                        level=logging.DEBUG)
    client = connect_mqtt()
    client.loop_start()
    time.sleep(1000)

    print(NHRs.getVoltage())

    if client.is_connected():
        # on_message_get()
        print("connect")
    else:
        client.loop_stop()

def signal_handler(sig, frame):
    print('You pressed Ctrl+C!')
    client_influxdb.close()
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)
print('Press Ctrl+C')
# signal.pause()

if __name__ == '__main__':
    run()
