###############################################
# RabbitMQ in Action
# Chapter 10 - Queue count (AMQP) check.
###############################################
# 
# 
# Author: Jason J. W. Williams
# (C)2011
###############################################
import sys, pika, socket

#(aqcc.0) Nagios status codes
EXIT_OK = 0
EXIT_WARNING = 1
EXIT_CRITICAL = 2
EXIT_UNKNOWN = 3

#/(aqcc.1) Parse command line arguments
server, port = sys.argv[1].split(":")
vhost = sys.argv[2]
username = sys.argv[3]
password = sys.argv[4]
queue_name = sys.argv[5]
max_critical = int(sys.argv[6])
max_warn = int(sys.argv[7])

#/(aqcc.2) Establish connection to broker
creds_broker = pika.PlainCredentials(username, password)
conn_params = pika.ConnectionParameters(server,
                                        virtual_host = vhost,
                                        credentials = creds_broker)
try:
    conn_broker = pika.BlockingConnection(conn_params)
    channel = conn_broker.channel()
except socket.timeout:
#/(aqcc.3) Connection failed, return unknown status
    print "Unknown: Could not connect to %s:%s!" % (server, port)
    exit(EXIT_UNKNOWN)

try:
    response = channel.queue_declare(queue=queue_name,
                                     passive=True)
except pika.exceptions.AMQPChannelError:
    print "CRITICAL: Queue %s does not exist." % queue_name
    exit(EXIT_CRITICAL)

#(aqcc.4) Message count is above critical limit
if response.method.message_count >= max_critical:
    print "CRITICAL: Queue %s message count: %d" % \
          (queue_name, response.method.message_count)
    exit(EXIT_CRITICAL)

#(aqcc.5) Message count is above warning limit
if response.method.message_count >= max_warn:
    print "WARN: Queue %s message count: %d" % \
          (queue_name, response.method.message_count)
    exit(EXIT_WARNING)

#(aqcc.6) Connection OK, return OK status
print "OK: Queue %s message count: %d" % \
      (queue_name, response.method.message_count)
exit(EXIT_OK)