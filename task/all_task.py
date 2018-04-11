#!/usr/bin/env python
# -*- coding: utf-8 -*-
from tornado.httpclient import HTTPClient
import time
from dbpool import task_backend


def async_http_():
    urls = 'http://www.baidu.com'
    http_client = HTTPClient()
    response = http_client.fetch(urls)
    print(response.body)


def print_time():
    print("celery time is: " + str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
    time.sleep(2)
    print("time sleep test")


if __name__ == "__main__":
    pass
