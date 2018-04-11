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
        self.serversocket.setblocking(0)

    def run(self):
        response = b'connecting success: status: 200 \n'
        response += b'haody,client !'
        epoll = select.epoll()
        epoll.register(self.serversocket.fileno(), select.EPOLLIN)

        try:
            connections = {}
            requests = {}
            responses = {}
            endflag = '\n\r\n'

            while True:
                events = epoll.poll(1)
                for fileno, event in events:
                    if fileno == self.serversocket.fileno():
                        connection, address = self.serversocket.accept()
                        connection.setblocking(0)
                        epoll.register(connection.fileno(), select.EPOLLIN)
                        connections[connection.fileno()] = connection
                        requests[connection.fileno()] = ''
                        responses[connection.fileno()] = response
                        print("1")

                    elif event & select.EPOLLIN:
                        try:
                            requests[fileno] = connections[fileno].recv(1024)
                            if len(str(requests[fileno].decode())) == 0:
                                connections[fileno].shutdown(socket.SHUT_RDWR)
                                break
                            else:
                                print("2")
                                print("2 | ------ : " + str(requests[fileno].decode()) + "\n")
                                byteswritten = connections[fileno].send(responses[fileno])

                            if endflag in requests[fileno]:
                                epoll.modify(fileno, select.EPOLLOUT)
                                connections[fileno].setsockopt(socket.IPPROTO_TCP, socket.TCP_CORK, 1)
                                print('-' * 40 + '\n' + requests[fileno].decode()[:-2])
                        except:
                            print("3")
                            continue

                    elif event & select.EPOLLOUT:
                        byteswritten = connections[fileno].send(responses[fileno])
                        responses[fileno] = responses[fileno][byteswritten:]
                        if len(responses[fileno]) == 0:
                            connections[fileno].setsockopt(socket.IPPROTO_TCP, socket.TCP_CORK, 0)
                            epoll.modify(fileno, 0)
                            connections[fileno].shutdown(socket.SHUT_RDWR)

                    elif event & select.EPOLLHUP:
                        epoll.unregister(fileno)
                        connections[fileno].close()
                        del connections[fileno]

        except:
            print("server excepted ...")
            epoll.unregister(self.serversocket.fileno())
            self.run()

        finally:
            print("server closed ...")


if __name__=="__main__":
    emsc = emsc_server()
    emsc.run()