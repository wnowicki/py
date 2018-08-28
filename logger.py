#!/usr/bin/env python

"""Simple logger"""

__author__ = "Wojciech Nowicki"
__copyright__ = "Copyright 2018, wojciechnowicki.com"
__credits__ = []
__license__ = "GPL"
__version__ = "0.1.0"
__maintainer__ = "Wojciech Nowicki"
__email__ = "contact@wojciechnowicki.com"
__status__ = "Development"

import datetime


def log_error(message):
    file_object = open('log.txt', 'a')
    file_object.write("%s [ERROR] %s \n" % (datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), message))
    file_object.close()


if __name__ == "__main__":

    log_error('test')
