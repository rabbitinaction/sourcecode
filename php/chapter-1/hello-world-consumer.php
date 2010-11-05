<?php
###############################################
# RabbitMQ in Action
# 
# Requires: php-amqplib
# 
# Author: Alvaro Videla
# (C)2010
###############################################
require_once('../lib/php-amqplib/amqp.inc');

define('HOST', 'localhost');
define('PORT', 5672);
define('USER', 'guest');
define('PASS', 'guest');
define('VHOST', '/');

$exchange = 'hello-exchange';
$queue = 'hello-queue';
$consumer_tag = 'consumer';

$conn = new AMQPConnection(HOST, PORT, USER, PASS, VHOST);
$channel = $conn->channel();

$channel->exchange_declare($exchange,
         'direct',
         false,
         true,
         false);

$channel->queue_declare($queue);

$channel->queue_bind($queue, $exchange);

$consumer = function($msg){
  $msg->delivery_info['channel']->basic_ack($msg->delivery_info['delivery_tag']);
  
  if($msg->body == 'quit'){
    $msg->delivery_info['channel']->basic_cancel($msg->delivery_info['consumer_tag']);
  }else{
    echo 'Hello ',  $msg->body, "\n";
  }
};

$channel->basic_consume($queue,
  $consumer_tag,
  false,
  false,
  false,
  false,
  $consumer);

while(count($channel->callbacks)) {
    $channel->wait();
}

$channel->close();
$conn->close();

?>