#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Task Worker
This module define function which can dynamic load task and execute task's function.
Celery Worker connect RMQ,redis backer and backend
    self.BROKER = 'amqp://admin:guest@127.0.0.1:5672/'
    self.BACKEND = 'redis://127.0.0.1:6379/0'

 Dynamic Import:
     def dync_load_task(self, import_name):
        ...

 Register Task:
    @celery.task
    def execute(func, *args, **kwargs):
        ...

You can Register more task to complete more function.

Usage:
$ python task_worker.py

you can also run like this:
celery worker -A tasks --loglevel=info

"""
from celery.bin import worker as celery_worker
from importlib import import_module, reload
from config import shadowx_config
import os


class TWorker():
    def __init__(self):
        self.celery, self.BROKER = shadowx_config.get_celery()

    def get_celery(self):
        return self.celery

    def dync_load_task(self, import_name):
        """ 动态任务导入 """
        import_name = str(import_name).replace(':', '.')
        modules = import_name.split('.')
        mod = import_module(modules[0])

        moo = import_name.split('.')
        moo.pop(-1)
        task_path = '.'.join(moo)
        import_module(task_path)

        for comp in modules[1:]:
            if not hasattr(mod, comp):
                reload(mod)
            mod = getattr(mod, comp)
        return mod

    def worker_start(self):
        """ 启动 worker """
        worker = celery_worker.worker(app=self.celery)
        worker.run(
            broker=self.BROKER,
            concurrency=30,
            traceback=False,
            loglevel='INFO',
        )


""" 实例化Worker """
tw = TWorker()
celery = tw.get_celery()

""" 任务注册"""
@celery.task
def execute(func, *args, **kwargs):
    func = tw.dync_load_task(func)
    return func(*args, **kwargs)


if __name__ == '__main__':
    """ 启动任务 """
    tw.worker_start()

