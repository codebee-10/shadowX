#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
import sys


class Logger():
    def __init__(self, log_name, logger):
        # 获取logger实例，如果参数为空则返回root logger
        self.logger = logging.getLogger(log_name)

        # 指定logger输出格式
        self.formatter = logging.Formatter('%(asctime)s %(levelname)-8s: %(message)s')

        # 文件日志
        self.file_handler = logging.FileHandler(logger)
        self.file_handler.setFormatter(self.formatter)  # 可以通过setFormatter指定输出格式

        # 控制台日志
        self.console_handler = logging.StreamHandler(sys.stdout)
        self.console_handler.formatter = self.formatter  # 也可以直接给formatter赋值

        # 为logger添加的日志处理器
        self.logger.addHandler(self.file_handler)
        self.logger.addHandler(self.console_handler)

        # 指定日志的最低输出级别，默认为WARN级别
        self.logger.setLevel(logging.DEBUG)


    def getlog(self):
        return self.logger