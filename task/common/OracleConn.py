import cx_Oracle
from config.log_config import monitor as logger


class Oracle(object):
    def __init__(self, host, port, username, password, tnsname):
        self.__username = username
        self.__password = password
        self.__host = host
        self.__port = port
        self.__tnsname = tnsname
        self.conn = self.connect()
        self.cursor = self.get_cursor(self.conn)

    def connect(self):
        """
        连接数据库
        语法: cx_Oracle.connect('username','pwd','IP/HOSTNAME:PORT/TNSNAME')
        或
        cx_Oracle.makedsn(IP,PORT,TNSNAME)
        cx_Oracle.connect(username,pwd,dsn)
        """
        try:
            dsn = cx_Oracle.makedsn(self.__host, self.__port, self.__tnsname)
            conn = cx_Oracle.connect(self.__username, self.__password, dsn)
            # self.__conn = cx_Oracle.connect(self.__username, self.__password,
            #                   self.__host + ':' + self.__port + '/' + self.__service_name)
            return conn
        except Exception as err:
            logger.error(err)

    def get_cursor(self, conn):
        """
        :param conn:
        :return: 获取游标
        """
        cursor = conn.cursor()
        return cursor

    def execute_sql(self, sql):
        """
        :param sql:
        :return: 执行sql
        """
        self.cursor.execute(sql)

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

    def close(self):
        """
        关闭游标、关闭连接
        """
        self.cursor.close()
        self.conn.close()

    def __del__(self):
        self.close()


def main():
    import time, datetime
    # oracle = Oracle('10.10.81.114', '1521', 'monitor', 'Ex2ec809', 'EMZQDC')
    oracle = Oracle('10.10.73.222', '1521', 'middledevelop_r', 'md*aGjK', 'EMBASEGA')
    # oracle.execute_sql("SELECT * FROM ogg.em_ogg_process_lag ORDER BY seqno DESC")
    oracle.execute_sql("SELECT TDATE FROM newsadmin.TRAD_TD_TDATE WHERE TRADEMARKETCODE = '070001'")
    # oracle.execute_sql("SELECT Max(seqno) FROM ogg.em_ogg_process_lag")
    list_oracle = []
    res_oracle = oracle.fetchall
    for item in res_oracle:
        if '2017' in item[0]:
            list_oracle.append(item[0])

if __name__ == '__main__':
    main()
