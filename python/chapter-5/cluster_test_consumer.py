###############################################
# RabbitMQ in Action
# Chapter 5 - Cluster Test Consumer
# 
# Requires: pika >= 0.9.5
# 
# Author: Jason J. W. Williams
# (C)2011
###############################################
import sys, json, pika, time, traceback


def msg_rcvd(channel, method, header, body):
    message = json.loads(body)
    
    #/(ctc.1) Print & acknowledge our message
    print "Received: %(content)s/%(time)d" % message
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
    
    
    #/(ctc.4) On fault, reconnect to RabbitMQ
    while True:
        try:
            #/(ctc.5) Establish connection to RabbitMQ
            conn_broker = pika.BlockingConnection(conn_params)
            
            #/(ctc.6) Custom connection behavior
            channel = conn_broker.channel()
            #/(ctc.7) Declare the exchange, queues & bindings
            channel.exchange_declare( exchange="cluster_test",
                                      type="direct",
                                      auto_delete=False)    
            channel.queue_declare( queue="cluster_test",
                                   auto_delete=False)
            channel.queue_bind( queue="cluster_test",
                                exchange="cluster_test",
                                routing_key="cluster_test")
            
            #/(ctc.8) Start consuming messages
            print "Ready for testing!"
            channel.basic_consume( msg_rcvd,
                                   queue="cluster_test",
                                   no_ack=False,
                                   consumer_tag="cluster_test")
            channel.start_consuming()
        #/(ctc.9) Trap connection errors and print them
        except Exception, e:
            traceback.print_exc()
    
    
    