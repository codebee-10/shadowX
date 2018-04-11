from functools import wraps
import time

from monitor.common.RedisAlarmPublish import alarm_contorl, qzjalarm_contorl


class MyError(Exception):

    def __init__(self, *args, **kwargs):
        self.value_list = args
        self.value_dict = kwargs

    def ret_list(self):
        return self.value_list

    def ret_dict(self):
        return self.value_dict


def retry(MyException, logger, tries=1, delay=5, alarm=5, total=7, way=2):
    """
    :param MyException: 告警内容
    :param tries: 告警重试初始值
    :param delay: 告警重试间隔
    :param alarm: 触发告警次数
    :param total: 告警重试最大次数
    :param way: 检测方式
    """
    def deco_retry(f):
        @wraps(f)
        def f_retry(*args, **kwargs):
            mtries, mdelay, mtotal, malarm, mway = tries, delay, total, alarm, way
            while mtries < mtotal:
                try:
                    return f(*args, **kwargs)
                except MyException as err:
                    ip, item_id, err, typeid = err.ret_list()
                    if mway == 1:  # 手动检测
                        if mtries < malarm:
                            logger.error("重试次数:%s, 重试地址:%s, 错误内容:%s" % (mtries, ip, err))
                            mtries += 1
                            time.sleep(mdelay)
                        elif mtries >= malarm:
                            return err

                    if mway == 2:  # 自动检测
                        if mtries < malarm:
                            logger.error("重试次数:%s, 重试地址:%s, 错误内容:%s" % (mtries, ip, err))
                            mtries += 1
                            time.sleep(mdelay)
                        elif malarm <= mtries <= malarm+1:
                            logger.error("[发送]重试次数:%s, 重试地址:%s, 错误内容:%s" % (mtries, ip, err))
                            alarm_contorl(logger, ip, item_id, err, typeid)
                            time.sleep(mdelay)
                            if mtries == malarm+1:
                                return False
                            mtries += 1
                        else:
                            mtries += 1
                            return False
        return f_retry
    return deco_retry



def qzjretry(MyException, logger, tries=1, delay=1, alarm=1, total=1, way=2):
    """
    :param MyException: 告警内容
    :param tries: 告警重试初始值
    :param delay: 告警重试间隔
    :param alarm: 触发告警次数
    :param total: 告警重试最大次数
    :param way: 检测方式
    """
    def deco_retry(f):
        @wraps(f)
        def f_retry(*args, **kwargs):
            logger.error("重试测试进入")
            mtries, mdelay, mtotal, malarm, mway = tries, delay, total, alarm, way
            logger.error("检测类型：%s,%s,%s"%(mway,mtries,mtotal))
            try:
                return f(*args, **kwargs)
            except MyException as err:
                ip, item_id, err, typeid = err.ret_list()
                if mway == 2:  # 自动检测
                    logger.error("[发送]重试次数:%s, 类型:%s, 错误内容:%s" % (mtries, typeid, err))
                    qzjalarm_contorl(logger, ip, item_id, err, typeid)
                    time.sleep(mdelay)
        return f_retry
    return deco_retry
