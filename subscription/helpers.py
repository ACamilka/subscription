# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
import sys
import csv

from datetime import datetime
from collections import defaultdict


def get_int_or_none(value):
    try:
        return int(value)
    except ValueError:
        return None


def get_datetime_or_none(value):
    try:
        return datetime.strptime(value, '%H:%M')
    except ValueError:
        return None


class FileParser(object):
    """
    Разбор файла
    """

    def __init__(self, options, filenames):
        self.__filenames = filenames
        self.__period = options['period']
        self.__condition = options['condition']

    @property
    def filenames(self):
        return self.__filenames

    @property
    def period(self):
        return self.__period

    @property
    def condition(self):
        return self.__condition

    def run(self):
        result = defaultdict(lambda: defaultdict(int))
        for filename in self.filenames:
            if not os.path.isfile(filename):
                msg = '{} - doesn\'t exist'.format(filename)
                print >>sys.stderr, msg
                continue
            with open(filename) as f:
                reader = csv.DictReader(f)
                for num, row in enumerate(reader):
                    if len(row.keys()) != 6:
                        msg = '{} - row number {} format error'.format(
                            filename, num
                        )
                        print >>sys.stderr, msg
                        continue

                    # Если суммарное количество превышает self.period -
                    # пропускаем записи с данным id
                    if result[row['id']]['total'] > self.period:
                        continue

                    start = get_datetime_or_none(row['start'])
                    end = get_datetime_or_none(row['end'])
                    hours = get_int_or_none(row['hours'])

                    if not all([start, end, hours]):
                        continue

                    delta = (end - start).seconds/60 ** 2

                    # Проверка след условий:
                    # 1. Начало < конец
                    # 2. конец - Начало < 24
                    # 3. 0 < кол-во часов < 12
                    if 0 < delta < 24 and 0 < hours < 12:
                        result[row['id']]['total'] += delta
                        result[row['id']]['hours'] += hours

                        # Если количество часов соответсвует self.condition -
                        # производится оповещение
                        if result[row['id']]['hours'] == self.condition:
                            yield {'id': row['id'],
                                   'fio': row['fio'],
                                   'hours': self.condition}

