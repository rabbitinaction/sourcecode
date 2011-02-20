###############################################
# RabbitMQ in Action
# Chapter 4 - Cluster Test Consumer
# 
# Requires: pika >= 0.5
# 
# Author: Jason J. W. Williams
# (C)2011
###############################################
import sys, json, pika
from pika.connection import SimpleReconnectionStrategy



def msg_rcvd(channel, method, header, body):        
    #/(ctc.0) Decode our message from JSON
    if header.content_type != "application/json":
        print "Discarding message. Not JSON."
        channel.basic_ack(delivery_tag=method.delivery_tag)
        return
    
    message = json.loads(body)
    
    #/(ctc.1) Print & acknowledge our message
    print "Received: %(content)s/%(time)d" % message
    channel.basic_ack(delivery_tag=method.delivery_tag)


if __name__ == "__main__":
    #/(ctc.2) Broker settings
    AMQP_SERVER = sys.argv[1]
    AMQP_PORT = int(sys.argv[2])
    AMQP_USER = "guest"
    AMQP_PASS = "guest"
    AMQP_VHOST = "/"
    AMQP_EXCHANGE = "cluster_test"
    
    #/(ctc.3) Establish broker connection settings
    creds_broker = pika.PlainCredentials(AMQP_USER, AMQP_PASS)
    conn_params = pika.ConnectionParameters(AMQP_SERVER,
                                            port=AMQP_PORT,
                                            virtual_host = AMQP_VHOST,
                                            credentials = creds_broker,
                                            heartbeat = 10)
    
    #/(ctc.4) Custom connection behavior
    class CustomReconnectionStrategy(SimpleReconnectionStrategy):
    
        def on_connection_open(self, conn):
            self._reset()
            channel = conn.channel()

            #/(ctc.5) Declare the exchange, queues & bindings
            channel.exchange_declare( exchange=AMQP_EXCHANGE,
                                      type="direct",
                                      auto_delete=False)    
            channel.queue_declare(queue="cluster_test", auto_delete=False)
            channel.queue_bind(queue="cluster_test",
                               exchange=AMQP_EXCHANGE,
                               routing_key="cluster_test")

            #/(ctc.6) Make our msg processor
            channel.basic_consume( msg_rcvd,
                                   queue="cluster_test",
                                   no_ack=False,
                                   consumer_tag="cluster_test")
        
            print "Ready for testing!"
    
    #/(ctc.7) Establish connection to RabbitMQ
    reconnect = CustomReconnectionStrategy()
    conn_broker = pika.AsyncoreConnection(conn_params,
                                          reconnection_strategy=reconnect)
    
    pika.asyncore_loop()
    
    