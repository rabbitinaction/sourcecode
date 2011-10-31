###############################################
# RabbitMQ in Action
# Chapter 1 - Hello World Producer
#             w/ Publisher Confirms
# 
# Requires: pika >= 0.9.6
# 
# Author: Jason J. W. Williams
# (C)2011
###############################################

import pika, sys
from pika import spec

credentials = pika.PlainCredentials("guest", "guest")
conn_params = pika.ConnectionParameters("localhost",
                                        credentials = credentials)
conn_broker = pika.BlockingConnection(conn_params) #/(hwppc.1) Establish connection to broker


channel = conn_broker.channel() #/(hwppc.2) Obtain channel

def confirm_handler(frame): #/(hwppc.3) Publisher confirm handler
    if type(frame.method) == spec.Confirm.SelectOk:
        print "Channel in 'confirm' mode."
    elif type(frame.method) == spec.Basic.Nack:
        print "Nack received."
    elif type(frame.method) == spec.Basic.Ack:
        if frame.method.delivery_tag == msg_id_no:
            print "Confirm received!"


#/(hwppc.4) Put channel in "confirm" mode
channel.confirm_delivery(callback=confirm_handler)

msg = sys.argv[1]
msg_props = pika.BasicProperties()
msg_props.content_type = "text/plain" #/(hwppc.5) Create a plaintext message

msg_id_no = 0 #/(hwppc.6) Reset publisher confirm start ID

channel.basic_publish(body=msg,
                      exchange="hello-exchange",
                      properties=msg_props,
                      routing_key="hola") #/(hwppc.7) Publish the message

msg_id_no = msg_id_no + 1 #/(hwppc.8) Increment published message ID

channel.close()

