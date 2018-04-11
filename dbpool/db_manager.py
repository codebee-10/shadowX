#!/usr/bin/env python
# coding=utf-8
from DBUtils.PooledDB import PooledDB
from datetime import datetime
import pymysql


'''数据库实例化类'''
class DbManager():
    def __init__(self):
        connKwargs = {
            'host': '10.10.83.175',
            'port': 3306,
            'user': 'root',
            'passwd': 'root',
            'db': 'celery',
            'charset': "utf8"
        }

        self._pool = PooledDB(
            pymysql,
            mincached=100,
            maxcached=200,
            maxshared=200,
            maxusage=100,
            **connKwargs
        )

    def get_connection(self):
        return self._pool.connection()


def get_conn():
    """ 获取数据库连接 """
    return DbManager().get_connection()


def execute_and_getId(sql, param=None):
    """ 执行插入语句并获取自增id """
    conn = get_conn()
    cursor = conn.cursor()
    if param == None:
        cursor.execute(sql)
    else:
        cursor.execute(sql, param)
    id = cursor.lastrowid
    cursor.close()
    conn.close()

    return id


def execute(sql, param=None):
    """ 执行sql语句 """
    conn = get_conn()
    cursor = conn.cursor()
    if param == None:
        rowcount = cursor.execute(sql)
    else:
        rowcount = cursor.execute(sql, param)
    conn.commit()
    cursor.close()
    conn.close()

    return rowcount


def queryOne(sql):
    """ 获取一条信息 """
    conn = get_conn()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    rowcount = cursor.execute(sql)
    if rowcount > 0:
        res = cursor.fetchone()
    else:
        res = None
    cursor.close()
    conn.close()

    return res


def queryAll(sql):
    """ 获取所有信息 """
    conn = get_conn()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    rowcount = cursor.execute(sql)
    if rowcount > 0:
        res = cursor.fetchall()
    else:
        res = None
    cursor.close()
    conn.close()

    return res


def initTask():
    init_time = (datetime.now()).strftime("%Y-%m-%d %H:%M:%S")
    sql = "update tasks set last_run_time = '" + init_time + "'"
    res = execute(sql)
    if res > 0:
        print("init program completed ")
    else:
        print("zero monitor complete init ")
    return res


def updateTaskDate(task_id, run_time):
    sql = "update tasks set last_run_time = '" + run_time + "' where id = %d" % task_id
    res = execute(sql)
    return res


def getUserList():
    res = queryAll('select id,task_name,task_status,last_run_time,sec,crontab,task_type from tasks')
    return res

