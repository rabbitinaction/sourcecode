###############################################
# RabbitMQ in Action
# Chapter 9 - RMQ Queue Statistics
###############################################
# 
# Author: Jason J. W. Williams
# (C)2011
###############################################
import sys, json, httplib, urllib, base64

#/(uvm.1) Assign arguments
if len(sys.argv) < 6:
    print "USAGE: queue_stats.py server_name auth_user auth_pass VHOST QUEUE_NAME"
    sys.exit(1)

server, port = sys.argv[1].split(":")
username = sys.argv[2]
password = sys.argv[3]
vhost = sys.argv[4]
queue_name = sys.argv[5]

#/(uvm.2) Connect to server
conn = httplib.HTTPConnection(server, port)

#/(uvm.3) Build API path
vhost = urllib.quote(vhost, safe='')
queue_name = urllib.quote(queue_name, safe='')
path = "/api/queues/%s/%s" % (vhost, queue_name)
method = "GET"

#/(uvm.4) Issue API request
credentials = base64.b64encode("%s:%s" % (username, password))
conn.request(method, path, "",
             {"Content-Type" : "application/json",
              "Authorization" : "Basic " + credentials})
response = conn.getresponse()
if response.status > 299:
    print "Error executing API call (%d): %s" % (response.status,
                                                 response.read())
    sys.exit(2)

#/(uvm.6) Parse and display node list
resp_payload = json.loads(response.read())

print "'%s' Queue Stats" % urllib.unquote(queue_name)
print "-----------------"
print "\tMemory Used (bytes): %(memory)d" % resp_payload
print "\tConsumer Count: %(consumers)d" % resp_payload
print "\tMessages:"
print "\t\tUnack'd: %(messages_unacknowledged)d" % resp_payload
print "\t\tReady: %(messages_ready)d" % resp_payload
print "\t\tTotal: %(messages)d" % resp_payload

sys.exit(0)