#!/usr/bin/env python
# -*- coding: utf-8 -*-

import RPi.GPIO as GPIO
import dht11
import time
import datetime
import paho.mqtt.client as mqttClient
import time

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to broker")
        global Connected                #Use global variable
        Connected = True                #Signal connection 
    else:
        print("Connection failed")
 
# initialize GPIO
GPIO.setwarnings(True)
GPIO.setmode(GPIO.BCM)

# read data using pin GPIO4
instance = dht11.DHT11(pin=4)

Connected = False   #global variable for the state of the connection
broker_address= "eselgurke.local"
port = 1883
#user = ""
#password = ""
client = mqttClient.Client("Python")               #create new instance
#client.username_pw_set(user, password=password)    #set username and password
client.on_connect= on_connect                      #attach function to callback
client.connect(broker_address, port=port)          #connect to broker
client.loop_start()        #start the loop

# example topic: prometheus/job/ESP8266/instance/livingroom/temperature_celsius
broker_topic_prefix = 'prometheus'
broker_topic_job = 'hum_temp'
broker_topic_instance = 'livingroom'

while Connected != True:    #Wait for connection
    time.sleep(0.1)

try:
    while True:
        result = instance.read()
        if result.is_valid():
            print("Last valid input: " + str(datetime.datetime.now()))
            print("Temperature: %-3.1f C" % result.temperature)
            print("Humidity: %-3.1f %%" % result.humidity)
            client.publish(broker_topic_prefix+'/job/'+broker_topic_job+'/instance/'+broker_topic_instance+'/temperature_celsius', str(result.temperature), 0, True)
            client.publish(broker_topic_prefix+'/job/'+broker_topic_job+'/instance/'+broker_topic_instance+'/humidity', str(result.humidity), 0, True)
            time.sleep(60)
except KeyboardInterrupt:
    client.disconnect()
    client.loop_stop()
