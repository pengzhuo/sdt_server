# coding: utf-8
# Author: pengz
# Email: pch987.net@163.com

import MySQLdb
from DBUtils.PooledDB import PooledDB
from utils.singleton import Singleton
from utils.log import log
from config import *

#数据库操作
class Db_Mysql():
    __metaclass__ = Singleton

    #数据库对象
    pool = None
    conn = None
    cur = None

    def __init__(self):
        self.pool = PooledDB(
            MySQLdb,
            DB_MINCONNUM,
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            passwd=DB_PASSWD,
            db=DB_NAME,
        )

    def query(self, sql):
        res = None
        try:
            self.conn = self.pool.connection()
            self.cur = self.conn.cursor()
            self.cur.execute(sql)
            res = self.cur.fetchall()
            self.cur.close()
            self.conn.close()
        except:
            import traceback
            log().error(traceback.print_exc())
        finally:
            return res

    def execSql(self, sql):
        res = None
        try:
            self.conn = self.pool.connection()
            self.cur = self.conn.cursor()
            res = self.cur.execute(sql)
            self.conn.commit()
            self.cur.close()
            self.conn.close()
        except:
            import traceback
            log().error(traceback.print_exc())
        finally:
            return res

    def close(self):
        if self.pool is not None:
            self.pool.close()
            self.pool = None