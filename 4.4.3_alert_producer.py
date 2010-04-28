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
opt_parser.add_option("-s", "--server", dest="broker_server", default="localhost:5672", help="AMQP server & port (e.g. localhost:5672)")
opt_parser.add_option("-u", "--user", dest="broker_user", help="AMQP username")
opt_parser.add_option("-p", "--password", dest="broker_pass", help="AMQP password")
opt_parser.add_option("-v", "--vhost", dest="broker_vhost", help="AMQP vhost")
opt_parser.add_option("-e", "--exchange", dest="broker_exchange", help="AMQP exchange to publish to")
opt_parser.add_option("-r", "--routing-key", dest="routing_key", help="Routing key for message (e.g. myalert.im)")
opt_parser.add_option("-m", "--message", dest="message", help="Message text for alert.")

args = opt_parser.parse_args()[0]

if not(args.broker_server and args.broker_user and args.broker_pass and \
       args.broker_vhost and args.broker_exchange and args.routing_key and args.message):
    print "Required arguments missing. Please use --help for details."
    sys.exit(-1)

# Establish connection to broker
conn_broker = amqp.Connection( host=args.broker_server,
                               userid=args.broker_user,
                               password=args.broker_pass,
                               virtual_host=args.broker_vhost )

channel = conn_broker.channel()

# Publish alert message to broker
try:
    msg = amqp.Message(json.dumps(args.message))
    msg.properties["delivery_mode"] = 2 # Durable
    
    channel.basic_publish(msg, exchange=args.broker_exchange, routing_key=args.routing_key)
    channel.close()
    conn_broker.close()
except Exception, e:
    print "Error publish message. %s" % str(e)
    sys.exit(-1)

print "Sent message %s tagged with routing key '%s' to exchange '%s'." % (json.dumps(args.message),
                                                                         args.routing_key,
                                                                         args.broker_exchange)