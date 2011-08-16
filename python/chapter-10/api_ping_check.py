###############################################
# RabbitMQ in Action
# Chapter 10 - RabbitMQ ping (HTTP API) check.
###############################################
# 
# 
# Author: Jason J. W. Williams
# (C)2011
###############################################

import sys, json, httplib, urllib, base64, socket

#(apic.0) Nagios status codes
EXIT_OK = 0
EXIT_WARNING = 1
EXIT_CRITICAL = 2
EXIT_UNKNOWN = 3

#/(apic.1) Parse arguments
server, port = sys.argv[1].split(":")
vhost = sys.argv[2]
username = sys.argv[3]
password = sys.argv[4]

#/(apic.2) Connect to server
conn = httplib.HTTPConnection(server, port)

#/(apic.3) Build API path
path = "/api/aliveness-test/%s" % urllib.quote(vhost, safe="")
method = "GET"

#/(apic.4) Issue API request
credentials = base64.b64encode("%s:%s" % (username, password))

try:
    conn.request(method, path, "",
                 {"Content-Type" : "application/json",
                  "Authorization" : "Basic " + credentials})

#/(apic.5) Could not connect to API server, return critical status
except socket.error:
    print "CRITICAL: Could not connect to %s:%s" % (server, port)
    exit(EXIT_CRITICAL)

response = conn.getresponse()

#/(apic.6) RabbitMQ not responding/alive, return critical status
if response.status > 299:
    print "CRITICAL: Broker not alive: %s" % response.read()
    exit(EXIT_CRITICAL)

#/(apic.7) RabbitMQ alive, return OK status
print "OK: Broker alive: %s" % response.read()
exit(EXIT_OK)
