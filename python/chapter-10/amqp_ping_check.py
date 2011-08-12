###############################################
# RabbitMQ in Action
# Chapter 10 - RabbitMQ ping (AMQP) check.
###############################################
# 
# 
# Author: Jason J. W. Williams
# (C)2011
###############################################
import sys, pika, socket

#(nc.0) Nagios status codes
EXIT_OK = 0
EXIT_WARNING = 1
EXIT_CRITICAL = 2
EXIT_UNKNOWN = 3

#/(nc.1) Parse command line arguments
server, port = sys.argv[1].split(":")
vhost = sys.argv[2]
username = sys.argv[3]
password = sys.argv[4]

#/(nc.2) Establish connection to broker
creds_broker = pika.PlainCredentials(username, password)
conn_params = pika.ConnectionParameters(server,
                                        virtual_host = vhost,
                                        credentials = creds_broker)
try:
    conn_broker = pika.BlockingConnection(conn_params)
    channel = conn_broker.channel()
except socket.timeout:
#/(nc.3) Connection failed, return CRITICAL status
    print "CRITICAL: Could not connect to %s:%s!" % (server, port)
    exit(EXIT_CRITICAL)

#(nc.4) Connection OK, return OK status
print "OK: Connect to %s:%s successful." % (server, port)
exit(EXIT_OK)