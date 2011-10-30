###############################################
# RabbitMQ in Action
# Chapter 5 - Hello World Consumer
#             (Mirrored Queues)
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
conn_broker = pika.BlockingConnection(conn_params) #/(hwcmq.1) Establish connection to broker


channel = conn_broker.channel() #/(hwcmq.2) Obtain channel

channel.exchange_declare(exchange="hello-exchange", #/(hwcmq.3) Declare the exchange
                         type="direct",
                         passive=False,
                         durable=True,
                         auto_delete=False)

queue_args = {"x-ha-policy" : "nodes",
              "x-ha-policy-params" : ["rabbit@Phantome",
                                      "rabbit2@Phantome"]} #/(hwcmq.4) Set queue mirroring policy

channel.queue_declare(queue="hello-queue", arguments=queue_args) #/(hwcmq.5) Declare the queue

channel.queue_bind(queue="hello-queue",     #/(hwcmq.6) Bind the queue and exchange together on the key "hola"
                   exchange="hello-exchange",
                   routing_key="hola")


def msg_consumer(channel, method, header, body): #/(hwcmq.7) Make function to process incoming messages
    
    channel.basic_ack(delivery_tag=method.delivery_tag)  #/(hwcmq.8) Message acknowledgement
    
    if body == "quit":
        channel.basic_cancel(consumer_tag="hello-consumer") #/(hwcmq.9) Stop consuming more messages and quit
        channel.stop_consuming()
    else:
        print body
    
    return



channel.basic_consume( msg_consumer,    #/(hwc.9) Subscribe our consumer
                       queue="hello-queue",
                       consumer_tag="hello-consumer")

channel.start_consuming() #/(hwc.10) Start consuming