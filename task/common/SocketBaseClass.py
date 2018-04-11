import socket
import re

from .SingletonClass import SingletonClass


class BaseSocket(SingletonClass):
    """
    connect: socket连接建立
    close: socket连接断开
    """

    def __init__(self, logger, ip, port):
        self.logger = logger
        self.ip = ip
        self.port = port
        self.sock = None

    def connect(self, timeout=5):
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.settimeout(timeout)
            self.sock.connect((self.ip, self.port))
            addr = self.sock.getsockname()
            self.logger.info("Client端主机:%s, 端口:%s" % (addr[0], addr[1]))
            return None, None
        except socket.error as e:
            self.logger.error(e)
            rule = re.compile(r'[^a-zA-z0-9]')
            desc = rule.sub(' ', str(e))
            message = '[TCP连接失败]IP地址:%s, 端口:%s, 错误内容:%s' % (self.ip, self.port, desc)
            self.logger.error(message)
            return False, message

    def close(self):
        self.sock.close()

    def __del__(self):
        self.close()
