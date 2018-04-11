#!/usr/bin/env python
# -*- coding: utf-8 -*-
import socket
import select


class emsc_server:
    def __init__(self):
        self.serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.serversocket.bind(('0.0.0.0', 5000))
        self.serversocket.listen(1000)
        self.serversocket.setblocking(1)

    def run(self):
        response = "接收成功，返回数据: connecting status: 200 \n"
        response += "haody,client !"
        epoll = select.epoll()
        epoll.register(self.serversocket.fileno(), select.EPOLLIN)

        try:
            connections = {}
            requests = {}
            responses = {}
            endflag = '\n\r\n'

            while True:
                events = epoll.poll(1)
                for fid, event in events:
                    if fid == self.serversocket.fileno():
                        connection, address = self.serversocket.accept()
                        connection.setblocking(0)
                        epoll.register(connection.fileno(), select.EPOLLIN)
                        connections[connection.fileno()] = connection
                        requests[connection.fileno()] = ''
                        responses[connection.fileno()] = response.encode()
                        print(response.encode())

                    elif event & select.EPOLLIN:
                        try:
                            requests[fid] = connections[fid].recv(1024)
                            if len(str(requests[fid].decode())) == 0:
                                connections[fid].shutdown(socket.SHUT_RDWR)
                                break
                            else:
                                print("2 | ------ : " + str(requests[fid].decode()) + "\n")
                                byteswritten = connections[fid].send(responses[fid])

                            if endflag in requests[fid]:
                                epoll.modify(fid, select.EPOLLOUT)
                                connections[fid].setsockopt(socket.IPPROTO_TCP, socket.TCP_CORK, 1)
                                print('-' * 40 + '\n' + requests[fid].decode()[:-2])
                        except:
                            continue

                    elif event & select.EPOLLOUT:
                        byteswritten = connections[fid].send(responses[fid])
                        responses[fid] = responses[fid][byteswritten:]
                        if len(responses[fid]) == 0:
                            connections[fid].setsockopt(socket.IPPROTO_TCP, socket.TCP_CORK, 0)
                            epoll.modify(fid, 0)
                            connections[fid].shutdown(socket.SHUT_RDWR)

                    elif event & select.EPOLLHUP:
                        epoll.unregister(fid)
                        connections[fid].close()
                        del connections[fid]

        except:
            print("server excepted ...")
            epoll.unregister(self.serversocket.fileno())
            self.run()

        finally:
            print("server closed ...")


if __name__=="__main__":
    emsc = emsc_server()
    emsc.run()