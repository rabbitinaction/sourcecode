###############################################
# RabbitMQ in Action
# Chapter 3.2.2 - Alerting Server Consumer
# 
# Requires: pika >= 0.5
# 
# Author: Jason J. W. Williams
# (C)2010
###############################################
import socket, struct, sys, json, asyncore, smtplib
import pika


def send_mail(recipients, subject, message):
    """E-mail generator for received alerts."""
    headers = "From: %s\r\nTo: \r\nDate: \r\nSubject: %s\r\n\r\n" % ("alerts@ourcompany.com", subject)
    
    smtp_server = smtplib.SMTP()
    smtp_server.connect("mail.ourcompany.com", 25)
    smtp_server.sendmail("alerts@ourcompany.com", recipients, headers + str(message))
    smtp_server.close()

# Notify Processors
def critical_notify(channel, method, header, body):
    """Sends CRITICAL alerts to administrators via e-mail."""
    
    EMAIL_RECIPS = ["ops.team@ourcompany.com",]
    
    # Decode our message from JSON
    if header.content_type != "application/json":
        print "Discarding message. Not JSON."
        channel.basic_ack(delivery_tag=method.delivery_tag)
        return
    
    message = json.loads(body)
    
    # Transmit e-mail to SMTP server
    send_mail(EMAIL_RECIPS, "CRITICAL ALERT", message)
    print "Sent alert via e-mail! Alert Text: %s  Recipients: %s" % (str(message), str(EMAIL_RECIPS))
    
    # Acknowledge the message
    channel.basic_ack(delivery_tag=method.delivery_tag)

def rate_limit_notify(channel, method, header, body):
    """Sends the message to the administrators via e-mail."""
    
    EMAIL_RECIPS = ["api.team@ourcompany.com",]
    
    # Decode our message from JSON
    if header.content_type != "application/json":
        print "Discarding message. Not JSON."
        channel.basic_ack(delivery_tag=method.delivery_tag)
        return
    
    message = json.loads(body)
    
    # Transmit e-mail to SMTP server
    send_mail(EMAIL_RECIPS, "RATE LIMIT ALERT!", message)
    
    print "Sent alert via e-mail! Alert Text: %s  Recipients: %s" % (str(message), str(EMAIL_RECIPS))
    
    # Acknowledge the message
    channel.basic_ack(delivery_tag=method.delivery_tag)


if __name__ == "__main__":
    # Broker settings
    AMQP_SERVER = "localhost"
    AMQP_USER = "alert_user"
    AMQP_PASS = "alertme"
    AMQP_VHOST = "/"
    AMQP_EXCHANGE = "alerts"
    channel = None
    
    # Establish connection to broker
    creds_broker = pika.PlainCredentials(AMQP_USER, AMQP_PASS)
    conn_broker = pika.AsyncoreConnection(pika.ConnectionParameters(AMQP_SERVER,
                                                                    virtual_host = AMQP_VHOST,
                                                                    credentials = creds_broker,
                                                                    heartbeat = 10))
    
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
    channel.basic_consume( critical_notify,
                           queue="critical",
                           no_ack=False,
                           consumer_tag="critical")
    
    channel.basic_consume( rate_limit_notify,
                           queue="rate_limit",
                           no_ack=False,
                           consumer_tag="rate_limit")
    
    print "Ready for alerts!"
    pika.asyncore_loop()
    
    