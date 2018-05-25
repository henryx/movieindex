#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright (C) 2018 Enrico Bianchi (enrico.bianchi@gmail.com)
# Project       movieindex
# Description   An IMDB movie indexer
# License       GPL version 2 (see LICENSE for details)
import argparse
import configparser
import logging

import imdb

import movieindex

__author__ = "Enrico Bianchi"
__copyright__ = "Copyright 2018, Enrico Bianchi"
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
    logger.setLevel(LEVELS.get(level.lower(), logging.NOTSET))
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

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
    parser.add_argument("-T", "--top", action="store_true", default=False, help="Retrieve top 250 movies")
    parser.add_argument("-B", "--bottom", action="store_true", default=False, help="Retrieve bottom 100 movies")

    return parser


def fetch(logger, top, bottom):
    """
    Retrieve data from IMDB
    :param logger: A logger for registering operations
    :param top: Fetch top 250 movies
    :param bottom: Fetch bottom 100 movies
    :return: Data fetched
    """

    ia = imdb.IMDb()
    fetched = []

    if not top and not bottom:
        logger.debug("No dataset selected")
        raise ValueError("No dataset selected")

    if top:
        logger.debug("Fetch top 250 movies")
        fetched += ia.get_top250_movies()

    if bottom:
        logger.debug("Fetch bottom 100 movies")
        fetched += ia.get_bottom100_movies()

    return fetched


def store_to_es(logger, cfgsection, movie):
    """
    Store data movie to Elasticsearch
    :param logger: A logger for registering operations
    :param cfgsection: Configuration section
    :param movie: Movie
    :return:
    """


def store_to_mongo(logger, cfgsection, movie):
    """
    Stora data movie to MongoDB
    :param logger: A logger for registering operations
    :param cfgsection: Configuration section
    :param movie: Movie
    :return:
    """

    with movieindex.store.MongoDB(cfgsection) as db:
        db.store(movie)


def save(logger, cfg, movies):
    """
    Save data to storage
    :param logger: A logger for registering operations
    :param cfg: Configuration data
    :param movies: A list containing fetched IMDB movies
    :return:
    """

    # FIXME: currently there is a bug on the IMDBpy in actor's role
    #        (refers https://github.com/alberanid/imdbpy/issues/144 )

    ia = imdb.IMDb()

    for movie in movies:
        ia.update(movie)

        data = {
            "id": movie.movieID,
            "name": movie["title"],
            "kind": movie["kind"],
            "year": movie["year"],
            "genres": movie["genres"],
            "rating": movie["rating"],
            "directors": [i["name"] for i in movie["director"]],
            "cast": []
        }

        for actor in movie.get("cast"):
            data["cast"].append({
                "actor": actor["name"],
                "role": actor.notes
            })

        if cfg["general"]["engine"] == "elasticsearch":
            store_to_es(logger, cfg["elasticsearch"], data)
        elif cfg["general"]["engine"] == "mongo":
            store_to_mongo(logger, cfg["mongo"], data)


def main():
    """
    Main function
    :return:
    """

    args = initargs().parse_args()
    cfg = configparser.ConfigParser()

    try:
        with open(args.cfg) as f:
            cfg.read_file(f)
    except OSError as e:
        logging.basicConfig(format="%(asctime)s - %(levelname)s - %(message)s")
        logging.fatal("Cannot open the configuration file {}: {}".format(args.cfg, e.strerror))

    logger = setlog("movieindex", cfg["general"]["logfile"], cfg["general"]["loglevel"])
    logger.debug("Started application")

    logger.debug("Fetch data")
    movies = fetch(logger, args.top, args.bottom)
    save(logger, cfg, movies)

    logger.debug("Ended application")


if __name__ == '__main__':
    main()
