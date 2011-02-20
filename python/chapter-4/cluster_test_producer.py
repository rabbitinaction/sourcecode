###############################################
# RabbitMQ in Action
# Chapter 4 - Cluster Test Producer
# 
# Requires: pika >= 0.5
# 
# Author: Jason J. W. Williams
# (C)2011
###############################################
import sys, time, json, pika
from pika.connection import SimpleReconnectionStrategy

AMQP_HOST = sys.argv[1]
AMQP_PORT = int(sys.argv[2])

#/(ctp.1) Establish connection to broker
creds_broker = pika.PlainCredentials("guest", "guest")
conn_params = pika.ConnectionParameters(AMQP_HOST,
                                        port=AMQP_PORT,
                                        virtual_host = "/",
                                        credentials = creds_broker,
                                        heartbeat = 10)

#/(ctp.2) Configure Pika to auto-reconnect to RabbitMQ
reconnect = SimpleReconnectionStrategy()
conn_broker = pika.AsyncoreConnection(conn_params,
                                      reconnection_strategy=reconnect)
channel = conn_broker.channel()

#/(ctp.3) Send AMQP message
msg = json.dumps({"content": "Cluster Test!", 
                  "time" : time.time()})
msg_props = pika.BasicProperties()
msg_props.content_type="application/json"

channel.basic_publish(body=msg,
                      exchange="cluster_test",
                      properties=msg_props,
                      routing_key="cluster_test")

print "Sent cluster test message."
