# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import sys
import json
from optparse import OptionParser

from pubsub import Subscriber


def parse_options():
    """
    Возвращает кортеж опций и аргументов
    :return:
    """
    parser = OptionParser(
        usage='usage: %prog [options] '
    )
    parser.add_option('--host', dest='host', default='localhost',
                      type='string')

    opts, args = parser.parse_args()

    return opts


def _callback(ch, method, properties, body):
    result = json.loads(body)
    print >>sys.stdout, '{} отработал ровно {} часов'.format(
        result['fio'], result['hours'])


def main(callback=_callback):

    options = parse_options()

    with Subscriber(options.host, callback) as sub:
        sub.run()

if __name__ == "__main__":
    main()
