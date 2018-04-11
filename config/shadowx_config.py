#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from celery import platforms
from celery import Celery


'''mysql 连接池配置 '''
mysql = {
    'pool_name': 'shadowX_pool',
    'host': '',  # 数据库地址
    'port': 3306,
    'user': 'root',
    'password': 'root',
    'database': 'celery',
    'pool_resize_boundary': 50,
    'enable_auto_resize': True,
    # 'max_pool_size': 10
}


'''redis 连接配置 '''
redis = {
    'host': '',  # redis 地址
    'port': 6379,
    'user': 'root',
    'password': 'root',
    'db': 0,
}


'''rabbitmq 连接配置 '''
rabbit = {
    'host': '',  # RMQ地址
    'port': 5672,
    'user': 'guest',
    'password': 'admin',
    'db': 0,
}


def get_celery():
    """ Celery 配置信息 """
    # rabbitmq 地址
    BROKER = 'amqp://'+rabbit['password']+':'+rabbit['user']+'@'+rabbit['host']+':'+str(rabbit['port'])
    # redis 地址
    BACKEND = 'redis://'+redis['host']+':'+str(redis['port'])+"/"+str(redis['db'])
    CELERY_ACCEPT_CONTENT = ['json']
    CELERY_TASK_SERIALIZER = 'json'
    CELERY_RESULT_SERIALIZER = 'json'
    CELERY_ENABLE_UTC = False
    CELERY_TIMEZONE = 'Asia/Shanghai'
    platforms.C_FORCE_ROOT = True

    # 创建 celery
    celery = Celery('worker', broker=BROKER, backend=BACKEND)
    # 定义任务发现
    celery.conf.CELERY_IMPORTS = ['task.all_task',  #
                                  'task.default.task_init',  # 默认启动任务
                                  'task.monitor.base',  # 基础监控任务
                                  'task.monitor.server',  # 业务监控任务
                                  'task.monitor.tpm'   # 第三方组件监控任务
                                  ]

    return celery, BROKER


DATE_FORMATE = "%Y-%m-%d %H:%M:%S"
