#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime, timedelta
from config.shadowx_config import DATE_FORMATE
from server.db import DataBasePool
import time


class MessageTunnel():
    def __init__(self, item_id, ip, message, client, alarmstatus=1):
        self.item_id = item_id
        self.ip = ip
        self.message = message
        self.client = client
        self.alarmstatus = alarmstatus

    def save_alarm_message(self):
        create_time = (datetime.now()).strftime(DATE_FORMATE)
        sql = "insert into monitor_alarms(content,alarmstatus,created_at,item_id,ip,client) values('"+self.message+"',0,'"+create_time+"',"+self.item_id+",'"+self.ip+"','"+self.client+"')"
        result = DataBasePool.DataBasePool(sql).execute()
        if result:
            print(result)

    def save_message(self):
        pass

    def send_message(self):
        alarm_message = str(self.item_id)+":"+self.ip+":"+self.message+":"+self.client
        print("sms,wx,email error message send : "+alarm_message)


if __name__ == "__main__":
    MessageTunnel("10.10.83.175", "error message", "10.10.83.175").save_alarm_message()