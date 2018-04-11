#!/usr/bin/env python
# -*- coding: utf-8 -*-
import socket
import time


class emsc_client:
    def __init__(self):
        self.host = "10.10.83.174"
        self.port = 5000
        self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


    def run(self):

        try:
            self.conn.connect((self.host, self.port))
            while True:
                self.conn.send(("来自客户端发送的数据 : " + str(time.time())).encode())
                data = self.conn.recv(1024).decode()
                print("来自服务端数据 :" + data + "|" + str(time.time()))
                time.sleep(100)
        except:
            print("服务器连接异常,尝试重新连接 (5s) ...")
            self.conn.close()
            time.sleep(5) # 断开连接后,每5s重新连接一次
            emsc_client().run()

        finally:
            print("客户端已关闭 ...")


if __name__=="__main__":
    emsc = emsc_client()
    emsc.run()