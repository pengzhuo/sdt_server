# coding: utf-8
# Author: pengz
# Email: pch987.net@163.com

from utils.db_redis import Db_Redis
from utils.singleton import Singleton
from models.user import User
from utils.log import log

class DataManager():
    __metaclass__ = Singleton

    prefix_sdt = "sdt_{0}"
    prefix_user = "user:{0}"
    prefix_uid = "uid_sdtid:{0}"
    db_mysql = None
    db_redis = None

    def __init__(self):
        self.db_redis = Db_Redis()

    def addUser(self, uid, session):
        res = None
        indexId = self.prefix_uid.format(uid)
        if self.db_redis.get(indexId) is None:
            userId = self.prefix_sdt.format(10000 + self.db_redis.getNo())
            if self.db_redis.get(self.prefix_user.format(userId)) is None:
                user = User(userId, uid, session)
                self.db_redis.set(self.prefix_user.format(userId), user.toJson())
                res = user
            else:
                log().info("already have the user [uid:{0}, session:{1}]".format(uid, session))
            self.db_redis.set(indexId, userId)
        else:
            user = User()
            userId = self.db_redis.get(indexId)
            userStr = self.db_redis.get(self.prefix_user.format(userId))
            user.initWithJson(userStr)
            user.session_key = session
            self.db_redis.set(self.prefix_user.format(userId), user.toJson())
            res = user
        return res

    def getUser(self, userId):
        str = self.db_redis.get(self.prefix_user.format(userId))
        if str is not None:
            user = User()
            user.initWithJson(str)
            return user
        return None

    def updateUser(self, user):
        self.db_redis.set(self.prefix_user.format(user.userId), user.toJson())