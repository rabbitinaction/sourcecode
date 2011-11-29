/*##############################################
# RabbitMQ in Action
# Appendix A- Alerting Server Producer (.NET)
# 
# Requires: 
#       * RabbitMQ.Client >= 2.7.0
#       * Newtonsoft.Json >= 4.0 
# 
# Author: Jason J. W. Williams
# (C)2011
##############################################*/

using System;
using System.Text;

using Newtonsoft.Json;

using RabbitMQ.Client;
using RabbitMQ.Client.Events;

namespace AlertingServer {
    
    class Producer {
        
        public static void Main(string[] args) {
            if(args.Length < 3) {
                Console.WriteLine("Must supply hostname, routing key, " +
                                  "and alert message.");
                Environment.Exit(-1);
            }
            
            var conn_factory  = new ConnectionFactory();
            
            conn_factory.HostName = args[0];
            conn_factory.UserName = "alert_user";
            conn_factory.Password = "alertme";
            
            //#/(aspdn.1) Establish connection to broker
            IConnection conn = conn_factory.CreateConnection();
            IModel chan = conn.CreateModel(); //#/(hwcdn.2) Obtain channel
            
            //#/(aspdn.2) Publish alert message to broker
            string msg = JsonConvert.SerializeObject(args[2]);
            IBasicProperties msg_props = chan.CreateBasicProperties();
            msg_props.ContentType = "application/json";
            msg_props.DeliveryMode = 2;
            chan.BasicPublish("alerts",
                              args[1],
                              msg_props,
                              Encoding.ASCII.GetBytes(msg));
            
            Console.WriteLine("Sent message " + args[2] + 
                              " tagged with routing key " + args[1] +
                              " to exchange 'alerts'.");
            
            Environment.Exit(0);
        }
    }
}