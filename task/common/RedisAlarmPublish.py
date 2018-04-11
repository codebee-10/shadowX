import json
import time
import requests
from task.common.RedisConn import ReidsConn
from config import shadowx_config as settings
#from monitor.models import GlobalConfs, Items, Alarms, InternetMappings, HostMaintenance
#from assets.models import Assets
from task.common.SmsClass import sendSMS
from config.shadowx_config import WARN_USER, WEIXINAPI

REDIS_OBJ = ReidsConn(settings.REDIS_CONN_ALARM['HOST'],
                      settings.REDIS_CONN_ALARM['PORT'],
                      password=settings.REDIS_CONN_ALARM['PASSWORD'])()


def alarm_contorl(logger, ip, item_id, err, typeid):
    """
    告警通知，redis发布和数据库记录
    """
    logger.debug("{}, {}, {}".format(ip, item_id, err))
    '''
    ch_status = int(GlobalConfs.objects.get(name='alarmstatus').val.strip())
    hk_status = int(GlobalConfs.objects.get(name='hkalarmstatus').val.strip())
    ds_status = int(GlobalConfs.objects.get(name='dsalarmstatus').val.strip())
    sql_status = int(GlobalConfs.objects.get(name='sqlalarmstatus').val.strip())
    oa_status = int(GlobalConfs.objects.get(name='accountstatus').val.strip())
    '''
    ch_status = ""
    hk_status = ""
    ds_status = ""
    sql_status = ""
    oa_status = ""

    logger.debug("告警路线123{}, {}".format(ds_status, typeid))
    if ch_status == 1 and typeid == 21:
        alarm_contorl_sub(logger, ip, item_id, err, typeid)
    elif hk_status == 1 and typeid == 22:
        alarm_contorl_sub(logger, ip, item_id, err, typeid)
    elif ds_status == 1 and typeid == 23:
        logger.debug("告警路线{}, {}".format(ds_status,typeid))
        alarm_contorl_sub(logger, ip, item_id, err, typeid)
    elif sql_status == 1 and typeid == 24:
        alarm_contorl_sub(logger, ip, item_id, err, typeid)
    elif oa_status == 1 and typeid == 25:
        alarm_contorl_sub(logger, ip, item_id, err, typeid)
    else:
        logger.warn("全局配置表告警开关没有开启")


def alarm_contorl_sub(logger, ip, item_id, err, typeid):
    global ip_monitorstatus
    redis_publish_data = {}
    try:
        # 库中查询 Items
        #iteminfo = Items.objects.get(id=item_id)
        iteminfo = ""
        desc = iteminfo.desc.strip()
        item_monitorstatus = iteminfo.monitorstatus  # 监控项开关
        if iteminfo.monitortype == 'report':
            cls_monitorstatus = 1
        else:
            cls_monitorstatus = iteminfo.servers.monitorstatus  # 监控服务开关
        client = iteminfo.clients  # 监控客户端IP和PORT
        personal = iteminfo.responsible

        # 库中查询 Assets
        #assetinfo = Assets.objects.filter(management_ip=ip)
        assetinfo = ""
        if assetinfo:
            ip_monitorstatus = assetinfo[0].monitorstatus  # 资产表开关

        internetinfo = InternetMappings.objects.filter(Q(internet_ip=ip) | Q(domain=ip))
        if internetinfo:
            ip_monitorstatus = internetinfo[0].monitorstatus  # 域名表开关

        alarmstatus = get_alarmstatus(ip, logger)
        if alarmstatus:
            redis_publish_data['alarmstatus'] = 0
        else:
            redis_publish_data['alarmstatus'] = 2

        if personal:
            content = "[监控项ID:" + str(item_id) + "] - " + "[告警IP:" + ip + "]" + desc + ', ' + \
                      err + ", 负责人:" + personal
        else:
            content = "[监控项ID:" + str(item_id) + "] - " + "[告警IP:" + ip + "]" + desc + ', ' + err
        redis_publish_data['ip'] = ip
        redis_publish_data['item_id'] = item_id
        redis_publish_data['content'] = content
        redis_publish_data['client'] = client

        Alarms.objects.create(**redis_publish_data)

        if int(item_monitorstatus) == 1 and int(ip_monitorstatus) == 1 and int(cls_monitorstatus) == 1 \
            and redis_publish_data['alarmstatus'] == 0:
            redis_publish_data['serviceid'] = typeid
            redis_publish_data = json.dumps(redis_publish_data)
            logger.debug(redis_publish_data)
            # REDIS_OBJ.publish(settings.REDIS_CONN_ALARM['CHANNEL'], redis_publish_data)  # redis发布
            # REDIS_OBJ.publish(settings.REDIS_CONN_MERGE_ALARM['CHANNEL'], redis_publish_data)
    except Exception as err:
        logger.error(err)


