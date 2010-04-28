#!/usr/bin/env php
<?php

require_once('../amqp.inc');
include_once('./default_amqp_conf.php');

$exchange = 'logs_exchange';
$consumer_tag = 'consumer';

$routing_key = isset($argv[1]) ? $argv[1] : '#';

echo $routing_key, "\n";

$conn = new AMQPConnection(HOST, PORT, USER, PASS);
$ch = $conn->channel();
$ch->access_request("/", false, false, true, true);

list($queue) = $ch->queue_declare();

echo $queue, "\n";

$ch->exchange_declare($exchange, 'topic', false, true, false);
$ch->queue_bind($queue, $exchange, $routing_key);

$consumer = function($msg) use ($ch, $consumer_tag){
  echo "\n--------\n";
  echo $msg->body;
  echo "\n--------\n";

  $ch->basic_ack($msg->delivery_info['delivery_tag']);
};

$shutdown = function($ch, $conn){
  $ch->basic_cancel($consumer_tag);
  $ch->close();
  $conn->close();
};

register_shutdown_function($shutdown, $ch, $conn);

$ch->basic_consume($queue, $consumer_tag, false, false, false, false, $consumer);

while(count($ch->callbacks)) {
    $ch->wait();
}
?>