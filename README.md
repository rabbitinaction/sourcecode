# RabbitMQ in Action Examples #


## Requirements ##

### Python Examples ###

* Python 2.6 or newer
* [Pika](https://github.com/tonyg/pika)

### PHP Examples ###
* The examples where tested with PHP 5.3
* [php-amqplib](http://github.com/tnc/php-amqplib)

### Ruby Examples ###
* Ruby 1.8.7 or 1.9.2. JRuby and Rubinius are supported.
* [amqp gem](http://github.com/ruby-amqp/amqp) 0.8.0.RC12 or later. See [Getting Started Guide](http://bit.ly/jcuACj) for installation instructions.

## Running the Examples: Python ##

### 3.2.2 Alerting Framework ###

_Requirements:_

* RabbitMQ server (2.0 or later) running on localhost.
* RabbitMQ user needed:
	* Username: alert\_user
	* Password: alertme
	* Permissions: read,write,config

_Running the Consumer:_  __python 3.2.2\_alert\_consumer.py__

_Running the Producer:_ __python 3.2.2\_alert\_producer.py -r ROUTING\_KEY -m MESSAGE__


### 3.3.3 RPC Example ###

_Requirements:_

* RabbitMQ server (2.0 or later) running on localhost.
* RabbitMQ user needed:
	* Username: rpc\_user
	* Password: rpcme
	* Permissions: read,write,config


_Running the Server:_ __python 3.3.3\_rpc\_server.py__
_Running the Client:_ __python 3.3.3\_rpc\_server.py__

## Running the Examples: PHP ##

* RabbitMQ server (2.0 or later) running on localhost.
* RabbitMQ user needed:
	* Username: guest
	* Password: guest

To run the PHP scripts simply do:

		php script_name.php

$$ Running the Examples: Ruby ##

* RabbitMQ server (2.0 or later) running on localhost.
* RabbitMQ user needed:
	* Username: guest
	* Password: guest

To run examples do

    ruby chapter-1/hello_world_consumer.rb

and so on. Or, if you use Bundler

    bundle exec chapter-1/hello_world_consumer.rb