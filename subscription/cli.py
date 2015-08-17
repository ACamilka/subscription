# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import sys
from optparse import OptionParser

from helpers import FileParser
from pubsub import Publisher


def parse_options(args):
    """
    Возвращает кортеж опций и аргументов
    :param args:
    :return:
    """
    parser = OptionParser(
        usage='usage: %prog [options] [path1 [path2 [... pathN]]] '
    )
    parser.add_option('-p', '--period', dest='period', default=40, type='int')
    parser.add_option('-c', '--condition', dest='condition', default=15,
                      type='int')
    parser.add_option('--host', dest='host', default='localhost',
                      type='string')

    opts, args = parser.parse_args(args)

    # Указание хотя бы одного файла обязательно
    if not len(args):
        print >>sys.stderr, parser.print_help()
        sys.exit()

    return opts, args


def main(args, config):
    options, filenames = parse_options(args)

    assert 'publisher_class' in config
    Publisher = config['publisher_class']

    parser = FileParser(options.__dict__, filenames)
    with Publisher(options.host) as pub:
        for row in parser.run():
            pub.publish(row)


if __name__ == "__main__":
    args = sys.argv[1:]
    config = {
        'publisher_class': Publisher
    }
    main(args, config)
