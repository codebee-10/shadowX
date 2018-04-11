import requests
import base64


class RabbitMQHttpAPIClass(object):

    def __init__(self, ip, port, username, password, method='http'):
        __basicpwd = base64.b64encode((username + ':' + password).encode('UTF-8'))
        self.headers = {"User-Agent": "wangjian",
                        "Content-Type": "application/json",
                        "Authorization": "Basic %s" % __basicpwd.decode('utf-8')}
        self.url = method + '://' + ip + ':' + str(port) + '/api/'

    def overview(self):
        url = self.url + 'overview'
        ret = requests.get(url, headers=self.headers, timeout=10)
        return ret.text

    def nodes(self):
        url = self.url + 'nodes'
        ret = requests.get(url, headers=self.headers, timeout=10)
        return ret.text

    def node(self, nodename):
        url = self.url + 'nodes/' + nodename
        ret = requests.get(url, headers=self.headers, timeout=10)
        return ret.text

    def extensions(self):
        url = self.url + 'extensions/'
        ret = requests.get(url, headers=self.headers, timeout=10)
        return ret.text

    def connections(self):
        url = self.url + 'connections/'
        ret = requests.get(url, headers=self.headers, timeout=10)
        return ret.text

    def channels(self):
        url = self.url + 'channels/'
        ret = requests.get(url, headers=self.headers, timeout=10)
        return ret.text

    def exchanges(self):
        url = self.url + 'exchanges/'
        ret = requests.get(url, headers=self.headers, timeout=10)
        return ret.text

    def queues(self):
        url = self.url + 'queues/'
        ret = requests.get(url, headers=self.headers, timeout=10)
        return ret.text

    def bindings(self):
        url = self.url + 'bindings/'
        ret = requests.get(url, headers=self.headers, timeout=10)
        return ret.text

    def vhosts(self):
        url = self.url + 'vhosts/'
        ret = requests.get(url, headers=self.headers, timeout=10)
        return ret.text

    def policies(self):
        url = self.url + 'policies/'
        ret = requests.get(url, headers=self.headers, timeout=10)
        return ret.text

    def queues_vhost(self, vhost):
        url = self.url + 'queues/' + vhost
        print(url)
        ret = requests.get(url, headers=self.headers, timeout=10)
        return ret.text

    def queues_vhost_name(self, name):
        url = self.url + 'queues/%2F/' + name
        ret = requests.get(url, headers=self.headers, timeout=10)
        return ret.text

    def delete_queue_message(self, name):
        url = self.url + 'queues/%2F/' + name + '/contents'
        ret = requests.delete(url, headers=self.headers, timeout=10)
        return ret.text


if __name__ == '__main__':
    import json
    obj = RabbitMQHttpAPIClass('139.196.136.241', 15672, 'guest', 'guest')
    print(obj.queues())
    for queue in json.loads(obj.queues()):
        print(queue['name'], queue.get('messages_ready', 0))
        # print(obj.queues_vhost(queue['vhost']))
        # print(obj.queues_vhost_name(queue['name']))
        print(obj.delete_queue_message(queue['name']))
