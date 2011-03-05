###############################################
# RabbitMQ in Action
# Chapter 4.3.3 - RPC Client
# 
# Requires: pika >= 0.9.5
# 
# Author: Jason J. W. Williams
# (C)2011
###############################################
import time, json, pika

#/(rpcc.0) Establish connection to broker
creds_broker = pika.PlainCredentials("rpc_user", "rpcme")
conn_params = pika.ConnectionParameters("localhost",
                                        virtual_host = "/",
                                        credentials = creds_broker)
conn_broker = pika.BlockingConnection(conn_params)
channel = conn_broker.channel()

#/(rpcc.1) Issue RPC call & wait for reply
msg = json.dumps({"client_name": "RPC Client 1.0", 
                  "time" : time.time()})

result = channel.queue_declare(exclusive=True, auto_delete=True)
msg_props = pika.BasicProperties()
msg_props.reply_to=result.method.queue

channel.basic_publish(body=msg,
                      exchange="rpc",
                      properties=msg_props,
                      routing_key="ping")

print "Sent 'ping' RPC call. Waiting for reply..."

def reply_callback(channel, method, header, body):
    """Receives RPC server replies."""
    print "RPC Reply --- " + body
    channel.stop_consuming()



channel.basic_consume(reply_callback,
                      queue=result.method.queue,
                      consumer_tag=result.method.queue)

channel.start_consuming()