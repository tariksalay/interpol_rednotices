# Push red notices list to rabbitmq queue

import pika  # needed for rabbitmq


def send_to_rabbitmq(message):
    # Connect to Container C (RabbitMQ queue)
    connection_parameters = pika.ConnectionParameters('localhost')
    connection = pika.BlockingConnection(connection_parameters)
    channel = connection.channel()  # creates the channel

    # # Set the connection parameters to connect to rabbit-server1 on port 5672
    # # on the / virtual host using the username "guest" and password "guest"
    # credentials = pika.PlainCredentials('guest', 'guest')
    # should i say docker instead of rabbitserver1? or something else
    # parameters = pika.ConnectionParameters('rabbit-server1',
    #                                        5672,
    #                                        '/',
    #                                        credentials)

    # Declare a queue along with its name
    # Durable = true to make the queue survive a broker restart
    # channel.queue_declare(queue='red_notices_queue', durable=True)
    channel.queue_declare(queue='red_notices_queue')

    # publish each item of data to the Container_C queue
    # message is the function parameter here, list of red notice people
    # basic_publish method pushes each person's data down to the queue
    for i in message:
        channel.basic_publish(exchange='',
                              routing_key='red_notices_queue',
                              body=str(i),
                              properties=pika.BasicProperties(
                                  delivery_mode=2,
                              ))

    print(f"Sent the updated list of Red Notices as: \n{message}")

    # to not leave connection hanging
    # connection/channel will be closed, but the queue will have the message stored
    connection.close()
