# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
import pika


DEFAULT_EXCHANGE = 'worked_hours'

class Publisher(object):
    """Класс осуществяющий рассылку сообщений
    """

    def __init__(self, host, exchange=DEFAULT_EXCHANGE):
        self.__host = host
        self.__exchange = exchange

    def __enter__(self):

        self.__connection = pika.BlockingConnection(
            pika.ConnectionParameters(self.__host)
        )
        self.__channel = self.__connection.channel()
        self.__channel.exchange_declare(
            exchange=self.__exchange,
            type='fanout')
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.__connection.close()

    def publish(self, data):
        self.__channel.basic_publish(
            exchange=self.__exchange,
            routing_key='',
            body=json.dumps(data)
        )


class Subscriber(object):
    """Класс подписчик
    """

    def __init__(self, host, callback, exchange=DEFAULT_EXCHANGE):
        self.__host = host
        self.__exchange = exchange
        self.__callback = callback

    def __enter__(self):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(self.__host)
        )
        self.channel = self.connection.channel()

        self.channel.exchange_declare(
            exchange=self.__exchange,
            type='fanout')

        result = self.channel.queue_declare(exclusive=True)
        queue_name = result.method.queue

        self.channel.queue_bind(
            exchange=self.__exchange,
            queue=queue_name)

        self.channel.basic_consume(
            self.__callback,
            queue=queue_name,
            no_ack=True)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.close()

    def run(self):
        self.channel.start_consuming()
