"""
pip install influxdb
InfluxDB属于时序数据库，没有提供修改和删除数据的方法。
"""

from influxdb import InfluxDBClient


class InfluxDBBaseClass(object):

    def __init__(self, ip, port, username=None, password=None, timeout=10, dbname=None):
        self.ip = ip
        self.port = int(port)
        self.username = username
        self.password = password
        self.timeout = timeout
        self.dbname = dbname
        self.__connect()

    def __connect(self):
        self.client = InfluxDBClient(host=self.ip, port=self.port, username=self.username, password=self.password,
                                     timeout=self.timeout, database=self.dbname)

    @property
    def get_list_database(self):
        """
        :return: 显示所有数据库名称
        """
        return self.client.get_list_database()

    def create_database(self, dbname):
        """
        :param dbname: 数据库名称
        :return: 创建数据库
        """
        return self.client.create_database(dbname)

    def drop_database(self, dbname):
        """
        :param dbname: 数据库名称
        :return: 删除数据库
        """
        return self.client.drop_database(dbname)

    def get_list_table(self, dbname=None):
        """
        :param dbname: 数据库名称
        :return: 显示数据库中的表
        """
        if self.dbname:
            return self.client.query('show measurements;', database=self.dbname)
        else:
            return self.client.query('show measurements;', database=dbname)

    def delete_table(self, tablename, dbname=None):
        """
        :param dbname: 数据库名称
        :param tablename: 表名
        :return: 删除表
        """
        if self.dbname:
            return self.client.query('drop measurement %s;' % tablename, database=self.dbname)
        else:
            return self.client.query('drop measurement %s;' % tablename, database=dbname)

    def insert_data(self, json_body, dbname=None):
        """
        :param json_body: InfluxDB没有提供单独的建表语句，可以通过并添加数据的方式建表
        :param dbname: 数据库名称
        :return:  创建新表并添加数据
        样例数据：json_body = [
                                {
                                    "measurement": "cpu_load_short",
                                    "tags": {
                                        "host": "server01",
                                        "region": "us-west"
                                    },
                                    "time": "2009-11-10T23:00:00Z",
                                    "fields": {
                                        "Float_value": 0.64,
                                        "Int_value": 3,
                                        "String_value": "Text",
                                        "Bool_value": True
                                    }
                                }
                            ]
        """
        if self.dbname:
            return self.client.write_points(json_body, database=self.dbname)
        else:
            return self.client.write_points(json_body, database=dbname)

    def query_table(self, query_content, dbname=None):
        """
        :param query_content: 查询语句
        :param dbname: 数据库名称
        :return: 查询表中数据
        """
        if self.dbname:
            return self.client.query(query_content, database=self.dbname)
        else:
            return self.client.query(query_content, database=dbname)

    def delete_series(self, dbname=None, measurement=None, tags=None):
        """
        :param dbname: 数据库名称
        :param measurement: 表名
        :param tags: 索引
        :return: 删除series集合
        """
        if self.dbname:
            return self.client.delete_series(database=self.dbname, measurement=measurement, tags=tags)
        else:
            return self.client.delete_series(database=dbname, measurement=measurement, tags=tags)


if __name__ == '__main__':
    obj = InfluxDBBaseClass('10.200.20.133', 8086, 'admin', 'admin')
    json_body = [
        {
            "measurement": "redis",
            "tags": {
                "typeid": "sms"
            },
            # "time": "2017-05-12T22:00:00Z",
            "fields": {
                "score": 90
            }
        }
    ]
    print(obj.insert_data(json_body, 'shhnwangjian'))
    print(obj.query_table('select * from redis', 'shhnwangjian'))
    # print obj.query_table('show series from memory_value', 'collectd')
    # print obj.delete_series('collectd', 'memory_value')
    # print obj.query_table('show series from memory_value', 'collectd')
    # print obj.delete_table('students2', 'shhnwangjian')
    # print obj.get_list_table('shhnwangjian')