def recover_contorl(logger, item_id, ip, typeid):
    """
    告警恢复，redis发布和数据库记录
    """
    try:
        logger.debug("{}, {}".format(ip, item_id))
        #item_data = Alarms.objects.filter(item_id=item_id, ip=ip, alarmstatus=0).order_by("-id")
        item_data = ""
        if item_data:
            content = item_data[0].content
            client = item_data[0].client
            logger.debug("{}, {}".format(client, content))
            item_data.update(alarmstatus=1)

            '''
            ch_status = int(GlobalConfs.objects.get(name='alarmstatus').val.strip())
            hk_status = int(GlobalConfs.objects.get(name='hkalarmstatus').val.strip())
            ds_status = int(GlobalConfs.objects.get(name='dsalarmstatus').val.strip())
            sql_status = int(GlobalConfs.objects.get(name='sqlalarmstatus').val.strip())
            oa_status = int(GlobalConfs.objects.get(name='accountstatus').val.strip())
            '''
            ch_status = ""
            hk_status = ""
            ds_status = ""
            sql_status = ""
            oa_status = ""

            if ch_status == 1 and typeid == 21:
                recover_contorl_sub(logger, item_id, ip, typeid, content, client)
            elif hk_status == 1 and typeid == 22:
                recover_contorl_sub(logger, item_id, ip, typeid, content, client)
            elif ds_status == 1 and typeid == 23:
                recover_contorl_sub(logger, item_id, ip, typeid, content, client)
            elif sql_status == 1 and typeid == 24:
                recover_contorl_sub(logger, item_id, ip, typeid, content, client)
            elif oa_status == 1 and typeid == 25:
                recover_contorl_sub(logger, item_id, ip, typeid, content, client)
            else:
                logger.warn("全局配置表告警开关没有开启")
    except Exception as err:
        logger.error(err)


def recover_contorl_sub(logger, item_id, ip, typeid, content, client):
    global ip_monitorstatus
    redis_publish_data = {}
    try:
        iteminfo = Items.objects.get(id=item_id)
        item_monitorstatus = iteminfo.monitorstatus  # 监控项开关
        if iteminfo.monitortype == 'report':
            cls_monitorstatus = 1
        else:
            cls_monitorstatus = iteminfo.servers.monitorstatus  # 监控服务开关

        assetinfo = Assets.objects.filter(management_ip=ip)
        if assetinfo:
            ip_monitorstatus = assetinfo[0].monitorstatus  # 资产表开关

        internetinfo = InternetMappings.objects.filter(Q(internet_ip=ip) | Q(domain=ip))
        if internetinfo:
            ip_monitorstatus = internetinfo[0].monitorstatus  # 域名表开关
        logger.debug("监控项状态：{}, IP状态：{}, 监控服务状态：{}".format(item_monitorstatus, ip_monitorstatus,
                                                           cls_monitorstatus))

        alarmstatus = get_alarmstatus(ip, logger)
        if alarmstatus:
            redis_publish_data['alarmstatus'] = 1
        else:
            redis_publish_data['alarmstatus'] = 2

        redis_publish_data['ip'] = ip
        redis_publish_data['item_id'] = item_id
        redis_publish_data['content'] = '[已修复] => ' + content
        redis_publish_data['client'] = client
        # redis_publish_data['alarmstatus'] = 1
        redis_publish_data['serviceid'] = typeid

        if int(item_monitorstatus) == 1 and int(ip_monitorstatus) == 1 and int(cls_monitorstatus) == 1 \
            and redis_publish_data['alarmstatus'] == 1:
            redis_publish_data = json.dumps(redis_publish_data)
            logger.debug(redis_publish_data)
            # REDIS_OBJ.publish(settings.REDIS_CONN_ALARM['CHANNEL'], redis_publish_data)
            # REDIS_OBJ.publish(settings.REDIS_CONN_MERGE_ALARM['CHANNEL'], redis_publish_data)
    except Exception as err:
        logger.error(err)


def get_alarmstatus(ip, logger=None):
    """
    :param ip:
    :return: 通过维护配置表HostMaintenance，判断告警IP是否需要下发短信，True:告警，False:维护
    """
    logger.debug("get_alarmstatus: {}".format(ip))
    hostinfo_List = HostMaintenance.objects.filter(status=1)
    nowtime = int(time.time())  # 当前时间戳
    if hostinfo_List:
        logger.debug(hostinfo_List)
        assetinfo = HostMaintenance.objects.filter(status=1, assets__management_ip=ip).order_by("-id")
        logger.debug(assetinfo)
        if assetinfo:
            end = assetinfo[0].end
            endtime = int(time.mktime(end.timetuple()))  # datetime转化成时间戳
            if endtime - nowtime > 0:
                return False
            else:
                return True

        internetinfo = HostMaintenance.objects.filter(Q(status=1),
                                                      Q(internets__internet_ip=ip) | Q(internets__domain=ip)).order_by(
            "-id")
        logger.debug(internetinfo)
        if internetinfo:
            end = internetinfo[0].end
            endtime = int(time.mktime(end.timetuple()))  # datetime转化成时间戳
            if endtime - nowtime > 0:
                return False
            else:
                return True
        return True
    else:
        return True



