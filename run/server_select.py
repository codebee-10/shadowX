#!/usr/bin/env python
# -*- coding: utf-8 -*-
import select
import socket
import queue
import time
import os


class emsc_select_server:
    def __init__(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setblocking(False)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_address = ('0.0.0.0', 5000)
        self.server.bind(self.server_address)
        self.server.listen(1000)
        self.inputs = [self.server]
        self.outputs = []
        self.message_queues = {}
        self.timeout = 20
    
    def run(self):
        response = "接收成功，返回数据: connecting status: 200 \n"
        response += "haody,client ! | "

        while self.inputs:
            print("waiting for next event")
            # timeout是超时，当前连接要是超过这个时间的话，就会kill
            readable, writable, exceptional = select.select(self.inputs, self.outputs, self.inputs, self.timeout)

            if not (readable or writable or exceptional):
                print("Time out ! ")
                break
            for ser in readable:
                if ser is self.server:
                    # 通过inputs查看是否有客户端来
                    connection, client_address = ser.accept()
                    print("connection from ", client_address)
                    connection.setblocking(0)
                    self.inputs.append(connection)
                    self.message_queues[connection] = queue.Queue()
                else:
                    data = ser.recv(1024)
                    if data:
                        print("收到数据 ", data.decode(), "\n来自:", ser.getpeername())
                        self.message_queues[ser].put(data)
                        # 添加通道
                        if ser not in self.outputs:
                            self.outputs.append(ser)
                    else:
                        print("closing", client_address)
                        if ser in self.outputs:
                            self.outputs.remove(ser)
                        self.inputs.remove(ser)
                        ser.close()
                        # 清除队列信息
                        del self.message_queues[ser]

            for ser in writable:
                try:
                    next_msg = self.message_queues[ser].get_nowait()
                except queue.Empty:
                    print(ser.getpeername(), 'queue empty')
                    self.outputs.remove(ser)
                else:
                    print("发送数据 ", str(response + next_msg.decode()), " to ", ser.getpeername(),"\n")
                    ser.send(response.encode()+next_msg)

            for ser in exceptional:
                print(" exception condition on ", ser.getpeername())
                # stop listening for input on the connection
                self.inputs.remove(ser)
                if ser in self.outputs:
                    self.outputs.remove(ser)
                ser.close()
                # 清除队列信息
                del self.message_queues[ser]


if __name__=="__main__":
    select_server = emsc_select_server()
    select_server.run()