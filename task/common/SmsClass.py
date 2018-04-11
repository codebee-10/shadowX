import requests
import json


def sendSMS(mobile, content):
    """
    :param mobile:
    :param content:
    :return: 短信告警
    """
    headers = {"Content-Type": "application/json"}
    # url = "http://10.10.70.121:80/api/Message/SendMessageV3"  # Help/Api/POST-api-Message-SendMessageV3
    # url = "http://10.10.70.121:80/api/Message/SendServiceSms_Em"
    url = "http://10.10.70.121:80/api/Message/SendMoniterSms"
    postdata = {"sysFlag": "monitoring",
                "IsBussniss": "1",
                "phoneNumbers": mobile,
                "content": content,
                }
    try:
        ret = requests.post(url, headers=headers, data=json.dumps(postdata), timeout=16, verify=False)
        return ret.text
    except Exception as err:
        print(err)
        return False


if __name__ == '__main__':
    sendSMS('输入手机号', '输入内容')
