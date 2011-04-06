###############################################
# RabbitMQ in Action
# Chapter 1 - Hello World Consumer
# 
# Requires: pika >= 0.9.5
# 
# Author: Jason J. W. Williams
# (C)2011
###############################################

import pika

credentials = pika.PlainCredentials("guest", "guest")
conn_params = pika.ConnectionParameters("localhost",
                                        credentials = credentials)
conn_broker = pika.BlockingConnection(conn_params) #/(hwc.1) Establish connection to broker


channel = conn_broker.channel() #/(hwc.2) Obtain channel

channel.exchange_declare(exchange="hello-exchange", #/(hwc.3) Declare the exchange
                         type="direct",
                         passive=False,
                         durable=True,
                         auto_delete=False)

channel.queue_declare(queue="hello-queue") #/(hwc.4) Declare the queue

channel.queue_bind(queue="hello-queue",     #/(hwc.5) Bind the queue and exchange together on the key "hola"
                   exchange="hello-exchange",
                   routing_key="hola")


def msg_consumer(channel, method, header, body): #/(hwc.6) Make function to process incoming messages
    
    channel.basic_ack(delivery_tag=method.delivery_tag)  #/(hwc.7) Message acknowledgement
    
    if body == "quit":
        channel.basic_cancel(consumer_tag="hello-consumer") #/(hwc.8) Stop consuming more messages and quit
        channel.stop_consuming()
    else:
        print body
    
    return



channel.basic_consume( msg_consumer,    #/(hwc.9) Subscribe our consumer
                       queue="hello-queue",
                       consumer_tag="hello-consumer")

channel.start_consuming() #/(hwc.10) Start consuming