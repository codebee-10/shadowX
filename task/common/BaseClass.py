import time
import datetime


def get_time():
    """
    :return: 返回小时、分钟、秒
    """
    h = time.strftime('%H')
    m = time.strftime('%M')
    s = time.strftime('%S')
    return h, m, s


def get_day():
    """
    :return: 获取月日
    """
    m = time.strftime('%m')
    d = time.strftime('%d')
    return m, d


def get_ymd():
    """
    :return: 获取年月日
    """
    y = time.strftime('%Y')
    m = time.strftime('%m')
    d = time.strftime('%d')
    return y, m, d


def get_specify_ymd(num=0, is_split=0):
    """
    :param num: num负数为今天之前的日期，num正数为今天之后的日期, num为0是今天日期
    :param is_split: 返回年月日是否拆分
    :return: 获取指定的年月日
    """
    now_time = datetime.datetime.now()
    yes_time = now_time + datetime.timedelta(days=num)
    if is_split:
        return yes_time.strftime('%Y'), yes_time.strftime('%m'), yes_time.strftime('%d')
    else:
        return yes_time.strftime('%Y%m%d')


class CalcDate(object):

    def get_average(self, data_set):
        """
        calc the avg value of data set
        :param data_set:
        :return:
        """
        return sum(data_set) / len(data_set)

    def get_max(self, data_set):
        """
        calc the max value of the data set
        :param data_set:
        :return:
        """
        return max(data_set)

    def get_min(self, data_set):
        """
        calc the minimum value of the data set
        :param data_set:
        :return:
        """
        return min(data_set)

    def get_mid(self, data_set):
        """
        calc the mid value of the data set
        :param data_set:
        :return:
        """
        data_set.sort()
        return data_set[int(len(data_set)/2)]
