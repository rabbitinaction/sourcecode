import com.rabbitmq.client.ConnectionFactory;
import com.rabbitmq.client.Connection;
import com.rabbitmq.client.Channel;
import com.rabbitmq.client.QueueingConsumer;
import com.rabbitmq.client.QueueingConsumer.Delivery;
import com.rabbitmq.client.AMQP.BasicProperties;
import org.json.JSONStringer;
import org.json.JSONException;

public class Client {

  private Connection connection;
  private Channel channel;
  private String replyQueueName;
  private QueueingConsumer consumer;

  public Client init()
  throws Exception {
    ConnectionFactory factory = new ConnectionFactory();
    factory.setUsername("rpc_user");
    factory.setPassword("rpcme");
    connection = factory.newConnection();
    channel = connection.createChannel();
    return this;
  }

  public Client setupConsumer()
  throws Exception {
    replyQueueName = channel.queueDeclare().getQueue();
    consumer = new QueueingConsumer(channel);
    channel.basicConsume(replyQueueName, false, consumer);
    return this;
  }

  public String call(String message) throws Exception {
    String response = null;

    channel.basicPublish(
      "rpc",
      "ping",
      getRequestProperties(),
      message.getBytes()
    );

    System.out.println("Sent 'ping' RPC call. Waiting for reply...");

    while (true) {
      Delivery delivery = consumer.nextDelivery();
      response = new String(delivery.getBody(), "UTF-8");
      break;
    }

    return response;
  }

  public void close() throws Exception {
    connection.close();
  }

  private BasicProperties
    getRequestProperties() {
      return new BasicProperties
                .Builder()
                .replyTo(replyQueueName)
                .build();
  }

  public static String createRequest()
  throws JSONException {
    float epoch = System.currentTimeMillis()/1000;
    JSONStringer msg = new JSONStringer();
    return msg
            .object()
            .key("client_name")
            .value("RPC Client 1.0")
            .key("time")
            .value(Float.toString(epoch))
            .endObject().toString();
  }

  public static void main(String[] args) {
    Client client = null;
    String response = null;

    try {
      client = new Client();
      client.init().setupConsumer();
      response = client.call(Client.createRequest());
      System.out.println("RPC Reply --- " + response);
    }
    catch  (Exception e) {
      e.printStackTrace();
    }
    finally {
      if (client!= null) {
        try {
          client.close();
        }
        catch (Exception ignore) {}
      }
    }
  }
}
