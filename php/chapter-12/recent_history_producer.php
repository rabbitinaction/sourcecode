<?php
###############################################
# RabbitMQ in Action
#
# Requires: php-amqplib
#
# Author: Alvaro Videla
# (C) 2011
###############################################
require_once('../lib/php-amqplib/amqp.inc');

define('HOST', 'localhost');
define('PORT', 5672);
define('USER', 'guest');
define('PASS', 'guest');
define('VHOST', '/');

$conn = new AMQPConnection(HOST, PORT, USER, PASS, VHOST);

$channel = $conn->channel();

for($i=0; $i<100; $i++) {
  $msg = new AMQPMessage('msg_'.$i,
        array('content_type' => 'text/plain'));
  $channel->basic_publish($msg, 'rh-exchange');
}

$channel->close();
$conn->close();
?>