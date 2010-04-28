#!/usr/bin/env php
<?php

require_once('../amqp.inc');

define('HOST', 'localhost');
define('PORT', 5672);
define('USER', 'guest');
define('PASS', 'guest');

$exchange = 'hello-exchange';
$queue = 'hello-queue';
$consumer_tag = 'consumer';

$conn = new AMQPConnection(HOST, PORT, USER, PASS);
$ch = $conn->channel();

$ch->access_request("/", false, false, true, true);

$ch->exchange_declare($exchange, 'direct', false, true, false);

$ch->queue_declare($queue);

$ch->queue_bind($queue, $exchange);

$consumer = function($msg) use ($ch, $consumer_tag){

  if ($msg->body === 'quit') {
      $ch->basic_cancel($consumer_tag);
  } else{
    echo 'Hello ',  $msg->body, "\n";
    $ch->basic_ack($msg->delivery_info['delivery_tag']);
  }
};

$ch->basic_consume($queue, $consumer_tag, false, false, false, false, $consumer);

while(count($ch->callbacks)) {
    $ch->wait();
}

$ch->close();
$conn->close();

?>