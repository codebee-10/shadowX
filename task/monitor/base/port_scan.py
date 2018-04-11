#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
from task.common.BaseClass import get_time
from task.common.SocketBaseClass import BaseSocket
from server.monitor import MessageTunnel, LogsFile
import json


def port_scan(item_id, ip="",  urls="", port="", method="", username="", password="", client="",
              logger=LogsFile.LogsFile().get_monitor_logs()):
    """
    port 检测
    :param ip:
    :param port:
    :param method:
    :param username:
    :param password:
    :param item_id:
    :param logger:
    :return:
    """

    logger = logger
    item_id = item_id
    ip = ip
    urls = urls
    port = int(port)
    method = method
    username = username
    password = password
    scanport = None
    logger.debug('----------------------------------------------------------------\n')

    global err
    try:
        logger.info("[CONNECTING]主机地址:{}, 端口:{}".format(ip, port))
        start_time = int(round(time.time() * 1000))
        scanport = BaseSocket(logger, ip, port)
        connect_status, desc = scanport.connect(timeout=3)
        scanport.close()
        end_time = int(round(time.time() * 1000))
        response_time = end_time - start_time
        h, m, s = get_time()
        current_time = int(h) * 3600 + int(m) * 60 + int(s)
        if connect_status is False:
            err = desc
            MessageTunnel.MessageTunnel(item_id, ip, str(err), client).save_alarm_message()
            MessageTunnel.MessageTunnel(item_id, ip, str(err), client).send_message()

            if int(port) == 8906 and 80700 < current_time < 81300:
                logger.warn("每天22点30分开户视频服务重启，不告警！")
            else:
                raise Exception

        logger.debug("[CONNECT SUCCESS]主机地址:{}, 端口:{}, 耗时:{}".format(ip, port, response_time))
    except Exception as e:
        scanport.close()
        logger.error(e)
        if str(e):
            err = "[TCP连接失败]主机地址:{}, 端口:{}".format(ip, port)
        logger.error(err)
        return json.dumps(err)
