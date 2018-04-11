import pymongo
import bson
from pymongo import MongoClient


def check_mongodb(logger, host, port, user, passwd):
    try:
        uri = 'mongodb://' + user + ':' + passwd + '@' + host + ':' + port
        client = MongoClient(uri)
        admindb = client['admin']
        serverStatus = admindb.command(bson.son.SON([('serverStatus', 1)]))

        ok = int(serverStatus.get('ok', 0))
        if ok:
            version = serverStatus['version']  # 版本
            uptime = serverStatus['uptime']  # mongod服务启动后到现在已经存活的秒数
            uptimeEstimate = serverStatus['uptimeEstimate']  # mongod内部计算出来的存活秒数
            pid = serverStatus['pid']  # mongod的pid进程号
            process = serverStatus['process']  # mongodb进程，主要有mongod和mongos(分片集群中)两种

        # 连接数信息
        if serverStatus.get('connections', ''):
            connections_current = serverStatus['connections'].get('current', '')  # 当前连接数
            connections_available = serverStatus['connections'].get('available', '')  # 可用连接数
            connections_totalCreated = serverStatus['connections'].get('totalCreated', '')  # 截止目前为止总共创建的连接数

        # 全局锁信息
        if serverStatus.get('globalLock', ''):
            if serverStatus['globalLock'].get('activeClients', ''):
                globalLock_activeClients = serverStatus['globalLock']['activeClients'].get('total', '')  # 当前活跃客户端的个数

            if serverStatus['globalLock'].get('currentQueue', ''):
                globalLock_currentQueue = serverStatus['globalLock']['currentQueue'].get('total', '')  # 当前的全局锁等待锁等待的个数

        # 额外信息
        if serverStatus.get('extra_info', ''):
            extra_info_note = serverStatus['extra_info'].get('note', '')  # 表示当前这个extra_info的显示信息依赖于底层系统
            extra_info_page_faults = serverStatus['extra_info'].get('page_faults',
                                                                    '')  # 数据库访问数据时发现数据不在内存时的页面数量，当数据库性能很差或者数据量极大时，这个值会显著上升

        # 索引统计信息
        if serverStatus.get('indexCounters', ''):
            indexCounters_accesses = serverStatus['indexCounters'].get('accesses',
                                                                       '')  # 索引访问次数，值越大表示你的索引总体而言建得越好，如果值增长很慢，表示系统建的索引有问题
            indexCounters_hits = serverStatus['indexCounters'].get('hits', '')  # 索引命中次数，值越大表示mogond越好地利用了索引
            indexCounters_misses = serverStatus['indexCounters'].get('misses', '')  # 表示mongod试图使用索引时发现其不在内存的次数，越小越好
            indexCounters_resets = serverStatus['indexCounters'].get('resets', '')  # 计数器重置的次数
            indexCounters_missRatio = serverStatus['indexCounters'].get('missRatio', '')  # 丢失率，即misses除以hits的值

        # 后台刷新信息
        if serverStatus.get('backgroundFlushing', ''):
            backgroundFlushing_flushes = serverStatus['backgroundFlushing'].get('flushes', '')  # 数据库刷新写操作到磁盘的总次数，会逐渐增长
            backgroundFlushing_total_ms = serverStatus['backgroundFlushing'].get('total_ms', '')  # 数据到磁盘消耗的总时间，单位ms
            backgroundFlushing_average_ms = serverStatus['backgroundFlushing'].get('average_ms',
                                                                                   '')  # 上述两值的比例，表示每次写磁盘的平均时间
            backgroundFlushing_last_ms = serverStatus['backgroundFlushing'].get('last_ms',
                                                                                '')  # 当前最后一次写磁盘花去的时间，ms，结合上个平均值可观察到mongd总体写性能和当前写性能
            backgroundFlushing_last_finished = serverStatus['backgroundFlushing'].get('last_finished', '')  # 最后一次写完成的时间

        # 游标信息
        if serverStatus.get('cursors', ''):
            cursors_totalOpen = serverStatus['cursors'].get('totalOpen', '')  # mongodb当前为客户端维护的游标个数
            cursors_timeOut = serverStatus['cursors'].get('timeOut',
                                                          '')  # 从mongod启动以来的游标超时个数，如果这个值很大或者一直在增长，可能显示当前应用程序有错误

        # 持久化
        if serverStatus.get('dur', ''):
            dur_commits = serverStatus['dur'].get('commits', '')  # 上次分组提交间隔之后，写入journal的commit的次数
            dur_journaledMB = serverStatus['dur'].get('journaledMB', '')  # 上次分组提交间隔之后，写入journal的大小，单位M
            dur_writeToDataFilesMB = serverStatus['dur'].get('writeToDataFilesMB', '')  # 上次分组提交间隔之后，从journal写入到数据文件的大小
            dur_compression = serverStatus['dur'].get('compression', '')  # journal日志的压缩率
            dur_commitsInWriteLock = serverStatus['dur'].get('commitsInWriteLock', '')  # 提交的时候有写锁的次数，可以用该值判断当前系统的写压力
            dur_earlyCommits = serverStatus['dur'].get('earlyCommits',
                                                       '')  # 在分组提交间隔前，请求commit的次数。用这个值可以判断分组提交间隔，即 journal group commitinterval设置得是否合理
            if serverStatus['dur'].get('timeMs'):
                dur_timeMs_dt = serverStatus['dur']['timeMs'].get('dt', '')  # 收集数据所花的时间
                dur_timeMs_prepLogBuffer = serverStatus['dur']['timeMs'].get('prepLogBuffer',
                                                                             '')  # 准备写入journal所花的时间，单位ms，该值越小表示journal性能越好
                dur_timeMs_writeToJournal = serverStatus['dur']['timeMs'].get('writeToJournal',
                                                                              '')  # 真正写入journal所花的时间，单位ms，该值和文件系统和硬件设备有关
                dur_timeMs_writeToDataFiles = serverStatus['dur']['timeMs'].get('writeToDataFiles',
                                                                                '')  # 从journal写入到数据文件所花的时间，单位ms
                dur_timeMs_remapPrivateView = serverStatus['dur']['timeMs'].get('remapPrivateView',
                                                                                '')  # 重新映射内存所花的时间，单位ms，值越小表示journal性能越好

        # 内存信息
        if serverStatus.get('mem', ''):
            mem_bits = serverStatus['mem'].get('bits', '')  # 操作系统位数
            mem_resident = serverStatus['mem'].get('resident', '')  # 物理内存消耗，单位M
            mem_virtual = serverStatus['mem'].get('virtual', '')  # //虚拟内存消耗
            mem_supported = serverStatus['mem'].get('supported', '')  # true表示支持显示额外的内存信息
            mem_mapped = serverStatus['mem'].get('mapped', '')  # 映射内存
            mem_mappedWithJournal = serverStatus['mem'].get('mappedWithJournal', '')  # 除了映射内存外还包括journal日志消耗的映射内存

        # 网络信息
        if serverStatus.get('network'):
            network_bytesIn_persecond = int(serverStatus['network'].get('bytesIn'))  # 数据库接收到的网络传输字节数
            network_bytesOut_persecond = int(serverStatus['network'].get('bytesOut'))  # 从数据库发送出去的网络传输字节数
            network_numRequests_persecond = int(serverStatus['network'].get('numRequests'))  # 网络输入输出请求总次数

        # 操作计数器
        if serverStatus.get('opcounters', ''):
            opcounters_insert_persecond = int(serverStatus['opcounters'].get('insert'))  # /mongod最近一次启动后的insert次数
            opcounters_query_persecond = int(serverStatus['opcounters'].get('query'))  # mongod最近一次启动后的query次数
            opcounters_update_persecond = int(serverStatus['opcounters'].get('update'))  # mongod最近一次启动后的update次数
            opcounters_delete_persecond = int(serverStatus['opcounters'].get('delete'))  # mongod最近一次启动后的delete次数
            opcounters_command_persecond = int(
                serverStatus['opcounters'].get('command'))  # mongod最近一次启动后的执行command命令的次数

        # 断言
        if serverStatus.get('asserts', ''):
            asserts_regular = serverStatus['asserts'].get('regular', '')  # 服务启动后正常的asserts错误个数
            asserts_warning = serverStatus['asserts'].get('warning', '')  # 服务启动后的warning个数
            asserts_msg = serverStatus['asserts'].get('msg', '')  # 服务启动后的message assert个数
            asserts_user = serverStatus['asserts'].get('user', '')  # 服务启动后的user asserts个数
            asserts_rollovers = serverStatus['asserts'].get('rollovers', '')  # 服务启动后的重置次数

        # 记录状态信息
        if serverStatus.get('recordStats', ''):
            recordStats_accessesNotInMemory = serverStatus['recordStats'].get('accessesNotInMemory',
                                                                              '')  # 访问数据时发现不在内存的总次数
            recordStats_pageFaultExceptionsThrown = serverStatus['recordStats'].get(
                'pageFaultExceptionsThrown')  # 由于页面错误而抛出异常的总次数

        # repl复制集信息
        if serverStatus.get('repl', ''):
            if serverStatus['repl'].get('secondary', '') == True:
                setName = serverStatus['repl'].get('setName', '')
                repl_role = 'secondary'
            if serverStatus['repl'].get('ismaster', '') == True:
                setName = serverStatus['repl'].get('setName', '')
                repl_role = 'master'

    except Exception as e:
        logger_msg = "check mongodb %s:%s : %s" % (host, port, e)
        logger.warning(logger_msg)
