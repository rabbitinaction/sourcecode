###############################################
# RabbitMQ in Action
# Chapter 3.3.3 - RPC Client
# 
# Requires: pika >= 0.5
# 
# Author: Jason J. W. Williams
# (C)2010
###############################################
import sys, asyncore, time, json
import pika

# Establish connection to broker
creds_broker = pika.PlainCredentials("rpc_user", "rpcme")
conn_params = pika.ConnectionParameters("localhost",
                                        virtual_host = "/",
                                        credentials = creds_broker,
                                        heartbeat = 10)
conn_broker = pika.AsyncoreConnection(conn_params)
channel = conn_broker.channel()

# Issue RPC call & wait for reply
msg = json.dumps({"client_name": "RPC Client 1.0", 
                  "time" : time.time()})

result = channel.queue_declare(exclusive=True, auto_delete=True)
msg_props = pika.BasicProperties()
msg_props.reply_to=result.queue

channel.basic_publish(body=msg,
                      exchange="rpc",
                      properties=msg_props,
                      routing_key="ping",
                      block_on_flow_control = True)

print "Sent 'ping' RPC call. Waiting for reply..."

def reply_callback(channel, method, header, body):
    """Receives RPC server replies."""
    print "RPC Reply --- " + body
    channel.close()
    asyncore.close_all()



channel.basic_consume(reply_callback,
                      queue=result.queue,
                      consumer_tag=result.queue)

asyncore.loop()