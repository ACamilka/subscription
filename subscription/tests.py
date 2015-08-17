# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
import tempfile
import time
import threading
import unittest

from faker import Faker

from helpers import FileParser
import cli
import pubsub
import worker


class BaseFixtureTestCase(unittest.TestCase):
    """
    Базовый класс тестов
    """

    def setUp(self):
        self._id = '1'
        # Создание тестовых данных
        faker = Faker()
        data = [
            ['id', 'fio', 'contact', 'start', 'end', 'hours'],
            [self._id, faker.first_name(), faker.phone_number(), '9:00', '18:00', '7'],
            ['2', faker.first_name(), faker.phone_number(), '9:00', '18:00', '5'],
            [self._id, faker.first_name(), faker.phone_number(), '9:00', '18:00', '8']
        ]
        self.temp = tempfile.NamedTemporaryFile()
        self.temp.file.write('\n'.join([','.join(d) for d in data]))
        self.temp.file.close()

    def tearDown(self):
        if not self.temp.delete:
            self.temp.unlink()


class FileParserTestCase(BaseFixtureTestCase):
    """
    Тест для класса helpers.FileParser
    """
    def test_file_parse(self):
        options = {'period': 40, 'condition': 15}
        parser = FileParser(options, [self.temp.name])
        result = [i for i in parser.run()]

        self.assertEqual(len(result), 1)


class PublisherTestCase(BaseFixtureTestCase):
    """
    Тест для cli.main
    """
    def test_cli(self):
        class Publisher(object):
            result = None

            def __init__(self, host):
                pass

            def __enter__(self):
                return self

            def __exit__(self, exc_type, exc_val, exc_tb):
                pass

            def publish(self, data):
                Publisher.result = data

        config = {
            'publisher_class': Publisher
        }

        cli.main([self.temp.name], config)

        self.assertEqual(Publisher.result['id'], self._id)


class SubscriberTestCase(BaseFixtureTestCase):
    """
    Тест для worker.main
    """
    def test_worker(self):
        self.result = None

        def callback(ch, method, properties, body):
            self.result = json.loads(body)

        thread = threading.Thread(target=worker.main, args=[callback])
        thread.daemon = True
        thread.start()

        config = {
            'publisher_class': pubsub.Publisher
        }
        while self.result is None:
            time.sleep(1)
            cli.main([self.temp.name], config)

        self.assertEqual(self.result['id'], self._id)


if __name__ == '__main__':
    unittest.main()
