#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright (C) 2017 Enrico Bianchi (enrico.bianchi@gmail.com)
# Project       movieindex
# Description   An IMDB movie indexer
# License       GPL version 2 (see GPL.txt for details)
import argparse
import configparser
import logging
import os

import sys

__author__ = "Enrico Bianchi"
__copyright__ = "Copyright 2017, Enrico Bianchi"
__credits__ = ["Enrico Bianchi", ]
__license__ = "GPLv2"
__maintainer__ = "Enrico Bianchi"
__email__ = "enrico.bianchi@gmail.com"
__status__ = "Development"
__version__ = "0.0.0"


def setlog(application, filename, level):
    """
    Set logging parameters
    :param application: Application name
    :param filename: File name to save the log. If not specified, it uses standard error
    :param level: Set log level
    :return: An instance of the logger
    """

    LEVELS = {
        "debug": logging.DEBUG,
        "info": logging.INFO,
        "warning": logging.WARNING,
        "error": logging.ERROR,
        "critical": logging.CRITICAL
    }

    logger = logging.getLogger(application)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    if filename:
        handler = logging.FileHandler(filename=filename)
    else:
        handler = logging.StreamHandler()

    handler.setLevel(LEVELS.get(level.lower(), logging.NOTSET))
    handler.setFormatter(formatter)

    logger.addHandler(handler)

    return logger


def initargs():
    """
    Initialize arguments
    :return: A parser with arguments defined for the application
    """

    parser = argparse.ArgumentParser(description="IMDB movie indexer")
    parser.add_argument("-c", "--cfg", default="movieindex.cfg", help="Set the configuration file")
    parser.add_argument("-T", "--top", help="Retrieve top 250 movies")
    parser.add_argument("-B", "--bottom", help="Retrieve bottom 100 movies")

    return parser


def main():
    """
    Main function
    :return:
    """

    args = initargs().parse_args()
    cfg = configparser.ConfigParser()

    if not os.path.exists(args.cfg):
        logging.basicConfig(format="%(asctime)s - %(levelname)s - %(message)s")
        logging.fatal("Cannot open the configuration file {}: file not found".format(args.cfg))
        sys.exit(1)
    elif not os.path.isfile(args.cfg):
        logging.basicConfig(format="%(asctime)s - %(levelname)s - %(message)s")
        logging.fatal("Cannot open the configuration file {}: is not a file".format(args.cfg))
        sys.exit(1)
    else:
        cfg.read(args.cfg)


if __name__ == '__main__':
    main()
