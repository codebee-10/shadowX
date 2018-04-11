# -*- coding: utf-8 -*-

import pymysql
from task.common.BaseDesKey import prpcrypt
from config.log_config import monitor as logger


class Mysql(object):

    _key = '8888888866666666'  # AES加密秘钥

    def __init__(self, host, port, user, pwd, db, timeout=30):
        self.host = host
        self.port = port
        self.user = user
        self.password = pwd
        self.db = db
        self.timeout = timeout
        self.keydata = prpcrypt(self._key)
        self.conn = self.connect()
        self.cursor = self.get_cursor(self.conn)

    def connect(self):
        """
        连接数据库
        语法:  MySQLdb.connect(host=主机地址, port=端口, user=用户名, passwd=密码, db=库)
        """
        try:
            passwd = self.keydata.decrypt(self.password)
            conn = pymysql.connect(host=self.host, port=self.port, user=self.user, passwd=passwd, db=self.db,
                                   charset='utf8', connect_timeout=self.timeout)
            return conn
        except Exception as err:
            logger.error(err)

    def get_cursor(self, conn):
        """
        获取游标
        """
        cursor = conn.cursor()
        # cursor.execute('set names utf8')
        return cursor

    def execute_sql(self, sql):
        try:
            self.cursor.execute(sql)
        except Exception as err:
            logger.error(err)

    @property
    def fetchone(self):
        """
        :return: 返回一条数据，从第一条开始，每执行一次，依次返回
        """
        res_one = self.cursor.fetchone()
        return res_one

    def fetchmang(self, n):
        """
        :param n:
        :return: 返回第n条数据
        """
        res_mang = self.cursor.fetchmany(n)
        return res_mang

    @property
    def fetchall(self):
        """
        :return: 返回所有数据
        """
        res_all = self.cursor.fetchall()
        return res_all

    def commit(self):
        """
        提交事务
        """
        self.conn.commit()

    def close(self):
        """
        关闭游标、关闭连接
        """
        self.cursor.close()
        self.conn.close()

    def __del__(self):
        self.close()


def main():
    mysql_obj = Mysql('10.10.83.162', 3306, 'root', 'bc444a35b5a5bed6597ec28a83f33d13', 'eastmoney')
    mysql_obj.execute_sql('show global variables;')
    print(mysql_obj.fetchall)
    mysql_obj.execute_sql('show global status;')
    print(mysql_obj.fetchall)

if __name__ == '__main__':

    main()
