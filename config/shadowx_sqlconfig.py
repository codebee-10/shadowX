#!/usr/bin/env python
# -*- coding: utf-8 -*-

GET_ALL_TASK = 'select id,task_name,task_args,last_run_time,sec,crontab,task_type ' \
               'from monitor_items ' \
               'where monitorstatus = 1 '

GET_WARN_SET = 'select id,key_name,key_name_cn,key_value,status ' \
               'from monitor_warnsetting ' \
               'where key_name in (\'WARN_IS_OPEN\',\'A_ALARM\',\'B_ALARM\',' \
               '\'C_ALARM\',\'D_ALARM\',\'E_ALARM\',\'LOG_ALARM\')'

GET_SOME_TASK = 'select id,task_name,task_args,last_run_time,sec,crontab,task_type,typeid ' \
               'from monitor_items ' \
               'where monitorstatus = 1 and typeid not in  '

