# -*- coding: utf-8 -*-

# Copyright (C) 2018 Enrico Bianchi (enrico.bianchi@gmail.com)
# Project       movieindex
# Description   An IMDB movie indexer
# License       GPL version 2 (see LICENSE for details)
import urllib.parse

import bson
import pymongo


class Elasticsearch:
    _url = None
    _index = None

    @property
    def url(self):
        return self._url

    @property
    def index(self):
        return self._index

    def __init__(self, cfg):
        host = cfg["host"]
        port = cfg["port"] if "port" in cfg else 9200
        scheme = cfg["scheme"]
        self._index = cfg["index"]

        url = scheme + "://" + host + "/" + port
        self._url = urllib.parse.urlparse(url)

        if not self.url.scheme:
            raise ValueError("Malformed source URL: {}".format(url))

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def exists(self, data):
        pass

    def store(self, data):
        pass


class MongoDB:
    _connection = None
    _database = None
    _collection = None

    @property
    def connection(self):
        return self._connection

    @property
    def collection(self):
        return self._collection

    def __init__(self, cfg):
        host = cfg["host"]
        port = cfg["port"] if "port" in cfg else 27017
        user = cfg["user"] if "user" in cfg else None
        password = cfg["password"] if "password" in cfg else None
        dbauth = cfg["dbauth"] if "dbauth" in cfg else "admin"

        if user:
            self._connection = pymongo.MongoClient(host=host, port=int(port),
                                                   username=user, password=password,
                                                   authSource=dbauth)
        else:
            self._connection = pymongo.MongoClient(host=host,
                                                   port=int(port))

        self._database = self._connection[cfg["database"]]
        self._collection = cfg["collection"]

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def close(self):
        self._connection.close()

    def exists(self, data):
        """
        Check if data is in json
        :param data: JSON that contains data
        :return: True if is already stored else False
        """

        collection = self._database[self.collection]

        cur = collection.count(data)

        return False if cur == 0 else True

    def store(self, data):
        collection = self._database[self.collection]

        try:
            collection.insert_one(data)
        except bson.errors.InvalidDocument as e:
            print("|-- Cannot insert document: {}".format(e))
