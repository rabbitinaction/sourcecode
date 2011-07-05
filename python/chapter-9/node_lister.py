###############################################
# RabbitMQ in Action
# Chapter 9 - RMQ Node Lister
###############################################
# 
# 
# Author: Jason J. W. Williams
# (C)2011
###############################################
import sys, json, httplib, base64

#/(nl.1) Assign arguments
if len(sys.argv) < 4:
    print "USAGE: node_lister.py server_name:port auth_user auth_pass"
    sys.exit(1)

server, port = sys.argv[1].split(":")
username = sys.argv[2]
password = sys.argv[3]

#/(nl.2) Connect to server
conn = httplib.HTTPConnection(server, port)

#/(nl.3) Build API path
path = "/api/nodes"
method = "GET"

#/(nl.4) Issue API request
credentials = base64.b64encode("%s:%s" % (username, password))
conn.request(method, path, "",
             {"Content-Type" : "application/json",
              "Authorization" : "Basic " + credentials})
response = conn.getresponse()
if response.status > 299:
    print "Error executing API call (%d): %s" % (response.status,
                                                 response.read())
    sys.exit(2)

#/(nl.6) Parse and display node list
resp_payload = json.loads(response.read())
for node in resp_payload:
    print "Node '%(name)s'" % node
    print "================"
    print "\t Memory Used: %(mem_used)d" % node
    print "\t Memory Limit: %(mem_limit)d" % node
    print "\t Uptime (secs): %(uptime)d" % node
    print "\t CPU Count: %(processors)d" % node
    print "\t Node Type: %(type)s" % node
    print "\t Erlang Version: %(erlang_version)s"  % node
    print "\n"
    print "\tInstalled Apps/Plugins"
    print "\t----------------------"
    for app in node["applications"]:
        print "\t\t%(name)s" % app
        print "\t\t\tVersion: %(version)s" % app
        print "\t\t\tDescription: %(description)s\n" % app

sys.exit(0)