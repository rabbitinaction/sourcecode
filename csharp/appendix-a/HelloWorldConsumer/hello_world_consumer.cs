/*##############################################
# RabbitMQ in Action
# Appendix A- Hello World Consumer (.NET)
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
    class Consumer {
        
        public static void Main(string[] args) {
            
            var conn_factory  = new ConnectionFactory();
            
            // Validate hostname was passed in
            if(args.Length < 1) {
                Console.WriteLine("Must supply hostname.");
                Environment.Exit(-1);
            }
            
            conn_factory.HostName = args[0];
            conn_factory.UserName = "guest";
            conn_factory.Password = "guest";
            
            IConnection conn = conn_factory.CreateConnection();
            IModel chan = conn.CreateModel();
            
            chan.QueueDeclare("hello-queue", false, false, false, null);
            chan.ExchangeDeclare("hello-exchange", ExchangeType.Direct, true, false, null);
            chan.QueueBind("hello-queue", "hello-exchange", "hola");
            
            QueueingBasicConsumer consumer = new QueueingBasicConsumer(chan);
            String consumer_tag = chan.BasicConsume("hello-queue", false, consumer);
            
            while(true) {
                BasicDeliverEventArgs evt_args = (BasicDeliverEventArgs) consumer.Queue.Dequeue();
                IBasicProperties msg_props = evt_args.BasicProperties;
                
                String msg_body = Encoding.ASCII.GetString(evt_args.Body);
                
                chan.BasicAck(evt_args.DeliveryTag, false);
                
                if(msg_body == "quit") {
                    chan.BasicCancel(consumer_tag);
                    break;
                } else
                    Console.WriteLine("Message Body: " + msg_body);
                
            }
            
            Environment.Exit(0);
        }
    }
}