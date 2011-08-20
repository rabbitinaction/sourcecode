###############################################
# RabbitMQ in Action
# Chapter 10 - Queue count (HTTP API) check.
###############################################
# 
# 
# Author: Jason J. W. Williams
# (C)2011
###############################################

import sys, json, httplib, urllib, base64, socket

#(aqcc.0) Nagios status codes
EXIT_OK = 0
EXIT_WARNING = 1
EXIT_CRITICAL = 2
EXIT_UNKNOWN = 3

#/(aqcc.1) Parse arguments
server, port = sys.argv[1].split(":")
vhost = sys.argv[2]
username = sys.argv[3]
password = sys.argv[4]
queue_name = sys.argv[5]
max_unack_critical = int(sys.argv[6])
max_unack_warn = int(sys.argv[7])
max_ready_critical = int(sys.argv[8])
max_ready_warn = int(sys.argv[9])


#/(aqcc.2) Connect to server
conn = httplib.HTTPConnection(server, port)

#/(aqcc.3) Build API path
path = "/api/queues/%s/%s" % (urllib.quote(vhost, safe=""),
                              queue_name)
method = "GET"

#/(aqcc.4) Issue API request
credentials = base64.b64encode("%s:%s" % (username, password))

try:
    conn.request(method, path, "",
                 {"Content-Type" : "application/json",
                  "Authorization" : "Basic " + credentials})

#/(aqcc.5) Could not connect to API server, return unknown status
except socket.error:
    print "UNKNOWN: Could not connect to %s:%s" % (server, port)
    exit(EXIT_UNKNOWN)

response = conn.getresponse()

#/(aqcc.6) RabbitMQ not responding/alive, return critical status
if response.status > 299:
    print "UNKNOWN: Unexpected API error: %s" % response.read()
    exit(EXIT_UNKNOWN)

#/(aqcc.7) Extract message count levels from response
resp_payload = json.loads(response.read())
msg_cnt_unack = resp_payload["messages_unacknowledged"]
msg_cnt_ready = resp_payload["messages_ready"]
msg_cnt_total = resp_payload["messages"]

#/(aqcc.8) Consumed but unackowledged message count above thresholds
if msg_cnt_unack >= max_unack_critical:
    print "CRITICAL: %s - %d unack'd messages." % (queue_name,
                                                   msg_cnt_unack)
    exit(EXIT_CRITICAL)
elif msg_cnt_unack >= max_unack_warn:
    print "WARN: %s - %d unack'd messages." % (queue_name,
                                               msg_cnt_unack)
    exit(EXIT_WARNING)

#/(aqcc.9) Ready to be consumed message count above thresholds
if msg_cnt_ready >= max_ready_critical:
    print "CRITICAL: %s - %d unconsumed messages." % (queue_name,
                                                      msg_cnt_ready)
    exit(EXIT_CRITICAL)
elif msg_cnt_ready >= max_ready_warn:
    print "WARN: %s - %d unconsumed messages." % (queue_name,
                                                  msg_cnt_ready)
    exit(EXIT_WARNING)

# Message counts below thresholds, return OK status
print "OK: %s - %d in-flight messages. %dB used memory." % \
      (queue_name, msg_cnt_total, resp_payload["memory"])
exit(EXIT_OK)