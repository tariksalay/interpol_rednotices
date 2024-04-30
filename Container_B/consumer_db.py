# import RabbitMQ
import pika

# import Postgresql
import psycopg2

# to loop through everyone
i = 0


# https://www.postgresql.org/docs/current/libpq-connect.html
# 34.1. Database Connection Control Functions

# Consume messages and push it to the DB
def callback(ch, method, properties, body):
    print(f"New message has been pushed:\n{body}\n")

    # to get i out of loop
    global i

    # Convert message body to a dictionary
    data = eval(body)
    name = data.get("Name")
    age = data.get("Age")
    nationality = data.get("Nationalities")

    i += 1

    if i == (queue.method.message_count):
        ch.stop_consuming()  # Stop consuming messages after processing 20

    # Insert data into Postgresql database
    pg_cursor.execute("INSERT INTO interpol_rednotices (name_surname, age, nationality) VALUES (%s, %s, %s);",
                      (name, age, nationality))
    connection.commit()


# Establish the connection
connection = psycopg2.connect(
    dbname="postgres_db",
    user="postgres",
    password="postgres",
    host="localhost",
    port="5432"
)

# Create a cursor for executing SQL commands
pg_cursor = connection.cursor()

# Create 'interpol_rednotices.db' table if it doesn't exist
pg_cursor.execute("CREATE TABLE IF NOT EXISTS interpol_rednotices (ID SERIAL PRIMARY KEY, name_surname VARCHAR(100), "
                  "age VARCHAR(100), nationality VARCHAR(100));")
connection.commit()

# Copy the same lines from producer to declare the same connection
connection_parameters = pika.ConnectionParameters('172.17.0.2')
# connection_parameters = pika.ConnectionParameters('localhost')
rabbitmq_connection = pika.BlockingConnection(connection_parameters)
channel = rabbitmq_connection.channel()  # creates the channel

# it's ok to declare the queue with the same name, broker will know
# wherever the code executes first will declare the queue while the other one is ignored
# durable=True for Docker
# queue = channel.queue_declare(queue='red_notices_queue')

# to use later for stopping consume
queue = channel.queue_declare(queue='red_notices_queue', durable=True)
# channel.queue_declare(queue='red_notices_queue')
channel.queue_declare(queue='red_notices_queue', durable=True)


# to consume of the queue
channel.basic_consume(queue='red_notices_queue', on_message_callback=callback, auto_ack=True)

print("Starting consuming!\n")
channel.start_consuming()

# Return if any pending messages
requeued_messages = channel.cancel()
print('%i Pending messages\n' % requeued_messages)

if requeued_messages == 0:
    print("Consumed all successfully!\n")

    # Close the channel and the connection
    channel.close()

    # Close rabbitmq connection
    rabbitmq_connection.close()

    # Close cursor
    pg_cursor.close()

    # Close DB
    connection.close()

    print("DB and AMQP connections are closed")
