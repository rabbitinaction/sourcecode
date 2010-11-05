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

$metadata = json_encode(array(
	'image_id' => $argv[1],
	'user_id' => $argv[2],
	'image_path' => $argv[3]
	));

$msg = new AMQPMessage($metadata, array(
	'content_type' => 'application/json', 
	'delivery_mode' => 2));

$channel->basic_publish($msg, 'upload-pictures');

$channel->close();
$conn->close();
?>