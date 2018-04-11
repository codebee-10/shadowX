try:
    import netsnmp
except Exception as err:
    print(err)
    from pysnmp.hlapi import *


class NetSnmpClass(object):
    """
    netsnmp
    """
    def __init__(self, version=1, destHost="localhost", community="public"):
        self.version = version
        self.destHost = destHost
        self.community = community

    def query(self, oid):
        """
        snmpwalk
        """
        try:
            result = netsnmp.snmpwalk(oid,
                                      Version=self.version,
                                      DestHost=self.destHost,
                                      Community=self.community)
        except Exception as err:
            print(err)
            result = None
        return result


class PySnmpClass(object):
    """
    pysnmp
    """
    def __init__(self, ip, port=161, community='public'):
        self.ip = ip
        self.port = port
        self.community = community

    def query(self, oid):
        iterator = getCmd(SnmpEngine(),
                          CommunityData(self.community),
                          UdpTransportTarget((self.ip, self.port)),
                          ContextData(),
                          ObjectType(ObjectIdentity('SNMPv2-MIB', oid, 0)))

        errorIndication, errorStatus, errorIndex, varBinds = next(iterator)

        if errorIndication:  # SNMP engine errors
            print(errorIndication)
        else:
            if errorStatus:  # SNMP agent errors
                print('%s at %s' % (errorStatus.prettyPrint(), varBinds[int(errorIndex) - 1] if errorIndex else '?'))
            else:
                return varBinds[0][1]
                # for varBind in varBinds:  # SNMP response contents
                #     print(' = '.join([x.prettyPrint() for x in varBind]))


def netsnmp_main():
    # sysDescr  CSICO-3560 系统信息
    # ifNumber  CSICO-3560 接口总数
    # ifTable  CSICO-3560  接口详细信息
    # system 查看系统信息
    # ifDescr 获取网卡信息
    # .1.3.6.1.4.1.9.9.13.1.3.1.3  CSICO-3560 温度
    # .1.3.6.1.4.1.9.9.13.1.4.1.3  CSICO-3560 风扇状态
    # .1.3.6.1.4.1.9.9.13.1.5.1.3  CSICO-3560 电源状态
    # 1.3.6.1.4.1.9.9.48.1.1.1.1   CSICO-3560内存池名称，有多个，如Processor、I/O、Driver
    # 1.3.6.1.4.1.9.9.48.1.1.1.5   CSICO-3560内存池使用
    # 1.3.6.1.4.1.9.9.48.1.1.1.6   CSICO-3560内存池空闲，内存池总大小=使用+空闲
    # 1.3.6.1.4.1.9.9.109.1.1.1.1.6  CSICO-3560在最后五秒时间的整体CPU利用率
    # 1.3.6.1.4.1.9.9.109.1.1.1.1.7  CSICO-3560在最后一分钟期限的整体CPU利用率
    # 1.3.6.1.4.1.9.9.109.1.1.1.1.8  CSICO-3560在最后五分钟时间的整体CPU利用率
    # print SnmpClass(oid=".1.3.6.1.4.1.9.9.13.1.3.1.3", destHost="10.10.200.1")()[0]
    snmp_obj = NetSnmpClass(destHost="10.50.151.1", community="dongcai")
    print(snmp_obj.query('sysDescr'))


def pysnmp_main():
    snmp_obj = PySnmpClass("10.50.151.1", community="dongcai")
    print(snmp_obj.query('sysDescr'))


if __name__ == '__main__':
    pysnmp_main()
