#!/usr/bin/env python
_instances = {}
from .db_connection import MySQLConnectionPool


def ConnectionPool(*args, **kwargs):
    try:
        pool_name = args[0]
    except IndexError:
        pool_name = kwargs['pool_name']

    if pool_name not in _instances:
        _instances[pool_name] = MySQLConnectionPool(*args, **kwargs)
    pool = _instances[pool_name]
    assert isinstance(pool, MySQLConnectionPool)
    return pool