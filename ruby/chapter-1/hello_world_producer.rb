if defined?(Bundler); Bundler.setup; else; require "rubygems"; end

require "amqp"

EventMachine.run do
  AMQP.connect(:host => "localhost", :username => "guest", :password => "guest") do |connection|
    puts "Connected. Hit Control + C to stop me."

    channel  = AMQP::Channel.new(connection)
    channel.direct("hello-exchange", :durable => true, :auto_delete => false).
      publish(ARGV[0], :routing_key => "hola")

    # stop on Control + c or after 1 second
    stop = Proc.new { connection.close { EventMachine.stop } }
    Signal.trap("INT", &stop)
    EventMachine.add_timer(1, &stop)
  end
end