/*##############################################
# RabbitMQ in Action
# Appendix A- Hello World Producer (.NET)
# 
# Requires: 
# 
# Author: Jason J. W. Williams
# (C)2011
##############################################*/

using System;
using System.Text;

using RabbitMQ.Client;
using RabbitMQ.Client.Events;

namespace HelloWorld {
    class Producer {
        
        public static void Main(string[] args) {

            if(args.Length < 2) {
                Console.WriteLine("Must supply hostname and " +
                                  "message text.");
                Environment.Exit(-1);
            }
            
            var conn_factory  = new ConnectionFactory();
            
            conn_factory.HostName = args[0];
            conn_factory.UserName = "guest";
            conn_factory.Password = "guest";
            
            ///(hwpdn.1) Establish connection to broker
            IConnection conn = conn_factory.CreateConnection();
            IModel chan = conn.CreateModel();  ///(hwpdn.2) Obtain channel
            
            ///(hwpdn.3) Declare the exchange
            chan.ExchangeDeclare("hello-exchange",
                                 ExchangeType.Direct,
                                 true,
                                 false,
                                 null);
            
            ///(hwpdn.4) Create a plaintext message
            var msg_body = args[1];
            IBasicProperties msg_props = chan.CreateBasicProperties();
            msg_props.ContentType = "text/plain";
            
            ///(hwpdn.5) Publish the message
            chan.BasicPublish("hello-exchange",
                              "hola",
                              msg_props,
                              Encoding.ASCII.GetBytes(msg_body));
            
            Environment.Exit(0);
        }
    }
}