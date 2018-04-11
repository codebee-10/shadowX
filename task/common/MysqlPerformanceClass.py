# -*- coding: utf-8 -*-

from task.common.MysqlConn import Mysql


def get_mysql_status(mysql_obj):
    """
    获取MySQL运行状态，生成字典
    """
    mysql_obj.execute_sql('show global status;')
    data_list = mysql_obj.fetchall
    data_dict = {}
    for item in data_list:
        data_dict[item[0]] = item[1]
    return data_dict


def get_mysql_variables(mysql_obj):
    """
    获取系统变量，生成字典
    """
    mysql_obj.execute_sql('show global variables;')
    data_list = mysql_obj.fetchall
    data_dict = {}
    for item in data_list:
        data_dict[item[0]] = item[1]
    return data_dict


def check_mysql():
    mysql_obj = Mysql('10.10.83.162', 3306, 'root', 'bc444a35b5a5bed6597ec28a83f33d13', 'eastmoney')
    mysql_variables = get_mysql_variables(mysql_obj)
    mysql_status = get_mysql_status(mysql_obj)

    version = mysql_variables.get('version', '')
    innodb_version = mysql_variables.get('innodb_version', '')
    connections = int(mysql_status.get('Connections', 0))  # 试图连接到(不管是否成功)MySQL服务器的连接数
    bytes_received = int(mysql_status.get('Bytes_received', 0)) / 1024  # 从所有客户端接收到的字节数
    bytes_sent = int(mysql_status.get('Bytes_sent', 0)) / 1024  # 发送给所有客户端的字节数

    # 最大连接数
    max_used_connections = int(mysql_status.get('Max_used_connections', 0))  # 服务器连接在某个时间段是否有尖峰
    max_connections = int(mysql_variables.get('max_connections', 0))

    # TPS
    com_commit = int(mysql_status.get('Com_commit', 0))
    com_rollback = int(mysql_status.get('Com_rollback', 0))
    uptime = int(mysql_status.get('Uptime', 0))  # 服务器已经运行的时间（以秒为单位）
    TPS = round(float(com_commit + com_rollback) / uptime, 3)

    # QPS计算 针对MyISAM引擎为主的DB
    questions = int(mysql_status.get('Questions', ''))  # 已经发送给服务器的查询的个数
    MyISAM_QPS = round(float(questions) / uptime, 3)

    # QPS计算 针对InnnoDB引擎为主的DB
    com_update = int(mysql_status.get('Com_update', 0))
    com_insert = int(mysql_status.get('Com_insert', 0))
    com_select = int(mysql_status.get('Com_select', 0))
    com_delete = int(mysql_status.get('Com_delete', 0))
    InnnoDB_QPS = round(float(com_update+com_insert+com_delete+com_select) / uptime, 3)

    # 线程缓存命中率
    threads_cached = int(mysql_status.get('Threads_cached', 0))  # 当前此时此刻线程缓存中有多少空闲线程
    threads_connected = int(mysql_status.get('Threads_connected', 0))  # 当前已建立连接的数量，因为一个连接就需要一个线程，所以也可以看成当前被使用的线程数
    threads_created = int(mysql_status.get('Threads_created', 0))  # 从最近一次服务启动，已创建线程的数量
    threads_running = int(mysql_status.get('Threads_running', 0))  # 当前激活的（非睡眠状态）线程数
    Thread_cache_hits = round((1 - float(threads_created) / connections) * 100, 3)

    # Innodb 缓存命中率
    innodb_buffer_pool_read_requests = int(mysql_status.get('Innodb_buffer_pool_read_requests', 0))  # 从缓冲池中读取的次数
    innodb_buffer_pool_read_ahead = int(mysql_status.get('Innodb_buffer_pool_read_ahead', 0))  # 预读的页数
    innodb_buffer_pool_reads = int(mysql_status.get('Innodb_buffer_pool_reads', 0))  # 从物理磁盘读取的页数
    innodb_cache_hits = round(float(innodb_buffer_pool_read_requests) / (innodb_buffer_pool_read_requests + innodb_buffer_pool_read_ahead + innodb_buffer_pool_reads), 3)

    # 锁表信息
    table_locks_waited = int(mysql_status.get('Table_locks_waited', 0))
    table_locks_immediate = int(mysql_status.get('Table_locks_immediate', 0))
    table_lock_hits = round(float(table_locks_waited) / table_locks_immediate, 3)

    # MyISAM Key Buffer命中率和缓冲区使用率
    key_read_requests = int(mysql_status.get('Key_read_requests', 0))  # 从缓存读键的数据块的请求数
    key_write_requests = int(mysql_status.get('Key_write_requests', 0))  # 将键的数据块写入缓存的请求数
    key_reads = int(mysql_status.get('Key_reads', 0))  # 从硬盘读取键的数据块的次数
    key_writes = int(mysql_status.get('Key_writes', 0))  # 向硬盘写入将键的数据块的物理写操作的次数
    key_blocks_unused = int(mysql_status.get('Key_blocks_unused', 0))  # 键缓存内未使用的块数量
    key_cache_block_size = int(mysql_variables.get('key_cache_block_size', 0))
    key_buffer_size = int(mysql_variables.get('key_buffer_size', 0))
    buffer_hits = round((1 - float(key_blocks_unused*key_cache_block_size)/key_buffer_size) * 100, 3)
    key_buffer_read_hits = round((1 - float(key_reads)/key_read_requests) * 100, 3)
    key_buffer_write_hits = round((1 - float(key_writes) / key_write_requests) * 100, 3)

    print(MyISAM_QPS, InnnoDB_QPS, TPS, Thread_cache_hits, innodb_cache_hits, table_lock_hits, buffer_hits, \
        key_buffer_read_hits, key_buffer_write_hits)

if __name__ == '__main__':
    check_mysql()
