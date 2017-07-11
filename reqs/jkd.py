# coding: utf-8
# Author: pengz
# Email: pch987.net@163.com

from tornado.web import RequestHandler
from utils.func import findKdInfoByAddr

#寄快递
class Jkd(RequestHandler):
    tip = "未查询到快递信息！请确认地址是否正常或者稍后再试！"

    def post(self, *args, **kwargs):
        try:
            xzqname = self.get_argument("xzqname")
            keywords = self.get_argument("keywords")
            self.deal(xzqname, keywords)
        except:
            self.write(self.tip)

    def get(self, *args, **kwargs):
        try:
            xzqname = self.get_argument("xzqname")
            keywords = self.get_argument("keywords")
            self.deal(xzqname, keywords)
        except:
            self.write(self.tip)

    def deal(self, xzqname, keywords):
        if xzqname is not None and keywords is not None:
            res = findKdInfoByAddr(xzqname, keywords)
        if res is None:
            res = self.tip
        self.write(res)