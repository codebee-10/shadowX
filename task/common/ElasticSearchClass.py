"""
pip install elasticsearch
"""
import requests
import base64
import json
import datetime
from elasticsearch import Elasticsearch

from config.shadowx_config import ES_CONN


class ElasticSearchClass(object):

    def __init__(self, host, port, user, passwrod):
        self.host = host
        self.port = port
        self.user = user
        self.password = passwrod
        self.connect()

    def connect(self):
        self.es = Elasticsearch(hosts=[{'host': self.host, 'port': self.port}],
                                http_auth=(self.user, self.password))

    def count(self, indexname):
        """
        :param indexname:
        :return: 统计index总数
        """
        return self.es.count(index=indexname)

    def delete(self, indexname, doc_type, id):
        """
        :param indexname:
        :param doc_type:
        :param id:
        :return: 删除index中具体的一条
        """
        self.es.delete(index=indexname, doc_type=doc_type, id=id)

    def get(self, indexname, id):
        return self.es.get(index=indexname, id=id)

    def search(self, indexname, size=10):
        try:
            return self.es.search(index=indexname, size=size, sort="@timestamp:desc")
        except Exception as err:
            print(err)


class RequestsElasticSearchClass(object):

    def __init__(self, host, port, user=None, passwrod=None, logger=None):
        self.logger = logger
        self.url = 'http://' + host + ':' + str(port)
        self.headers = {"User-Agent": "shhnwangjian",
                        "Content-Type": "application/json"}
        if user:
            basicpwd = base64.b64encode((user + ':' + passwrod).encode('UTF-8'))
            self.headers["Authorization"] = "Basic {}".format(basicpwd.decode('utf-8'))

    def search_size(self, indexname, size=10):
        try:
            gettdata = {"sort": "@timestamp:desc",
                        "size": size}
            url = self.url + '/' + indexname + '/_search'
            ret = requests.get(url, headers=self.headers, timeout=10, params=gettdata)
            return ret.text
        except Exception as err:
            self.logger.error(err)

    def search_query(self, indexname, hostip, timestamp, size):
        """
        :param indexname:
        :param hostip:
        :return: 根据IP和时间范围查询结果，时间为近一小时，查出500条
        内置的now表示当前，然后用-1d/h/m/s来往前推
        https://www.elastic.co/guide/en/elasticsearch/reference/current/query-filter-context.html
        """
        try:
            postdata = {
                        "query": {
                            "bool": {
                                "must": {"match": {"hostip": hostip}},
                                "filter": [{"range": {"@timestamp": {"from": "now-{}".format(timestamp), "to": "now"}}}]
                                }
                            },
                        "size": size,
                        "sort": [{"@timestamp": "desc"}]
                        }
            url = self.url + '/' + indexname + '/_search'
            ret = requests.post(url, headers=self.headers, timeout=10, data=json.dumps(postdata))
            return ret.text
        except Exception as err:
            self.logger.error(err)

    def delete_index(self, indexname):
        """
        :param indexname: 索引文件名
        :return: 删除指定索引文件名
        """
        try:
            url = self.url + '/' + indexname
            ret = requests.delete(url, headers=self.headers, timeout=10)
            return ret.text
        except Exception as err:
            self.logger.error(err)


if __name__ == '__main__':
    # obj = ElasticSearchClass('10.207.30.11')
    # print obj.count('a_crm_20170224')
    # esobj = ElasticSearchClass('10.10.83.163', 9200, 'wangjian', 'qwerasdf')
    # print(esobj.count('redis_log-2017.07.13'))
    # print(esobj.delete('redis_log-2017.07.13', 'redis-log', 'AV053Wz7x9Vb8C7N-3X8'))
    # print(esobj.search('redis_log-2017.07.13', size=20))
    err_list = ["Cannot allocate memory", "error", "ERROR", "ERR", "err", "max number of clients",
                "Background saving terminated with success"]
    requests_esobj = RequestsElasticSearchClass(ES_CONN['IP'], ES_CONN['PORT'],
                                                ES_CONN['USERNAME'], ES_CONN['PASSWORD'])
    # requests_esobj.search_size('redis_log-2017.07.13', size=5)
    es_data = requests_esobj.search_query('redis_log-2017.07.25', '10.10.83.162')
    es_data_json = json.loads(es_data)
    if es_data_json.get("hits"):
        for line_redis_log in es_data_json["hits"]["hits"]:
            for err_info in err_list:
                if err_info in line_redis_log['_source']['message']:
                    print(line_redis_log['_source']['message'])
