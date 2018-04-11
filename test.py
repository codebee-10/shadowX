#!/usr/bin/env python
# coding=utf-8

#-*- coding:utf-8 -*-
import logging
# 配置日志信息
logging.basicConfig(level=logging.DEBUG,
          format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
          datefmt='%m-%d %H:%M',
          filename='myapp.log',
          filemode='w')
# 定义一个Handler打印INFO及以上级别的日志到sys.stderr
console = logging.StreamHandler()
console.setLevel(logging.INFO)
# 设置日志打印格式
formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
console.setFormatter(formatter)
# 将定义好的console日志handler添加到root logger
logging.getLogger('').addHandler(console)
logging.info('Jackdaws love my big sphinx of quartz.')
logger1 = logging.getLogger('myapp.area1')
logger1.debug('Quick zephyrs blow, vexing daft Jim.')

from task.default import task_init
from task.monitor.base.ping_scan import ping_scan
from task.monitor.base.port_scan import port_scan
from task.monitor.base.portal_scan import portal_scan
from config.log_config import monitor
from config import shadowx_config
from worker import execute
import re
import json
import requests
from server.db.DataBasePool import DataBasePool
from task.monitor.base.ping_muti_scan import ping_muti_scan


if __name__ == "__main__":
    #ping 检测
    #p = ping_scan(logger=monitor, item_id="", ip="10.10.83.235", port="", method="", username="", password="")

    # port 检测
    #p = port_scan(logger=monitor, item_id="", ip="10.10.83.235", port="3306", method="", username="", password="")

    # portal 检测 / 页面检测
    #p = portal_scan(urls="https://www.baidu.co",logger=monitor, item_id="", ip="10.10.83.235", port="3306", method="", username="", password="")
    #print(p)


    #execute.apply_async(args=['task.monitor.base.ping_scan.ping_scan'], kwargs={'ip':'10.10.83.235'})
    #execute.apply_async(args=['task.monitor.base.port_scan.port_scan'], kwargs={'ip': '10.10.83.175', 'port': '3306'})
    #execute.delay('task.monitor.base.ping_scan.ping_scan', ip='10.10.83.235')

    """
    ip_list=('10.10.83.175','10.10.83.174','10.10.83.173','10.10.83.172')
    args={'ip':ip_list, 'username':'roan', 'password':'Roancsu'}
    print(json.dumps(args))

    args_to_map = json.dumps(args)
    args_m = json.loads(args_to_map)
    print(type(json.loads(args_to_map)))
    ip = args_m['ip']
    print(ip.__len__())
    """

    #sql = "insert into monitor_alarms(content,alarmstatus,item_id,ip,client) value('告警信息',1,10008,'10.10.83.175','10.10.83.175')"
    #result = DataBasePool(sql).execute()
    #print(result)

    #port_scan(ip='10.10.83.235',port=3306)

    #task_args = "{'username': 'root', 'password': 'root','client':'10.10.83.175'}"
    '''
    print(type(eval(task_args)))
    print(eval(task_args))
    task_args = eval(task_args)
    task_args["ip"] = "10.10.83.175"
    print(task_args)
    '''
    #ip_list = "{'ip':['10.10.83.17', '10.10.83.18', '10.10.83.19', '10.10.83.20','10.10.83.21', '10.10.83.22', '10.10.83.23', '10.10.83.24','10.10.83.25', '10.10.83.26', '10.10.83.27', '10.10.83.28','10.10.83.29', '10.10.83.30', '10.10.83.31', '10.10.83.32','10.10.83.33', '10.10.83.34', '10.10.83.35', '10.10.83.36']}"
    #ip_list = eval(ip_list)
    #for ip in ip_list['ip']:
    #    print(ip)

    #ping_muti_scan("task.monitor.base.ping_scan.ping_scan",
    #               "{'ip':['10.10.83.17', '10.10.83.18', '10.10.83.19', '10.10.83.20','10.10.83.21', '10.10.83.22', '10.10.83.23', '10.10.83.24','10.10.83.25', '10.10.83.26', '10.10.83.27', '10.10.83.28','10.10.83.29', '10.10.83.30', '10.10.83.31', '10.10.83.32','10.10.83.33', '10.10.83.34', '10.10.83.35', '10.10.83.36'],"
    #               "'username': 'root', 'password': 'root','urls':['www.baidu.com'],'client':'10.10.83.175'}"
    #               )
    #portal_scan(urls='www.baidu.co', ip='10.10.83.23', item_id="110", client="10.10.83.175")

    #print(ip_list == "" or ip_list is None)

    # 获取 rmq 队列信息
    """
    res = requests.get(url='http://10.10.83.235:15672/api/queues', auth=('admin', 'guest'))
    print(json.loads(res.content.decode()))
    """

    notin = []
    notin.append(16)
    notin.append(17)
    notin.append(18)
    print(tuple(notin))



