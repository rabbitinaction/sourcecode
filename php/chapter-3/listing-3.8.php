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
require_once('../config/config.php');

$conn = new AMQPConnection(HOST, PORT, USER, PASS, VHOST);
$channel = $conn->channel();

$channel->exchange_declare('upload-pictures', 
	'fanout', false, true, false);

$channel->queue_declare('add-points', 
	false, true, false, false);

$channel->queue_bind('add-points', 'upload-pictures');

$consumer = function($msg){};

$channel->basic_consume($queue,
						$consumer_tag,
						false,
						false,
						false,
						false,
						$consumer);
						
$channel->close();
$conn->close();

?>
