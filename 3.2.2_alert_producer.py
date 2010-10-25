###############################################
# RabbitMQ in Action
# Chapter 3.2.2 - Alerting Producer
# 
# Requires: pika >= 0.5
# 
# Author: Jason J. W. Williams
# (C)2010
###############################################
import socket, struct, sys, json
import pika
from optparse import OptionParser


# Read in command line arguments
opt_parser = OptionParser()
opt_parser.add_option("-r", "--routing-key", dest="routing_key", help="Routing key for message (e.g. myalert.im)")
opt_parser.add_option("-m", "--message", dest="message", help="Message text for alert.")

args = opt_parser.parse_args()[0]


# Establish connection to broker
creds_broker = pika.PlainCredentials("alert_user", "alertme")
conn_broker = pika.AsyncoreConnection(pika.ConnectionParameters("localhost",
                                                                virtual_host = "/",
                                                                credentials = creds_broker,
                                                                heartbeat = 10))

channel = conn_broker.channel()

# Publish alert message to broker
msg = json.dumps(args.message)
msg_props = pika.BasicProperties()
msg_props.content_type = "application/json"
msg_props.durable = False

channel.basic_publish(body=msg,
                      exchange="alerts",
                      properties=msg_props,
                      routing_key=args.routing_key,
                      block_on_flow_control = True)
channel.close()
conn_broker.close()

print "Sent message %s tagged with routing key '%s' to exchange '/'." % (json.dumps(args.message),
                                                                         args.routing_key)