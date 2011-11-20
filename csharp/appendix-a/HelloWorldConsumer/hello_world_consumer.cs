/*##############################################
# RabbitMQ in Action
# Appendix A- Hello World Consumer (.NET)
# 
# Requires: 
#       * RabbitMQ.Client >= 2.7.0
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

            if(args.Length < 1) {
                Console.WriteLine("Must supply hostname.");
                Environment.Exit(-1);
            }
            
            var conn_factory  = new ConnectionFactory();
            
            conn_factory.HostName = args[0];
            conn_factory.UserName = "guest";
            conn_factory.Password = "guest";
            
            ///(hwcdn.1) Establish connection to broker
            IConnection conn = conn_factory.CreateConnection();
            IModel chan = conn.CreateModel(); ///(hwcdn.2) Obtain channel
            
            //(hwcdn.3) Declare the exchange
            chan.ExchangeDeclare("hello-exchange",
                                 ExchangeType.Direct,
                                 true,
                                 false,
                                 null);
            
            ///(hwcdn.4) Declare the queue
            chan.QueueDeclare("hello-queue", 
                              false,
                              false,
                              false,
                              null);
            
            ///(hwcdn.5) Bind the queue and exchange together on the key "hola"
            chan.QueueBind("hello-queue", "hello-exchange", "hola");
            
            ///(hwcdn.6) Subscribe our consumer
            QueueingBasicConsumer consumer = new QueueingBasicConsumer(chan);
            String consumer_tag = chan.BasicConsume("hello-queue", false, consumer);
            
            ///(hwcdn.7) Start consuming
            while(true) {
                ///(hwcdn.8) Process incoming messages
                BasicDeliverEventArgs evt_args = (BasicDeliverEventArgs) consumer.Queue.Dequeue();
                IBasicProperties msg_props = evt_args.BasicProperties;
                
                String msg_body = Encoding.ASCII.GetString(evt_args.Body);
                
                ///(hwcdn.9) Message acknowledgement
                chan.BasicAck(evt_args.DeliveryTag, false);
                
                if(msg_body == "quit") {
                    //(hwc.10) Stop consuming more messages and quit
                    chan.BasicCancel(consumer_tag);
                    break;
                } else
                    Console.WriteLine("Message Body: " + msg_body);
                
            }
            
            Environment.Exit(0);
        }
    }
}