def qzjalarm_contorl(logger, ip, item_id, err, typeid):
    """
    告警通知，redis发布和数据库记录
    """
    '''
    logger.debug("{}, {}, {}".format(ip, item_id, err))
    ch_status = int(GlobalConfs.objects.get(name='alarmstatus').val.strip())
    hk_status = int(GlobalConfs.objects.get(name='hkalarmstatus').val.strip())
    ds_status = int(GlobalConfs.objects.get(name='dsalarmstatus').val.strip())
    sql_status = int(GlobalConfs.objects.get(name='sqlalarmstatus').val.strip())
    oa_status = int(GlobalConfs.objects.get(name='accountstatus').val.strip())
    '''

    ch_status = ""
    hk_status = ""
    ds_status = ""
    sql_status = ""
    oa_status = ""


    logger.debug("告警路线123{}, {}".format(ds_status, typeid))
    if ch_status == 1 and typeid == 21:
        qzjalarm_contorl_sub(logger, ip, item_id, err, typeid)
    elif hk_status == 1 and typeid == 22:
        qzjalarm_contorl_sub(logger, ip, item_id, err, typeid)
    elif ds_status == 1 and typeid == 23:
        logger.debug("告警路线{}, {}".format(ds_status,typeid))
        qzjalarm_contorl_sub(logger, ip, item_id, err, typeid)
    elif sql_status == 1 and typeid == 24:
        qzjalarm_contorl_sub(logger, ip, item_id, err, typeid)
    elif oa_status == 1 and typeid == 25:
        qzjalarm_contorl_sub(logger, ip, item_id, err, typeid)
    else:
        logger.warn("全局配置表告警开关没有开启")


def qzjalarm_contorl_sub(logger, ip, item_id, err, typeid):
    global ip_monitorstatus
    try:
        iteminfo = Items.objects.get(id=item_id)
        desc = iteminfo.desc.strip()
        item_monitorstatus = iteminfo.monitorstatus  # 监控项开关
        if iteminfo.monitortype == 'report':
            cls_monitorstatus = 1
        else:
            cls_monitorstatus = iteminfo.servers.monitorstatus  # 监控服务开关
        client = iteminfo.clients  # 监控客户端IP和PORT
        personal = iteminfo.responsible
        logger.debug("监控项{}, 负责人{}".format(item_id, personal))
        assetinfo = Assets.objects.filter(management_ip=ip)
        if assetinfo:
            ip_monitorstatus = assetinfo[0].monitorstatus  # 资产表开关

        internetinfo = InternetMappings.objects.filter(Q(internet_ip=ip) | Q(domain=ip))
        if internetinfo:
            ip_monitorstatus = internetinfo[0].monitorstatus  # 域名表开关

        if personal:
            content = "[监控项ID:" + str(item_id) + "] - " + desc + err + ", 负责人:" + personal
        else:
            content = "[监控项ID:" + str(item_id) + "] - " + desc + err

        if int(item_monitorstatus) == 1 and int(ip_monitorstatus) == 1 and int(cls_monitorstatus) == 1:
            logger.debug("进入发送{}, {}, {}".format(ip, item_id, err))
            #根据有无负责人判断通知那批次人，有负责人就通知tcp那波人，没有通知QZJ那波人
            if personal:
                types = 'TCP'
            else:
                types = 'QZJ'
            warn_phone = WARN_USER['PHONE'][types]
            warn_weixin = WARN_USER['WEIXIN'][types]
            userlist = warn_phone.split('|')

            # 1.发送短信
            # for iphone in userlist:
            #     logger.debug("发送手机号{}, 内容{}".format(iphone, content))
            #     sendSMS(iphone, content)
            # 2.发送微信信息
            url = WEIXINAPI['URL']
            logger.debug("发送微信{},地址{}, 内容{}".format(warn_weixin, url, content))
            try:
                headers = {
                    "content-type": "application/json",
                }
                postdata = {"touser": warn_weixin,
                            "content": content,
                            }
                ret = requests.post(url, headers=headers, data=json.dumps(postdata), timeout=16, verify=False)
                logger.debug("返回结果{},地址{}, 发送内容{}".format(ret.text, url, json.dumps(postdata)))
            except Exception as err:
                return Exception(err)
    except Exception as err:
        logger.error(err)



