###############################################
# RabbitMQ in Action
# Chapter 4.3.3 - Alerting Server Consumer
# 
# Requires: py-amqplib >= 0.5
#           xmppy >= 0.5
#           python-twitter >= 0.6
# 
# Author: Jason J. W. Williams
# (C)2010
###############################################
import socket, struct, sys, json, smtplib
from amqplib import client_0_8 as amqp


def send_mail(recipients, subject, message):
    headers = "From: %s\r\nTo: \r\nDate: \r\nSubject: %s\r\n\r\n" % ("alerts@ourcompany.com", subject)
    
    smtp_server = smtplib.SMTP()
    smtp_server.connect("mail.ourcompany.com", 25)
    smtp_server.sendmail("alerts@ourcompany.com", recipients, headers + str(message))
    smtp_server.close()

# Notify Processors
def critical_notify(msg):
    """Sends CRITICAL alerts to administrators via e-mail."""
    global channel
    
    EMAIL_RECIPS = ["ops.team@ourcompany.com",]
    
    # Decode our message from JSON
    message = json.loads(msg.body)
    
    # Transmit e-mail to SMTP server
    send_mail(EMAIL_RECIPS, "CRITICAL ALERT", message)
    print "Sent alert via e-mail! Alert Text: %s  Recipients: %s" % (str(message), str(EMAIL_RECIPS))
    
    # Acknowledge the message
    channel.basic_ack(msg.delivery_tag)

def rate_limit_notify(msg):
    """Sends the message to the administrators via e-mail."""
    global channel
    
    EMAIL_RECIPS = ["api.team@ourcompany.com",]
    
    # Decode our message from JSON
    message = json.loads(msg.body)
    
    # Transmit e-mail to SMTP server
    send_mail(EMAIL_RECIPS, "RATE LIMIT ALERT!", message)
    
    print "Sent alert via e-mail! Alert Text: %s  Recipients: %s" % (str(message), str(EMAIL_RECIPS))
    
    # Acknowledge the message
    channel.basic_ack(msg.delivery_tag)


if __name__ == "__main__":
    # Broker settings
    AMQP_SERVER = "localhost:5672"
    AMQP_USER = "alert_user"
    AMQP_PASS = "alertme"
    AMQP_VHOST = "/"
    AMQP_EXCHANGE = "alerts"
    channel = None
    
    # Establish connection to broker
    conn_broker = amqp.Connection( host=AMQP_SERVER,
                                   userid=AMQP_USER,
                                   password=AMQP_PASS,
                                   virtual_host=AMQP_VHOST )
    
    channel = conn_broker.channel()
    
    # Declare the Exchange
    channel.exchange_declare( exchange=AMQP_EXCHANGE,
                              type="topic",
                              auto_delete=False)
    
    # Build the queues and bindings for our topics    
    channel.queue_declare(queue="critical", auto_delete=False)
    channel.queue_bind(queue="critical", exchange="alerts", routing_key="critical.*")
    
    channel.queue_declare(queue="rate_limit", auto_delete=False)
    channel.queue_bind(queue="rate_limit", exchange="alerts", routing_key="*.rate_limit")
    
    # Make our alert processors
    channel.basic_consume( queue="critical",
                           no_ack=False,
                           callback=critical_notify,
                           consumer_tag="critical")
    
    channel.basic_consume( queue="rate_limit",
                           no_ack=False,
                           callback=rate_limit_notify,
                           consumer_tag="rate_limit")
    
    print "Ready for alerts!"
    while True:
        channel.wait()
    
    