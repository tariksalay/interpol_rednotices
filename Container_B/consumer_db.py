"""Consume JSON messages; acknowledge only after the database transaction commits."""
import json
import logging
import os

import pika
import psycopg2
from database import connect

LOGGER = logging.getLogger(__name__)
QUEUE = 'red_notices_queue'
FIELDS = ('Name', 'Age', 'Nationalities')


def decode_notice(body):
    data = json.loads(body)
    if not isinstance(data, dict):
        raise ValueError('Notice must be a JSON object')
    for field in FIELDS:
        if not isinstance(data.get(field), str) or len(data[field]) > 100:
            raise ValueError(f'{field} must be a string of at most 100 characters')
    if not data['Name'].strip():
        raise ValueError('Name must not be empty')
    return tuple(data[field] for field in FIELDS)


def callback(channel, method, properties, body):
    try:
        values = decode_notice(body)
    except (ValueError, UnicodeDecodeError):
        LOGGER.warning('Rejecting invalid notice message')
        channel.basic_nack(delivery_tag=method.delivery_tag, requeue=False)
        return
    connection = None
    try:
        connection = connect()
        with connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    'INSERT INTO interpol_rednotices (name_surname, age, nationality) '
                    'VALUES (%s, %s, %s)', values)
    except psycopg2.Error:
        # Stop the worker after requeueing rather than retrying indefinitely in a hot loop.
        channel.basic_nack(delivery_tag=method.delivery_tag, requeue=True)
        raise
    finally:
        if connection is not None:
            connection.close()
    channel.basic_ack(delivery_tag=method.delivery_tag)


def main():
    connection = pika.BlockingConnection(pika.URLParameters(os.environ['AMQP_URL']))
    try:
        channel = connection.channel()
        channel.queue_declare(queue=QUEUE, durable=True)
        channel.basic_qos(prefetch_count=1)
        channel.basic_consume(queue=QUEUE, on_message_callback=callback, auto_ack=False)
        channel.start_consuming()
    finally:
        connection.close()


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    main()
