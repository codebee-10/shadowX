#!/usr/bin/env python
# -*- coding: utf-8 -*-
from config import shadowx_config
from config.log_config import redis_log
import redis


def tasks_clear():
    '''清除backend中redis 数据'''
    try:
        re = redis.Redis(host=shadowx_config.redis['host'], port=shadowx_config.redis['port'], db=shadowx_config.redis['db'])
        re.flushdb()
        redis_log.debug("[ Reids flush complete !]")
    except:
        redis_log.debug("[ Reids flush failed !]")


def tasks_init():
    pass



