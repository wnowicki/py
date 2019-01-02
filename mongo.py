#!/usr/bin/env python

import json
import requests
import configuration
import database
import pymongo
import datetime
import logger

"""Mongo"""

__author__ = "Wojciech Nowicki"
__copyright__ = "Copyright 2018,"
__credits__ = []
__license__ = ""
__version__ = "0.1.0"
__maintainer__ = "Wojciech Nowicki"
__email__ = ""
__status__ = "Development"


def load(file):
    with open(file, 'r') as content_file:
        return json.load(content_file)


def load_from_api(reference, user, password):
    url = '' % reference
    response = requests.post(url, auth=(user, password))

    if response.status_code != 200:
        raise Exception

    return response.json()


class Destination:
    def __init__(self):
        self._db = database.connect()
        self._table = ""

    def insert_rules(self, rules):
        cursor = self._db.cursor()

        query = ""

        cursor.executemany(query, rules)
        self._db.commit()

        return cursor.rowcount

    def fetch_max_date(self):
        cursor = self._db.cursor()
        cursor.execute("SELECT MAX(decision_created_at) AS date FROM %s" % self._table)
        return cursor.fetchall()[0][0]


class Source:
    @staticmethod
    def fetch(date: datetime.datetime, limit=30):
        client = pymongo.MongoClient(conf['mongodb'])
        collection = client.decision_engine.decision_object

        try:
            date.isoformat()
        except Exception:
            date = datetime.datetime(2017, 1, 1)

        return collection.find(
            {"created_at.date": {"$exists": True}, "$and": [{"created_at.date": {"$gte": date.strftime("%Y-%m-%d %H:%M:%S")}}]}) \
            .sort([("created_at.date", 1)]) \
            .skip(0) \
            .limit(limit)


if __name__ == "__main__":

    conf = configuration.load()

    destination = Destination()

    for i in range(30):
        for row in Source.fetch(destination.fetch_max_date(), 100):
            try:
                data = []
                try:
                    res = destination.insert_rules(data)
                    print('%s: %s' % (row['reference'], res))
                    pass
                except Exception as e:
                    print("%s: Writing ERROR: %s" % (row['reference'], e))
            except Exception:
                print('%s: Error' % row['reference'])
                logger.log_error("Parsing error in [%s]" % row['reference'])

        print(destination.fetch_max_date())
        print(i)
