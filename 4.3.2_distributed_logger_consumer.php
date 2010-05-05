#!/usr/bin/env php
<?php


require_once('../amqp.inc');
include_once('./default_amqp_conf.php');

$exchange = 'logs_exchange';

$callback_function = isset($argv[1]) ? $argv[1] : 'screen_logger';
$consumer_tag = isset($argv[2]) ? $argv[2] : 'consumer';

$conn = new AMQPConnection(HOST, PORT, USER, PASS);
$channel = $conn->channel();
$channel->access_request("/", false, false, true, true);

list($queue) = $channel->queue_declare();

echo $queue, "\n";

$channel->exchange_declare($exchange, 'fanout', false, true, false);
$channel->queue_bind($queue, $exchange);

$file_logger = function($msg) use ($channel, $consumer_tag){
  $cmd = sprintf('echo "%s" >> /tmp/%s.log' , $msg->body, $consumer_tag);
  echo "Executing command: ", $cmd, "\n";
  exec($cmd);
  $channel->basic_ack($msg->delivery_info['delivery_tag']);
};

$screen_logger = function($msg) use ($channel, $consumer_tag){
  echo $msg->body, "\n";
  $channel->basic_ack($msg->delivery_info['delivery_tag']);
};

$shutdown = function($channel, $conn) use ($consumer_tag){
  $channel->basic_cancel($consumer_tag);
  $channel->close();
  $conn->close();
};

register_shutdown_function($shutdown, $channel, $conn);

$channel->basic_consume($queue, $consumer_tag, false, false, false, false, $$callback_function);

while(count($channel->callbacks)) {
    $channel->wait();
}
?>