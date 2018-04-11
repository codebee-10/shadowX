import requests


def phone(mobile, content):
    """
    :param mobile:
    :param content:
    :return: 电话告警
    """
    headers = {"Content-Type": "application/json"}
    mobile = '90' + mobile
    get_paras = "?phone=" + mobile + "&verifyCode=" + content
    url_headers = 'http://58.220.215.99:7080/AEPOBService/ob'
    url = url_headers + get_paras
    try:
        ret = requests.get(url, headers=headers, timeout=16, verify=False)
        print(ret.elapsed.microseconds / 1000, ret.status_code, ret.text)
    except Exception as err:
        print(err)
