###############################################
# RabbitMQ in Action
# Chapter 10 - Basic Nagios check.
###############################################
# 
# 
# Author: Jason J. W. Williams
# (C)2011
###############################################
import sys, json, httplib, base64

#/(nc.1) Return requested Nagios status code 
status = sys.argv[1]

if status.lower() == "warning":
    print "Status is WARN"
    exit(1)
elif status.lower() == "critical":
    print "Status is CRITICAL"
    exit(2)
elif status.lower() == "unknown":
    print "Status is UNKNOWN"
    exit(3)
else:
    print "Status is OK"
    exit(0)
