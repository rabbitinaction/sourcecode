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
	
$channel->queue_declare('resize-picture', 
	false, true, false, false);
	
$channel->queue_bind('resize-picture', 'upload-pictures');

$consumer = function($msg){
	
	if($msg->body == 'quit'){
		$msg->delivery_info['channel']->
			basic_cancel($msg->delivery_info['consumer_tag']);
	}

	$meta = json_decode($msg->body, true);

	resize_picture($meta['image_id'], $meta['image_path']);

	$msg->delivery_info['channel']->
		basic_ack($msg->delivery_info['delivery_tag']);
};

function resize_picture($image_id, $image_path){
	echo sprintf("Resizing picture: %s %s\n",
	 	$image_id, $image_path);
}

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