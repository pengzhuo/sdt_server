# coding: utf-8
# Author: pengz
# Email: pch987.net@163.com

from utils.db_mysql import Db_Mysql
from utils.db_redis import Db_Redis
from utils.singleton import Singleton
from models.user import User
from utils.log import log

class DataManager():
    __metaclass__ = Singleton

    prefix_sdt = "sdt_{0}"
    prefix_user = "user:{0}"
    db_mysql = None
    db_redis = None

    def __init__(self):
        self.db_mysql = Db_Mysql()
        self.db_redis = Db_Redis()

    def addUser(self, uid, session):
        res = None
        userId = self.prefix_sdt.format(10000 + self.db_redis.getNo())
        sql = "insert into user (userId, uid, session_key) VALUES ('{0}', '{1}', '{2}')".format(userId, uid, session)
        if self.db_redis.get(self.prefix_user.format(userId)) is None:
            if self.db_mysql.execSql(sql) is not None:
                user = User(userId, uid, session)
                self.db_redis.set(self.prefix_user.format(userId), user.toJson())
                res = user
        else:
            log().info("already have the user [uid:{0}, session:{1}]".format(uid, session))
        return res

    def getUser(self, userId):
        str = self.db_redis.get(self.prefix_user.format(userId))
        if str is not None:
            user = User()
            user.initWithJson(str)
            return user
        return None

    def updateUser(self, user):
        sql = "UPDATE user SET uname='{0}',icon='{1}',country='{2}',province='{3}',city='{4}',gender={5} WHERE userId='{6}'".format(
            user.uname.encode("utf-8"),
            user.icon,
            user.country,
            user.province,
            user.city,
            user.gender,
            user.userId
        )
        if self.db_mysql.execSql(sql) is not None:
            self.db_redis.set(self.prefix_user.format(user.userId), user.toJson())