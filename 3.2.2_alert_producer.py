###############################################
# RabbitMQ in Action
# Chapter 4.3.3 - Alerting Producer
# 
# Author: Jason J. W. Williams
# (C)2010
###############################################
import socket, struct, sys, json
from amqplib import client_0_8 as amqp
from optparse import OptionParser


# Read in command line arguments
opt_parser = OptionParser()
opt_parser.add_option("-r", "--routing-key", dest="routing_key", help="Routing key for message (e.g. myalert.im)")
opt_parser.add_option("-m", "--message", dest="message", help="Message text for alert.")

args = opt_parser.parse_args()[0]


# Establish connection to broker
conn_broker = amqp.Connection( host="localhost",
                               userid="alert_user",
                               password="alertme",
                               virtual_host="/" )

channel = conn_broker.channel()

# Publish alert message to broker
try:
    msg = amqp.Message(json.dumps(args.message))
    channel.basic_publish(msg, exchange="alerts", routing_key=args.routing_key)
    channel.close()
    conn_broker.close()
except Exception, e:
    print "Error publish message. %s" % str(e)
    sys.exit(-1)

print "Sent message %s tagged with routing key '%s' to exchange '/'." % (json.dumps(args.message),
                                                                         args.routing_key)