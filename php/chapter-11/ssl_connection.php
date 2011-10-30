<?php

require_once(__DIR__ . '/../amqp.inc');

define('HOST', 'localhost');
define('PORT', 5671);
define('USER', 'guest');
define('PASS', 'guest');
define('VHOST', '/');
define('AMQP_DEBUG', true);

define('CERTS_PATH',
  '/path/to/ca/folder/');

$ssl_options = array(
      'cafile' => CERTS_PATH . '/rmqca/cacert.pem',
      'local_cert' => CERTS_PATH . '/phpcert.pem',
      'verify_peer' => true
  );

$conn = new AMQPSSLConnection(HOST, PORT, USER, PASS, VHOST, $ssl_options);

function shutdown($conn){
    $conn->close();
}

register_shutdown_function('shutdown', $conn);

while(1){}