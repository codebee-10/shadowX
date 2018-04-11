# -*- coding: utf-8 -*-
import pymysql
from config.log_config import monitor as logger


class Mysql(object):
    def __init__(self, host, port, user, pwd, db, timeout=30):
        self.host = host
        self.port = port
        self.user = user
        self.password = pwd
        self.db = db
        self.timeout = timeout
        self.conn = self.connect()
        self.cursor = self.get_cursor(self.conn)

    def connect(self):
        """
        连接数据库
        语法:  MySQLdb.connect(host=主机地址, port=端口, user=用户名, passwd=密码, db=库)
        """
        try:
            conn = pymysql.connect(host=self.host, port=self.port, user=self.user, passwd=self.password, db=self.db,
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
        logger.error("关闭mysql链接")
        self.close()


def main():
    mysql_obj = Mysql('180.163.69.170', 48752, 'zabbix', 'zabbix', 'zabbix')
    mysql_obj.execute_sql("select hostid from hosts where host = '10.10.72.161'")
    mysql_res = mysql_obj.fetchone
    if mysql_res:
        hostid = mysql_res[0]
        mysql_obj.execute_sql("SELECT itemid FROM items WHERE hostid ='{}' AND key_='tcpconn'".format(hostid))
        item_res = mysql_obj.fetchone
        if item_res:
            item_id = item_res[0]
            mysql_obj.execute_sql("select value,FROM_UNIXTIME(clock) from history_uint where itemid ='{}'AND clock >1512005400 AND clock <1512006600 ORDER BY clock DESC".format(item_id))
            item_ress = mysql_obj.fetchall
            if item_ress:
                i = 0
                for item in item_ress:
                    j = i+1
                    if(j > (len(item_ress)-1)):
                        break
                    first = item[0]
                    second = item_ress[j][0]
                    clock = item[1]
                    bi = abs(first-second)/second
                    print("比例，值1，值2,时间", bi, first, second,clock)
                    i = i+1



if __name__ == '__main__':

    main()
