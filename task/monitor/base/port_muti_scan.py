#!/usr/bin/env python
# -*- coding: utf-8 -*-
from worker import execute


def port_muti_scan(item_id, ip="", urls="", port="", method="", username="", password="", client=""):

    if ip !="" and ip is not None:
        ip_list = eval(str(ip))
        for ip in ip_list:
            execute.apply_async(
                args=['task.monitor.base.port_scan.port_scan'],
                kwargs={'ip': ip, 'item_id': item_id, 'urls': urls, 'port': port, 'method': method,
                        'username': username, 'password': password, 'client': client
                        }
            )

    elif urls !="" and urls is not None:
        ip_list = eval(str(urls))
        for ip in ip_list:
            execute.apply_async(
                args=['task.monitor.base.port_scan.port_scan'],
                kwargs={'ip': ip, 'item_id': item_id, 'urls': urls, 'port': port, 'method': method,
                        'username': username, 'password': password, 'client': client
                        }
            )