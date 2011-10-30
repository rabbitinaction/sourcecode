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

$exchange = 'rh-exchange';

$conn = new AMQPConnection(HOST, PORT, USER, PASS, VHOST);
$ch = $conn->channel();

$ch->exchange_declare($exchange,
        'x-recent-history',
        false,
        true,
        false);

list($queue,,) = $ch->queue_declare('');

$ch->queue_bind($queue, $exchange);

$consumer = function($msg){
    echo $msg->body, "\t";
};

$ch->basic_consume(
        $queue,
        '',
        false,
        true,
        false,
        false,
        $consumer);

echo "consuming from queue: ", $queue, "\n";

function shutdown($conn, $ch){
  $ch->close();
  $conn->close();
}

register_shutdown_function('shutdown', $conn, $ch);

while(count($ch->callbacks)) {
    $ch->wait();
}
?>