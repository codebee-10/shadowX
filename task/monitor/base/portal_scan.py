import requests
from requests.exceptions import ConnectTimeout, ConnectionError, ReadTimeout
from server.monitor import MessageTunnel, LogsFile
import json


def portal_scan(item_id, ip="", urls="", port="", method="", username="", password="", client="",
                logger=LogsFile.LogsFile().get_monitor_logs()):
    """
    run: 主运行方法
    http_access: 访问重要站点页面
    :param url:
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
    item_id = item_id
    ip = ip
    urls = urls
    port = port
    method = method
    username = username
    password = password
    client = client
    logger.debug('----------------------------------------------------------------\n')


    global url, err
    headers = {"content-type": "application/json",
               }
    try:
        url = urls
        '''
        postfix = Items.objects.get(id=self.item_id).dependent.strip()
        if postfix:
            url = self.method + '://' + self.ip + ':' + self.port + postfix
        else:
            url = self.method + '://' + self.ip + ':' + self.port
        '''

        logger.debug(url)
        ret = requests.get(url, headers=headers, timeout=16, verify=False)
        logger.debug("耗时:{}, 返回码:{}, cookie:{}"
                              .format(ret.elapsed.microseconds / 1000, ret.status_code, ret.cookies.items()))
        err = None
        if ret.status_code >= 400:
            err = '[访问异常]{}, 响应码:{}'.format(url, ret.status_code)
            raise Exception
    except ConnectTimeout as e:
        logger.error(e)
        err = "{},URL连接超时".format(url)
        #return json.dumps(err)
    except ConnectionError as e:
        logger.error(e)
        err = "{},URL连接地址异常".format(url)
        #return json.dumps(err)
    except ReadTimeout as e:
        logger.error(e)
        err = "{},URL连接地址异常, {}".format(url, e)
        #return json.dumps(err)
    except Exception as e:
        logger.error(e)
        if str(e):
            err = '[访问异常]{}'.format(url)
        logger.error(err)
        #return json.dumps(err)

    if err != None:
        print("error.....")
        print(err)
        MessageTunnel.MessageTunnel(item_id, ip, str(err), client).save_alarm_message()
        MessageTunnel.MessageTunnel(item_id, ip, str(err), client).send_message()