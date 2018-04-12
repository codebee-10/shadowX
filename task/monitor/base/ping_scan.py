#!/usr/bin/env python
# -*- coding: utf-8 -*-
from task.common.PingBaseClass import Ping
from server.monitor import MessageTunnel, LogsFile
import json


def ping_scan(item_id, ip="", urls="", port="", method="", username="", password="", client="",
              logger=LogsFile.LogsFile().get_monitor_logs()):
    """
    ping 检测
    :param ip:
    :param item_id:
    :param port:
    :param method:
    :param username:
    :param password:
    :param logger:
    :return:
    """

    logger = logger
    ip = ip
    item_id = item_id
    urls = urls
    method = method
    username = username
    password = password
    client = client
    logger.debug('----------------------------------------------------------------\n')

    global err
    try:
        ping_status = Ping(ip, timeout=5, count=3)
        if not ping_status:
            err = "[ping检测异常]IP地址:{}".format(ip)
            MessageTunnel.MessageTunnel(item_id, ip, str(err), client).save_alarm_message()
            MessageTunnel.MessageTunnel(item_id, ip, str(err), client).send_message()
            raise Exception
        logger.debug("[ping正常]{}".format(ip))
    except Exception as e:
            logger.error(e)
            logger.error(err)
            return json.dumps(err)