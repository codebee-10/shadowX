#!/usr/bin/env python
# -*- coding: utf-8 -*-
from dbpool import db_instance
from config import shadowx_config, shadowx_sqlconfig


class DataBasePool():
    def __init__(self, sql):
        self.pool = db_instance.ConnectionPool(**shadowx_config.mysql)
        self.sql = sql

    def execute(self):
        '''存储数据 '''
        with self.pool.cursor() as cursor:
            res = cursor.execute(self.sql)
            return res

    def select(self):
        '''存储数据 '''
        with self.pool.cursor() as cursor:
            cursor.execute(self.sql)
            res = sorted(cursor, key=lambda x: x['id'])
            return res

    def save(self):
        '''存储数据 '''
        pass

    def update(self):
        '''存储数据 '''
        pass
