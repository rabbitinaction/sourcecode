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

function add_points_to_user($user_id){
	echo sprintf("Adding points to user: %s\n", $user_id);
}

$consumer = function($msg){
	
	if($msg->body == 'quit'){
		$msg->delivery_info['channel']->
			basic_cancel($msg->delivery_info['consumer_tag']);
	}
	
	$meta = json_decode($msg->body, true);
	
	add_points_to_user($meta['user_id']);
	
	$msg->delivery_info['channel']->
		basic_ack($msg->delivery_info['delivery_tag']);
};

$channel->close();
$conn->close();

?>