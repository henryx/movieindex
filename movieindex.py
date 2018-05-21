#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright (C) 2017 Enrico Bianchi (enrico.bianchi@gmail.com)
# Project       movieindex
# Description   An IMDB movie indexer
# License       GPL version 2 (see GPL.txt for details)
import argparse

__author__ = "Enrico Bianchi"
__copyright__ = "Copyright 2017, Enrico Bianchi"
__credits__ = ["Enrico Bianchi", ]
__license__ = "GPLv2"
__maintainer__ = "Enrico Bianchi"
__email__ = "enrico.bianchi@gmail.com"
__status__ = "Development"
__version__ = "0.0.0"


def initargs():
    """
    Initialize arguments
    :return: A parser with arguments defined for the application
    """

    parser = argparse.ArgumentParser(description="IMDB movie indexer")
    parser.add_argument("-c", "--cfg", help="Set the configuration file")
    parser.add_argument("-T", "--top", help="Retrieve top 250 movies")
    parser.add_argument("-B", "--bottom", help="Retrieve bottom 100 movies")

    return parser


def main():
    """
    Main function
    :return:
    """
    args = initargs().parse_args()


if __name__ == '__main__':
    main()
