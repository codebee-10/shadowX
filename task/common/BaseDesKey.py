import pyDes
import random
import hashlib


class DES(object):
    """
    DES 加解密类，调用pyDes模块
    """

    def __init__(self, iv, key):
        self.iv = iv
        self.key = key

    def encrypt(self, data):
        k = pyDes.des(self.key, pyDes.CBC, self.iv, pad=None, padmode=pyDes.PAD_PKCS5)
        d = k.encrypt(data)
        return d

    def decrypt(self, data):
        k = pyDes.des(self.key, pyDes.CBC, self.iv, pad=None, padmode=pyDes.PAD_PKCS5)
        d = k.decrypt(data)
        return d


def random_key():
    """
    :return:DES随机秘钥（8位）
    """
    checkcode = ''
    for i in range(8):
        current = random.randrange(0, 8)
        if current != i:
            temp = chr(random.randint(65, 90))
        else:
            temp = random.randint(0, 9)
        checkcode += str(temp)
    return checkcode


def mycrc32(szString):
    """
    :param szString:
    :return: 校验码
    """
    import binascii
    return binascii.crc32(szString)
    # return '0x%x' % (binascii.crc32(v) & 0xffffffff)  # 取crc32的八位数据 %x返回16进制
    # m_pdwCrc32Table = [0 for x in range(0, 256)]
    # dwPolynomial = 0xEDB88320
    # dwCrc = 0
    # for i in range(0, 255):
    #     dwCrc = i
    #     for j in [8, 7, 6, 5, 4, 3, 2, 1]:
    #         if dwCrc & 1:
    #             dwCrc = (dwCrc >> 1) ^ dwPolynomial
    #         else:
    #             dwCrc >>= 1
    #     m_pdwCrc32Table[i] = dwCrc
    # dwCrc32 = 0xFFFFFFFFL
    # for i in szString:
    #     b = ord(i)
    #     dwCrc32 = ((dwCrc32) >> 8) ^ m_pdwCrc32Table[(b) ^ ((dwCrc32) & 0x000000FF)]
    # dwCrc32 = dwCrc32 ^ 0xFFFFFFFFL
    # return dwCrc32


def get_md5(val):
    """
    :param val: 加密内容
    :return: 返回十六进制数字字符串
    """
    m = hashlib.md5()
    m.update(val)
    return m.hexdigest()


if __name__ == '__main__':
    # obj = prpcrypt('8888888866666666')
    # print(obj.encrypt('root'))
    # print(obj.decrypt('bc444a35b5a5bed6597ec28a83f33d13'))
    print(mycrc32(b'd\x01\x00wangjian_QZJ\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00N\x01\x00\x00N\x01\x00\x00'))
