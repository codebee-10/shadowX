import redis
from config.log_config import monitor as logger


class ReidsConn(object):

    def __init__(self, host, port, db=0, password=None):
        self.host = host
        self.port = port
        self.db = db
        self.password = password

    def __call__(self, *args, **kwargs):
        res = self.connect()
        return res

    def connect(self):
        """
        :return: 连接redis
        """
        try:
            if self.password is None:
                pool = redis.ConnectionPool(host=self.host, port=self.port, db=self.db)
            else:
                pool = redis.ConnectionPool(host=self.host, port=self.port, db=self.db, password=self.password)
            r = redis.Redis(connection_pool=pool)
            return r
        except Exception as err:
            logger.error(err)
