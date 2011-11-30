<?php

require_once('./php-amqplib/amqp.inc');

define('HOST', 'localhost');
define('PORT', 5672);
define('USER', 'guest');
define('PASS', 'guest');

#/(rex.1) Obtain a connection and a channel
$conn = new AMQPConnection(HOST, PORT, USER, PASS);
$channel = $conn->channel();

#/(rex.2) Declare the exchnage
$channel->exchange_declare('logs-exchange',
  'topic', false, true, false);

#/(rex.3) Declare the queues
$channel->queue_declare('msg-inbox-errors',
  false, true, false, false);

$channel->queue_declare('msg-inbox-logs',
  false, true, false, false);

$channel->queue_declare('all-logs', false,
  true, false, false);

#/(rex.4) Bind the queues to the exchange
$channel->queue_bind('msg-inbox-errors',
  'logs-exchange', 'error.msg-inbox');

$channel->queue_bind('msg-inbox-logs',
  'logs-exchange', '*.msg-inbox');
?>