###############################################
# RabbitMQ in Action
# Chapter 10 - Queue config watchdog check.
###############################################
# 
# 
# Author: Jason J. W. Williams
# (C)2011
###############################################

import sys, json, httplib, urllib, base64, socket

#(qcwc.0) Nagios status codes
EXIT_OK = 0
EXIT_WARNING = 1
EXIT_CRITICAL = 2
EXIT_UNKNOWN = 3

#/(qcwc.1) Parse arguments
server, port = sys.argv[1].split(":")
vhost = sys.argv[2]
username = sys.argv[3]
password = sys.argv[4]
queue_name = sys.argv[5]
auto_delete = json.loads(sys.argv[6].lower())
durable = json.loads(sys.argv[7].lower())

#/(qcwc.2) Connect to server
conn = httplib.HTTPConnection(server, port)

#/(qcwc.3) Build API path
path = "/api/queues/%s/%s" % (urllib.quote(vhost, safe=""),
                              urllib.quote(queue_name))
method = "GET"

#/(qcwc.4) Issue API request
credentials = base64.b64encode("%s:%s" % (username, password))
try:
    conn.request(method, path, "",
                 {"Content-Type" : "application/json",
                  "Authorization" : "Basic " + credentials})
#/(qcwc.5) Could not connect to API server, return unknown status
except socket.error:
    print "UNKNOWN: Could not connect to %s:%s" % (server, port)
    exit(EXIT_UNKNOWN)

response = conn.getresponse()

#/(qcwc.6) Queue does not exist, return critical status
if response.status == 404:
    print "CRITICAL: Queue %s does not exist." % queue_name
    exit(EXIT_CRITICAL)
#/(qcwc.7) Unexpected API error, return unknown status
elif response.status > 299:
    print "UNKNOWN: Unexpected API error: %s" % response.read()
    exit(EXIT_UNKNOWN)

#/(qcwc.8) Parse API response
response = json.loads(response.read())

#/(qcwc.9) Queue auto_delete flag incorrect, return warning status
if response["auto_delete"] != auto_delete:
    print "WARN: Queue '%s' - auto_delete flag is NOT %s." % \
          (queue_name, auto_delete)
    exit(EXIT_WARNING)

#/(qcwc.10) Queue durable flag incorrect, return warning status
if response["durable"] != durable:
    print "WARN: Queue '%s' - durable flag is NOT %s." % \
          (queue_name, durable)
    exit(EXIT_WARNING)


#/(qcwc.11) Queue exists and it's flags are correct, return OK status
print "OK: Queue %s configured correctly." % queue_name
exit(EXIT_OK)