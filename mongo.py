#!/usr/bin/env python

import json
import requests
import configuration
import database
import pymongo
import datetime
import logger

"""Decision object parser"""

__author__ = "Wojciech Nowicki"
__copyright__ = "Copyright 2018, PayBreak.com"
__credits__ = []
__license__ = "PayBreak"
__version__ = "0.1.0"
__maintainer__ = "Wojciech Nowicki"
__email__ = "dev@paybreak.com"
__status__ = "Development"


def load(file):
    with open(file, 'r') as content_file:
        return json.load(content_file)


def load_from_api(reference, user, password):
    url = 'https://api.paybreak.com/merchant-transactions/%s/show-advice' % reference
    response = requests.post(url, auth=(user, password))

    if response.status_code != 200:
        raise Exception

    return response.json()


def parse_decision_object(decision):
    return parse_decision(decision['response'], decision['reference'], decision['created_at']['date'], str(decision['_id']))


def parse_decision(decision, reference, created_at=None, id=None):
    rtn = []
    for k, v in decision['advisers'].items():
        data = parse_adviser(v, k, reference, created_at, id)
        rtn = rtn + data

    return rtn


def parse_adviser(adviser, code, reference, created_at, id):
    rtn = []
    for k, v in adviser['meta'].items():
        if k == k.upper():
            data = parse_scorecard(v, code, reference, created_at, id)
            rtn = rtn + data

    return rtn


def parse_scorecard(scorecard, adviser, reference, created_at, id):
    rtn = []
    for row in scorecard['rules']:
        rtn.append((int(reference), created_at, id, adviser, scorecard['type'], scorecard.get('id', None), row['rule']['source'], row['rule']['active'], row['rule']['description'], row['value']['value'], row['risk']))

    return rtn


class Destination:
    def __init__(self):
        self._db = database.connect()
        self._table = "rules"

    def insert_rules(self, rules):
        cursor = self._db.cursor()

        query = "INSERT INTO  " + self._table + \
                " (reference, decision_created_at, document_id, parent, rule_group, rule_group_version, source, active, rule, value, risk, created_at, updated_at) " \
                "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, NOW(), NOW())"

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

    # reference = 2001984208
    # data = load_from_api(reference, conf['api']['cleo']['user'], conf['api']['cleo']['password'])
    # rules = parse_decision(data, reference)
    # print(insert_rules(rules))

    destination = Destination()

    # print(destination.fetch_max_date().strftime("%Y-%m-%d %H:%M:%S"))
    # exit()

    for i in range(30):
        for row in Source.fetch(destination.fetch_max_date(), 100):
            try:
                data = parse_decision_object(row)
                try:
                    res = destination.insert_rules(data)
                    print('%s: %s' % (row['reference'], res))
                    pass
                except Exception as e:
                    print("%s: Writing ERROR: %s" % (row['reference'], e))
                    # exit()
            except Exception:
                print('%s: Error' % row['reference'])
                logger.log_error("Parsing error in [%s]" % row['reference'])

        print(destination.fetch_max_date())
        print(i)
