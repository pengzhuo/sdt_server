# coding: utf-8
# Author: pengz
# Email: pch987.net@163.com

from tornado.ioloop import IOLoop
from tornado.web import Application
from tornado.options import define, options
from reqs.cxkd import Cxkd
from reqs.jkd import Jkd
from reqs.details import Details
from reqs.user import User
from config import *

def main():
    define("host", "0.0.0.0", type=str)
    define("server_port", SERVER_PORT, type=int)
    define("logger_port", LOGGER_PORT, type=int)
    define("redis_host", REDIS_HOST, type=str)
    define("redis_port", REDIS_PORT, type=int)
    define("redis_password", REDIS_PASSWORD, type=str)
    define("redis_db", REDIS_DB, type=int)
    options.parse_command_line()
    
    app = Application(
        handlers=[
            (r"/sdt/cxkd", Cxkd),
            (r"/sdt/jkd", Jkd),
            (r"/sdt/details", Details),
            (r"/sdt/user", User),
        ]
    )
    app.listen(options.server_port)
    IOLoop.instance().start()

if __name__ == '__main__':
    main()