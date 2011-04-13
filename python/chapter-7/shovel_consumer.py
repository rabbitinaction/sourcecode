###############################################
# RabbitMQ in Action
# Chapter 5 - Shovel Test Consumer
# 
# Requires: pika >= 0.9.5
# 
# Author: Jason J. W. Williams
# (C)2011
###############################################
import sys, json, pika, time, traceback


def msg_rcvd(channel, method, header, body):
    message = json.loads(body)
    
    #/(ctc.1) Print & acknowledge our order
    print "Received order %(ordernum)d for %(type)s." % message
    channel.basic_ack(delivery_tag=method.delivery_tag)


if __name__ == "__main__":
    #/(ctc.2) Broker settings
    AMQP_SERVER = sys.argv[1]
    AMQP_PORT = int(sys.argv[2])
    
    #/(ctc.3) Establish broker connection settings
    creds_broker = pika.PlainCredentials("guest", "guest")
    conn_params = pika.ConnectionParameters( AMQP_SERVER,
                                             port=AMQP_PORT,
                                             virtual_host="/",
                                             credentials=creds_broker)
    
    #/(ctc.5) Establish connection to RabbitMQ
    conn_broker = pika.BlockingConnection(conn_params)
    channel = conn_broker.channel()
    
    #/(ctc.8) Start processing orders
    print "Ready for orders!"
    channel.basic_consume( msg_rcvd,
                           queue="warehouse_carpinteria",
                           no_ack=False,
                           consumer_tag="order_processor")
    channel.start_consuming()
    