#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Task Beat
This module define function which can execute muti-asyn-task and dispatch tasks.
Use stack to sort the date of task which will be executing.Min_time is the Main
processing sleeping time that can compute more quick to execute task .

    pool = db_instance.ConnectionPool(**db_config.mysql)linu
        ...
use database pool to connect mysql

    @async
    def execute_task(taskList):
        ...
use muti-thread to execute task. Performance: 1000 tasks /s

Usage:

$ python task_beat.py

suggestion:
    you can use supervisor to make sure the main progress will not die in abnormal
    condition .
"""
from datetime import datetime, timedelta
from threading import Thread
from config import shadowx_config, shadowx_sqlconfig
from config.shadowx_config import DATE_FORMATE
from dbpool import db_instance
from worker import execute
from run.crontab import crontab_run_nextTime
import time
import json
import heapq

MAIN_SLEEP_TIME = 1


def async(f):
    '''线程异步'''
    def wrapper(*args, **kwargs):
        thr = Thread(target=f, args=args, kwargs=kwargs)
        thr.start()
    return wrapper


def date_seconds(date1, date2):
    '''将时间差转化为秒'''
    di = date2 - date1
    return di.days*24*3600 + di.seconds


def connection_pool():
    '''获取连接池实例 '''
    pool = db_instance.ConnectionPool(**shadowx_config.mysql)
    return pool


def init_task():
    '''初始化任务 '''
    with connection_pool().cursor() as cursor:
        print("init ...")
        init_time = (datetime.now()).strftime(DATE_FORMATE)
        sql = "update monitor_items set last_run_time = '" + init_time + "'"
        cursor.execute(sql)

@async
def update_task(task_id, run_time):
    '''异步更新任务的执行时间 '''
    with connection_pool().cursor() as cursor:
        sql = "update monitor_items set last_run_time = '" + run_time + "' where id = %d" % task_id
        cursor.execute(sql)


def execute_muti_tasks(id, task_name, task_args):
    task_args = eval(task_args)
    task_args["item_id"] = str(id)
    execute.apply_async(args=[task_name], kwargs=eval(str(task_args)))


@async
def execute_task(taskList):
    '''最小堆执行任务 '''
    now_time = datetime.now()
    run_time = list()
    count = 0
    for task in taskList:
        dt = date_seconds(now_time, task['last_run_time'])
        # 如果得到的结果为0，则执行任务,修改时间为最新的next_run_time
        if dt == 0:
            # 执行循环任务
            if task['task_type'] == 1:
                if task['task_args'] is None:
                    execute.apply_async(args=[task['task_name']])
                else:
                    execute_muti_tasks(task['id'], task['task_name'], task['task_args'])

                next_run_time = (datetime.now() + timedelta(seconds=task['sec'])).strftime(DATE_FORMATE)
                update_task(task_id=task['id'], run_time=next_run_time)
                run_time.append(task['sec'])
                count += 1

            # 执行定时任务
            elif task['task_type'] == 2:
                if task['task_args'] is None:
                    execute.apply_async(args=[task['task_name']])
                else:
                    execute_muti_tasks(task['id'], task['task_name'], task['task_args'])

                # 计算下次运行的时间
                next_run_time = crontab_run_nextTime(task['crontab'])[0]
                update_task(task_id=task['id'], run_time=next_run_time)
                run_time.append(date_seconds(datetime.strptime(next_run_time, DATE_FORMATE), now_time))
                count += 1

        elif dt < 0:
            # linu如果得到的结果为负数，则需要修改时间为最新的next_run_time
            if task['task_type'] == 1:
                next_run_time = (datetime.now() + timedelta(seconds=task['sec'])).strftime(DATE_FORMATE)
                update_task(task_id=task['id'], run_time=next_run_time)
                run_time.append(task['sec'])

            elif task['task_type'] == 2:
                next_run_time = crontab_run_nextTime(task['crontab'])[0]
                update_task(task_id=task['id'], run_time=next_run_time)
                run_time.append(date_seconds(datetime.strptime(next_run_time, DATE_FORMATE), now_time))
        else:
            run_time.append(dt)

    if count > 0:
        print("execute success tasks: %d " % count)
        print(run_time)


def _main(notin):
    '''可以用本地队列对全量获取task做优化'''
    with connection_pool().cursor() as cursor:
        res = cursor.execute(shadowx_sqlconfig.GET_SOME_TASK + str(notin))
        tasks = sorted(cursor, key=lambda x: x['id'])
        # 返回最小休眠时间
        if list(tasks).__len__() > 0:
            print(datetime.now().strftime(DATE_FORMATE) + ": main process sleeping and task num:  %d " % list(
                tasks).__len__())
            execute_task(list(tasks))
        else:
            print("task num is zero , sleeping %d s" % 5)
            time.sleep(5)
        # 主进程休眠
        time.sleep(MAIN_SLEEP_TIME)


'''
tasks[0]: 监控开关
tasks[1]: A类监控开关
tasks[2]: B类监控开关
tasks[3]: C类监控开关
tasks[4]: D类监控开关
tasks[5]: E类监控开关
tasks[6]: 日志监控开关
'''
def _main_set():
    with connection_pool().cursor() as cursor:
        res = cursor.execute(shadowx_sqlconfig.GET_WARN_SET)
        tasks = sorted(cursor, key=lambda x: x['id'])
        notin = []
        for task in tasks[1:]:
            if task["status"] == 0:
                notin.append(task["id"])
        notin.append(0)
        return tasks[0], tuple(notin)


def run():
    notin = _main_set()[1]
    if _main_set()[0]["status"]:
        _main(notin)
    else:
        print("Monitor is closed ")
        time.sleep(5)


if __name__ == "__main__":
    init_task()
    # 出现异常不会中断进程
    while True:
       try:
           run()
       except:
           run()