#!/usr/bin/env python

"""Simple configuration helper"""

__author__ = "Wojciech Nowicki"
__copyright__ = "Copyright 2018, wojciechnowicki.com"
__credits__ = []
__license__ = "GPL"
__version__ = "0.1.0"
__maintainer__ = "Wojciech Nowicki"
__email__ = "contact@wojciechnowicki.com"
__status__ = "Development"

import json


def load(file="config.json"):
    with open(file, 'r') as content_file:
        return json.load(content_file)


if __name__ == "__main__":
    conf = load('config.json')
    print(conf)
