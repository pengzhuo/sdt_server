# coding: utf-8
# Author: pengz
# Email: pch987.net@163.com

from utils.db_mysql import Db_Mysql
from utils.db_redis import Db_Redis
from utils.singleton import Singleton

class DataManager():
    __metaclass__ = Singleton

    db_mysql = None
    db_redis = None

    def __init__(self):
        self.db_mysql = Db_Mysql()
        self.db_redis = Db_Redis()

    def addUser(self, userInfo):
        pass