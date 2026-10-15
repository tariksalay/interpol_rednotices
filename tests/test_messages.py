import json
from pathlib import Path
from types import SimpleNamespace
import sys
import unittest
from unittest.mock import MagicMock, patch
sys.path[:0] = [str(Path(__file__).resolve().parents[1] / folder)
               for folder in ('Container_A', 'Container_B')]
import consumer_db as consumer
import scraper_producer as producer
import webapp
import psycopg2

NOTICE = {'Name': 'Synthetic example', 'Age': '30', 'Nationalities': 'Example'}


class MessageTests(unittest.TestCase):
    def test_only_valid_json_objects_are_accepted(self):
        self.assertEqual(consumer.decode_notice(json.dumps(NOTICE)), tuple(NOTICE.values()))
        for body in ("__import__('os').system('echo unsafe')", '[]', '{}', 'null',
                     json.dumps({**NOTICE, 'Name': ''}), json.dumps({**NOTICE, 'Age': 123}),
                     json.dumps({**NOTICE, 'Name': 'a' * 101})):
            with self.assertRaises(ValueError):
                consumer.decode_notice(body)

    def test_commit_precedes_ack_and_connection_closes(self):
        events = []
        connection = MagicMock()
        connection.__exit__.side_effect = lambda *args: events.append('commit')
        channel = MagicMock()
        channel.basic_ack.side_effect = lambda **kwargs: events.append('ack')
        with patch.object(consumer, 'connect', return_value=connection):
            consumer.callback(channel, SimpleNamespace(delivery_tag=42), None, json.dumps(NOTICE))
        self.assertEqual(events, ['commit', 'ack'])
        connection.close.assert_called_once()
        channel.basic_ack.assert_called_once_with(delivery_tag=42)

    def test_database_failure_requeues_without_ack(self):
        channel = MagicMock()
        with patch.object(consumer, 'connect', side_effect=psycopg2.OperationalError):
            with self.assertRaises(psycopg2.OperationalError):
                consumer.callback(channel, SimpleNamespace(delivery_tag=7), None, json.dumps(NOTICE))
        channel.basic_nack.assert_called_once_with(delivery_tag=7, requeue=True)
        channel.basic_ack.assert_not_called()

    def test_bad_message_never_opens_database(self):
        channel = MagicMock()
        with patch.object(consumer, 'connect') as connect:
            consumer.callback(channel, SimpleNamespace(delivery_tag=8), None, b'not json')
        connect.assert_not_called()
        channel.basic_nack.assert_called_once_with(delivery_tag=8, requeue=False)

    def test_publisher_uses_json_and_closes_connection(self):
        connection = MagicMock()
        with patch.dict('os.environ', {'AMQP_URL': 'amqp://localhost'}), \
             patch.object(producer.pika, 'BlockingConnection', return_value=connection):
            producer.send_to_rabbitmq([NOTICE])
        kwargs = connection.channel.return_value.basic_publish.call_args.kwargs
        self.assertEqual(json.loads(kwargs['body']), NOTICE)
        self.assertTrue(kwargs['mandatory'])
        connection.close.assert_called_once()

    def test_web_request_reads_rows_and_closes_connection(self):
        connection = MagicMock()
        connection.cursor.return_value.__enter__.return_value.fetchall.return_value = [
            (1, '<script>not executable</script>', '30', 'Example')]
        with patch.object(webapp, 'connect', return_value=connection):
            response = webapp.webapp.test_client().get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'&lt;script&gt;', response.data)
        connection.close.assert_called_once()


if __name__ == '__main__':
    unittest.main()
