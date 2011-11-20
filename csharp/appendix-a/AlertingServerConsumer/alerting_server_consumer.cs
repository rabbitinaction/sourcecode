/*##############################################
# RabbitMQ in Action
# Appendix A- Alerting Server Consumer (.NET)
# 
# Requires: 
# 
# Author: Jason J. W. Williams
# (C)2011
##############################################*/

using System;
using System.Text;
using System.Net.Mail;

using Newtonsoft.Json;

using RabbitMQ.Client;
using RabbitMQ.Client.Events;

namespace AlertingServer {
    class Consumer {
        
        private static void send_mail(string[] recipients,
                                      string subject,
                                      string message) {
            
            MailMessage msg = new MailMessage();
            msg.From = new MailAddress("alerts@ourcompany.com");
            
            foreach(string recip in recipients)
                msg.To.Add(recip);
            
            msg.Subject = subject;
            msg.Body = message;
            
            SmtpClient smtp_server = new SmtpClient("mail.ourcompany.com");
            smtp_server.Port = 25;
            smtp_server.Send(msg);
        }
        
        private static void critical_notify(IBasicConsumer consumer,
                                            BasicDeliverEventArgs evt_args) {
            
            string[] EMAIL_RECIPS = new string[] {"ops.team@ourcompany.com"};
            
            IBasicProperties msg_props = evt_args.BasicProperties;
            String msg_body = Encoding.ASCII.GetString(evt_args.Body);
            
            ///(ascdn.6) Decode our message from JSON    
            msg_body = JsonConvert.DeserializeObject<string>(msg_body);
            
            ///(ascdn.7) Transmit e-mail to SMTP server
            send_mail(EMAIL_RECIPS, "CRITICAL ALERT", msg_body);
            
            Console.WriteLine("Sent alert via e-mail! Alert Text: " +
                              msg_body + " Recipients: " +
                              string.Join(",", EMAIL_RECIPS));
            
            ///(ascdn.8) Acknowledge the message
            consumer.Model.BasicAck(evt_args.DeliveryTag, false);
        }
        
        private static void rate_limit_notify(IBasicConsumer consumer,
                                              BasicDeliverEventArgs evt_args) {
            
            string[] EMAIL_RECIPS = new string[] {"api.team@ourcompany.com"};
            
            IBasicProperties msg_props = evt_args.BasicProperties;
            String msg_body = Encoding.ASCII.GetString(evt_args.Body);
            
            ///(ascdn.9) Decode our message from JSON
            msg_body = JsonConvert.DeserializeObject<string>(msg_body);
            
            ///(ascdn.10) Transmit e-mail to SMTP server
            send_mail(EMAIL_RECIPS, "RATE LIMIT ALERT!", msg_body);
            
            Console.WriteLine("Sent alert via e-mail! Alert Text: " +
                              msg_body + " Recipients: " +
                              string.Join(",", EMAIL_RECIPS));
            
            ///(ascdn.11) Acknowledge the message
            consumer.Model.BasicAck(evt_args.DeliveryTag, false);
        }
        
        public static void Main(string[] args) {
            if(args.Length < 1) {
                Console.WriteLine("Must supply hostname.");
                Environment.Exit(-1);
            }
            
            var conn_factory  = new ConnectionFactory();
            
            conn_factory.HostName = args[0];
            conn_factory.UserName = "alert_user";
            conn_factory.Password = "alertme";
            
            ///(ascdn.1) Establish connection to broker
            IConnection conn = conn_factory.CreateConnection();
            IModel chan = conn.CreateModel(); ///(hwcdn.2) Obtain channel
            
            ///(ascdn.2) Declare the Exchange
            chan.ExchangeDeclare("alerts",
                                 ExchangeType.Topic,
                                 true,
                                 false,
                                 null);
            
            //(ascdn.3) Build the queues and bindings for our topics 
            chan.QueueDeclare("critical", 
                              false,
                              false,
                              false,
                              null);
            
            chan.QueueBind("critical", "alerts", "critical.*");
            
            chan.QueueDeclare("rate_limit", 
                              false,
                              false,
                              false,
                              null);
            
            chan.QueueBind("rate_limit", "alerts", "*.rate_limit");
            
            //(ascdn.4) Make our alert processors
            EventingBasicConsumer
                c_consumer = new EventingBasicConsumer {Model = chan};
            c_consumer.Received += critical_notify;
            chan.BasicConsume("critical",
                              false,
                              c_consumer);
            
            
            EventingBasicConsumer
                 r_consumer = new EventingBasicConsumer {Model = chan};
            r_consumer.Received += rate_limit_notify;
            chan.BasicConsume("rate_limit",
                              false,
                              r_consumer);
            
        }
    }
}