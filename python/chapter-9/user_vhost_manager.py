###############################################
# RabbitMQ in Action
# Chapter 9 - RMQ User & Vhost Manager
# 
#   USAGE: 
#       # user_vhost_manager.py "host" "auth_user" "auth_pass" create vhost 'vhostname'
#                               "host" "auth_user" "auth_pass" delete vhost 'vhostname'
#                               "host" "auth_user" "auth_pass" list vhost
#                               "host" "auth_user" "auth_pass" show vhost 'vhostname'
#                               "host" "auth_user" "auth_pass" create user 'user' 'password' 'true/false'
#                               "host" "auth_user" "auth_pass" delete user 'user'
#                               "host" "auth_user" "auth_pass" list user
#                               "host" "auth_user" "auth_pass" show user 'user'
#                               "host" "auth_user" "auth_pass" show permission 'user' 'vhost'
#                               "host" "auth_user" "auth_pass" create permission 'user' 'vhost' 'read' 'write' 'configure'
# 
# Author: Jason J. W. Williams
# (C)2011
###############################################
import sys, json, httplib, base64

base_path = "/api/%ss"

#/(uvm.1) Assign arguments
if len(sys.argv) < 6:
    print "USAGE: user_vhost_manager.py server_name auth_user auth_pass",
    print "ACTION RESOURCE [PARAMS...]"
    sys.exit(1)

server, port = sys.argv[1].split(":")
username = sys.argv[2]
password = sys.argv[3]
action = sys.argv[4]
res_type = sys.argv[5]

if len(sys.argv) > 6:
    res_params = sys.argv[6:]
else:
    res_params = []

#/(uvm.2) Connect to server
conn = httplib.HTTPConnection(server, port)

#/(uvm.3) Build API request
if action == "list":
    path = base_path % res_type
    method = "GET"
else:
    if res_type == "permission":
        path = (base_path % res_type) + ("/%s/%s" % (res_params[0],
                                                     res_params[1])) 
    else:
        path = (base_path % res_type) + "/" + res_params[0]
    
    if action == "create":
        method = "PUT"
    elif action == "delete":
        method = "DELETE"
    elif action == "show":
        method = "GET"


#/(uvm.4) Build JSON arguments
json_args = ""
if action == "create" and res_type == "user":
    json_args = {"password" : res_params[1],
                 "administrator" : json.loads(res_params[2])}
    json_args = json.dumps(json_args)

if action == "create" and res_type == "permission":
    json_args = {"read" : res_params[2],
                 "write" : res_params[3],
                 "configure" : res_params[4]}
    json_args = json.dumps(json_args)

#/(uvm.5) Issue API call
credentials = base64.b64encode("%s:%s" % (username, password))
conn.request(method, path, json_args,
             {"Content-Type" : "application/json",
              "Authorization" : "Basic " + credentials})
response = conn.getresponse()
if response.status > 299:
    print "Error executing API call (%d): %s" % (response.status,
                                                 response.read())
    sys.exit(2)

#/(uvm.6) Parse and display response
resp_payload = response.read()
if action in ["list", "show"]:
    resp_payload = json.loads(resp_payload)
    
    #/(uvm.7) Process 'list' results
    if action == "list":
        print "Count: %d" % len(resp_payload)
        if res_type == "vhost":
            for vhost in resp_payload:
                print "Vhost: %(name)s" % vhost
        elif res_type == "user":
            for user in resp_payload:
                print "User: %(name)s" % user
                print "\tPassword: %(password_hash)s" % user
                print "\tAdministrator: %(administrator)s\n" % user
    
    #/(uvm.8) Process 'show' results
    elif action == "show":
        if res_type == "vhost":
            print "Vhost: %(name)s" % resp_payload
        elif res_type == "user":
            print "User: %(name)s" % resp_payload
            print "\tPassword: %(password_hash)s" % resp_payload
            print "\tAdministrator: %(administrator)s\n" % resp_payload
        elif res_type == "permission":
            print "Permissions for '%(user)s' in '%(vhost)s'..." % resp_payload
            print "\tRead: %(read)s" % resp_payload
            print "\tWrite: %(write)s" % resp_payload
            print "\tConfig: %(configure)s" % resp_payload
else:
    print "Completed request!"

sys.exit(0)