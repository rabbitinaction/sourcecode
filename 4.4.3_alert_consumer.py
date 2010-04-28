###############################################
# RabbitMQ in Action
# Chapter 4.3.3 - Alerting Server Consumer
# 
# Requires: py-amqplib >= 0.5
#           pyxmpp >= 1.1.1
# 
# Author: Jason J. W. Williams
# (C)2010
###############################################
import socket, struct, sys, json, smtplib
import pyxmpp
from amqplib import client_0_8 as amqp

# Broker settings
AMQP_SERVER = "localhost:5672"
AMQP_USER = "alert_user"
AMQP_PASS = "alertme"
AMQP_VHOST = "/"
AMQP_EXCHANGE = "alerts"
channel = None

# Twitter settings
TWITTER_ENDPOINT = "http://"
TWITTER_USER = "joetwit"
TWITTER_PASS = "joepass"

# Email (SMTP) settings
EMAIL_SERVER = "204.134.222.177"
EMAIL_PORT = 25
EMAIL_FROM = "alerts@mycorp.tld"
EMAIL_SUBJECT = "Web Process Alert!"
EMAIL_RECIPS = ["williamsjj@digitar.com",]

# IM (XMPP) settings
IM_SERVER = "talk.google.com"
IM_PORT = 5223
IM_USER = "joe"
IM_PASS = "test"
IM_RECIPS = ["jasonjwwilliams@gmail.com", "williamsjj@digitar.com"]


# Notify Processors
def twitter_notify(msg):
    """Sends the message text as a Twitter direct message to the specified Twitter recipient."""
    global channel
    
    # Decode our message from JSON
    try:
        message = json.loads(msg.body)
    except Exception, e:
        print "Problem decoding JSON message. %s" % str(e)
        channel.basic_ack(msg.delivery_tag)
        return
    
    # Transmit message to Twitter
    try:
        print "Sending to Twitter!"
    except Exception, e:
        print "Problem transmitting to Twitter. %s" % str(e)
        channel.basic_ack(msg.delivery_tag)
        return
    
    # Acknowledge the message
    channel.basic_ack(msg.delivery_tag)

def im_notify(msg):
    """Sends an IM with the message text to the specified recipient."""
    global channel

    # Decode our message from JSON
    try:
        message = json.loads(msg.body)
    except Exception, e:
        print "Problem decoding JSON message. %s" % str(e)
        channel.basic_ack(msg.delivery_tag)
        return

    # Transmit message to XMPP server
    #try:
    xmpp_id = pyxmpp.all.JID(IM_USER)
    if not xmpp_id.resource:
        xmpp_id = pyxmpp.all.JID(xmpp_id.node, xmpp_id.domain, "rabbitAlertProducer")
    
    tls = pyxmpp.streamtls.TLSSettings(require=True, verify_peer=False)
    
    for recipient in IM_RECIPS:
        pyxmpp.jabber.simple.send_message(xmpp_id, IM_PASS, pyxmpp.jid.JID(recipient), str(message), "Web Alert!")
    #except Exception, e:
    #    print "Problem transmitting to IM server. %s" % str(e)
    #    channel.basic_ack(msg.delivery_tag)
    #    return

    # Acknowledge the message
    channel.basic_ack(msg.delivery_tag)

def email_notify(msg):
    """Sends an email with the message text to the specified recipient."""
    global channel

    # Decode our message from JSON
    try:
        message = json.loads(msg.body)
    except Exception, e:
        print "Problem decoding JSON message. %s" % str(e)
        channel.basic_ack(msg.delivery_tag)
        return

    # Transmit e-mail to SMTP server
    try:
        headers = "From: %s\r\nTo: \r\nDate: \r\nSubject: %s\r\n\r\n" % (EMAIL_FROM, EMAIL_SUBJECT)
        
        smtp_server = smtplib.SMTP()
        smtp_server.connect(EMAIL_SERVER, EMAIL_PORT)
        smtp_server.sendmail(EMAIL_FROM, EMAIL_RECIPS, headers + str(message))
        smtp_server.close()
        
        print "Sent alert via e-mail! Alert Text: %s  Recipients: %s" % (str(message), str(EMAIL_RECIPS))
    except Exception, e:
        print "Problem transmitting to e-mail server. %s" % str(e)
        channel.basic_ack(msg.delivery_tag)
        return

    # Acknowledge the message
    channel.basic_ack(msg.delivery_tag)


TWITTER = { "queue" : "twitter",
            "callback" : twitter_notify }
IM      = { "queue" : "im",
            "callback" : im_notify }
EMAIL   = { "queue" : "email",
            "callback" : email_notify }



# Topic Bindings
topic_bindings = [ ("req-per-sec.*", (EMAIL,)),
                   ("mal-req_vol.*", (EMAIL, IM)),
                   ("talky-ip.*", (EMAIL,TWITTER)),
                   ("*.email", (EMAIL,)),
                   ("*.twitter", (TWITTER,)),
                   ("*.im", (IM,)) ]






if __name__ == "__main__":
    
    # Establish connection to broker and declare echange
    try:
        conn_broker = amqp.Connection( host=AMQP_SERVER,
                                       userid=AMQP_USER,
                                       password=AMQP_PASS,
                                       virtual_host=AMQP_VHOST )
        
        channel = conn_broker.channel()
    
    except (socket.gaierror, socket.error, IOError), e:
        print "Error connecting to server! %s" % str(e)
        sys.exit(-1)
    except struct.error, e:
        print "Couldn't log on to vhost! Please check your credentials."
        sys.exit(-1)
    
    try:
        channel.exchange_declare( exchange=AMQP_EXCHANGE,
                                  type="topic",
                                  auto_delete=False)
    except Exception, e:
        print "Couldn't create exchange! %s" % str(e)
        sys.exit(-1)
    
    # Build the queues and bindings for our topics
    for binding in topic_bindings:
        try:
            for notify_type in binding[1]:
                channel.queue_declare( queue=notify_type["queue"],
                                       auto_delete=False)
                channel.queue_bind( queue=notify_type["queue"],
                                    exchange=AMQP_EXCHANGE,
                                    routing_key=binding[0])
        except Exception, e:
            print "Error encountered creating queues and bindings. %s" % str(e)
            sys.exit(-1)
    
    
    # Make our alert processors
    try:
        channel.basic_consume( queue=TWITTER["queue"],
                               no_ack=False,
                               callback=TWITTER["callback"],
                               consumer_tag="twitter")
        
        channel.basic_consume( queue=IM["queue"],
                               no_ack=False,
                               callback=IM["callback"],
                               consumer_tag="im")
        
        channel.basic_consume( queue=EMAIL["queue"],
                               no_ack=False,
                               callback=EMAIL["callback"],
                               consumer_tag="email")
    except amqp.AMQPChannelException, e:
        print "One or more queues does not exist on the broker. Could not set up consumption."
        sys.exit(-1)
    except Exception, e:
        print "Unexpected connection error setting up channel consumers."
        sys.exit(-1)
    
    print "Ready for alerts!"
    while True:
        channel.wait()
    
    