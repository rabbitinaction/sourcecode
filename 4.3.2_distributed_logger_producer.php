#!/usr/bin/env php
<?php

require_once('../amqp.inc');
include_once('./default_amqp_conf.php');

$exchange = 'logs_exchange';

$conn = new AMQPConnection(HOST, PORT, USER, PASS);
$channel = $conn->channel();
$channel->access_request("/", false, false, true, true);

$msg_body = $argv[1];

$msg = new AMQPMessage($msg_body, array('content_type' => 'text/plain'));
$channel->basic_publish($msg, $exchange);

$channel->close();
$conn->close();
?>