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

$conn = new AMQPConnection(HOST, PORT, USER, PASS, VHOST);
	
$channel = $conn->channel();

$channel->exchange_declare('hello-exchange',
					'direct',
					false,
					true,
					false);

$msg = new AMQPMessage($argv[1], 
			array('content_type' => 'text/plain'));

$channel->basic_publish($msg, 'hello-exchange');

$channel->close();
$conn->close();
?>