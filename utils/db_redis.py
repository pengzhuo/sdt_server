# coding: utf-8
# Author: pengz
# Email: pch987.net@163.com

import redis
from utils.singleton import Singleton
from config import *

class Db_Redis():
    __metaclass__ = Singleton

    instance = None

    def __init__(self):
        self.instance = redis.StrictRedis(REDIS_HOST, REDIS_PORT, REDIS_DB, REDIS_PASSWORD)

    def get(self, key):
        return self.instance.get(key)

    def set(self, key, value):
        self.instance.set(key, value)