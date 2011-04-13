###############################################
# RabbitMQ in Action
# Chapter 5 - Cluster Test Producer
# 
# Requires: pika >= 0.9.5
# 
# Author: Jason J. W. Williams
# (C)2011
###############################################
import sys, time, json, pika

AMQP_HOST = sys.argv[1]
AMQP_PORT = int(sys.argv[2])

#/(ctp.1) Establish connection to broker
creds_broker = pika.PlainCredentials("guest", "guest")
conn_params = pika.ConnectionParameters(AMQP_HOST,
                                        port=AMQP_PORT,
                                        virtual_host = "/",
                                        credentials = creds_broker)

conn_broker = pika.BlockingConnection(conn_params)

channel = conn_broker.channel()

#/(ctp.2) Connect to RabbitMQ and send message

msg = json.dumps({"content": "Cluster Test!", 
                  "time" : time.time()})
msg_props = pika.BasicProperties(content_type="application/json")

channel.basic_publish(body=msg, mandatory=True,
                      exchange="",
                      properties=msg_props,
                      routing_key="cluster_test")

print "Sent cluster test message."

