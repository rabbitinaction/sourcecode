#!/usr/bin/env php
<?php

require_once('../amqp.inc');

define('HOST', 'localhost');
define('PORT', 5672);
define('USER', 'guest');
define('PASS', 'guest');

$exchange = 'hello-exchange';

$conn = new AMQPConnection(HOST, PORT, USER, PASS);
$ch = $conn->channel();

$ch->access_request("/", false, false, true, true);

$ch->exchange_declare($exchange, 'direct', false, true, false);

$msg = new AMQPMessage($argv[1], array('content_type' => 'text/plain'));
$ch->basic_publish($msg, 'hello-exchange');

$ch->close();
$conn->close();
?>
