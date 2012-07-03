if defined?(Bundler); Bundler.setup; else; require "rubygems"; end

require "amqp"

EventMachine.run do
  
  AMQP.connect(:host => "localhost", :username => "guest", :password => "guest") do |connection|
    puts "Connected. Waiting for messages... Hit Control + C to stop me."

    channel  = AMQP::Channel.new(connection)
    exchange = channel.direct("hello-exchange", :durable => true, :auto_delete => false)
    channel.queue("hello-queue", :durable => true, :auto_delete => false).bind(exchange, :routing_key => "hola").subscribe do |header, body|
      
      if body == "quit"
        connection.close { EventMachine.stop }
      else
        puts body
      end
    end

    # stop on Control + c
    stop = Proc.new { connection.close { EventMachine.stop } }
    Signal.trap("INT", &stop)
  end
end