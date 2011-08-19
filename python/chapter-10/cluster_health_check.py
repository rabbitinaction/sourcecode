###############################################
# RabbitMQ in Action
# Chapter 10 - Cluster health check.
###############################################
# 
# 
# Author: Jason J. W. Williams
# (C)2011
###############################################

import sys, json, httplib, base64, socket

#(chc.0) Nagios status codes
EXIT_OK = 0
EXIT_WARNING = 1
EXIT_CRITICAL = 2
EXIT_UNKNOWN = 3

#/(chc.1) Parse arguments
server, port = sys.argv[1].split(":")
username = sys.argv[2]
password = sys.argv[3]
node_list = sys.argv[4].split(",")
mem_critical = int(sys.argv[5])
mem_warning = int(sys.argv[6])

#/(chc.2) Connect to server
conn = httplib.HTTPConnection(server, port)

#/(chc.3) Build API path
path = "/api/nodes"
method = "GET"

#/(chc.4) Issue API request
credentials = base64.b64encode("%s:%s" % (username, password))
try:
    conn.request(method, path, "",
                 {"Content-Type" : "application/json",
                  "Authorization" : "Basic " + credentials})
#/(chc.5) Could not connect to API server, return unknown status
except socket.error:
    print "UNKNOWN: Could not connect to %s:%s" % (server, port)
    exit(EXIT_UNKNOWN)

response = conn.getresponse()

#/(chc.6) Unexpected API error, return unknown status
if response.status > 299:
    print "UNKNOWN: Unexpected API error: %s" % response.read()
    exit(EXIT_UNKNOWN)

#/(chc.7) Parse API response
response = json.loads(response.read())

#/(chc.8) Cluster is missing nodes, return warning status
for node in response:
    if node["name"] in node_list and node["running"] != False:
        node_list.remove(node["name"])

if len(node_list):
    print "WARNING: Cluster missing nodes: %s" % str(node_list)
    exit(EXIT_WARNING)

#/(chc.9) Node used memory is over limit
for node in response:
    if node["mem_used"] > mem_critical:
        print "CRITICAL: Node %s memory usage is %d." % \
              (node["name"], node["mem_used"])
        exit(EXIT_CRITICAL)
    elif node["mem_used"] > mem_warning:
        print "WARNING: Node %s memory usage is %d." % \
              (node["name"], node["mem_used"])
        exit(EXIT_WARNING)

#/(chc.10) All nodes present and used memory below limit
print "OK: %d nodes. All memory usage below %d." % (len(response),
                                                    mem_warning)
exit(EXIT_OK)