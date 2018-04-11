import redis
from multiprocessing import Process


def check_redis(logger, host, port, ret=None, passwd=None, socket_timeout=3):
    try:
        r = redis.StrictRedis(host=host, port=int(port), password=passwd, db=0,
                              socket_timeout=socket_timeout, charset='utf-8')
        info = r.info()

        # Server
        redis_version = info.get('redis_version', '')  # Redis服务器版本
        redis_git_sha1 = info.get('redis_git_sha1', '')  # Git SHA1
        redis_git_dirty = info.get('redis_git_dirty', '')  # Git dirty flag
        arch_bits = info.get('arch_bits', '')  # 架构（32 或 64 位）
        multiplexing_api = info.get('multiplexing_api', '')  # Redis 所使用的事件处理机制
        gcc_version = info.get('gcc_version', '')  # 编译 Redis 时所使用的 GCC 版本
        process_id = info.get('process_id', '')  # 服务器进程的 PID
        uptime_in_seconds = info.get('uptime_in_seconds', '')  # 自 Redis 服务器启动以来，经过的秒数
        uptime_in_days = info.get('uptime_in_days', '')  # 自 Redis 服务器启动以来，经过的天数
        lru_clock = info.get('lru_clock', '')  # 以分钟为单位进行自增的时钟，用于 LRU 管理
        os = info.get('os', '')  # Redis 服务器的宿主操作系统
        redis_mode = info.get('redis_mode', '')  # redis运行模式
        hz = info.get('hz', '')  # Redis调用内部函数来执行许多后台任务的频率为每秒10次
        run_id = info.get('run_id', '')  # Redis 服务器的随机标识符（用于 Sentinel 和集群）
        tcp_port = info.get('tcp_port', '')  # TCP/IP 监听端口

        # Clients
        connected_clients = info.get('connected_clients', '')  # 已连接客户端的数量（不包括通过从属服务器连接的客户端）
        client_longest_output_list = info.get('client_longest_output_list', '')  # 当前连接的客户端当中，最长的输出列表
        client_biggest_input_buf = info.get('client_biggest_input_buf', '')  # 当前连接的客户端当中，最大输入缓存
        blocked_clients = info.get('blocked_clients', '')  # 正在等待阻塞命令（BLPOP、BRPOP、BRPOPLPUSH）的客户端的数

        # Memory
        used_memory = info.get('used_memory', '')  # 由 Redis 分配器分配的内存总量，以字节（byte）为单位
        used_memory_human = info.get('used_memory_human', '')  # 以人类可读的格式返回 Redis 分配的内存总量
        used_memory_rss = info.get('used_memory_rss', '')  # 从操作系统的角度，返回 Redis 已分配的内存总量（俗称常驻集大小）。这个值和 top 、 ps 等命令的输出一致。
        used_memory_peak = info.get('used_memory_peak', '')  # Redis 的内存消耗峰值（以字节为单位）
        used_memory_peak_human = info.get('used_memory_peak_human', '')  # 以人类可读的格式返回 Redis 的内存消耗峰值
        used_memory_lua = info.get('used_memory_lua', '')  # Lua 引擎所使用的内存大小（以字节为单位）
        used_memory_lua_human = info.get('used_memory_lua_human', '')  # 以人类可读的格式返回 Lua 引擎所使用的内存
        maxmemory = info.get('maxmemory', '')  # Redis最大使用的内存 （以字节为单位）
        maxmemory_human = info.get('maxmemory', '')  # 以人类可读的格式返回 Redis最大使用的内存
        maxmemory_policy = info.get('maxmemory_policy', '')  # 设置过期Key
        mem_fragmentation_ratio = info.get('mem_fragmentation_ratio', '')  # used_memory_rss 和 used_memory 之间的比率
        mem_allocator = info.get('mem_allocator', '')  # 在编译时指定的， Redis 所使用的内存分配器。可以是 libc、jemalloc或者tcmalloc

        # Persistence  RDB 和 AOF 的相关信息
        loading = info.get('loading', '')  # 一个标志值，记录了服务器是否正在载入持久化文件
        rdb_changes_since_last_save = info.get('rdb_changes_since_last_save', '')  # 距离最后一次成功创建持久化文件之后，改变了多少个键值
        rdb_bgsave_in_progress = info.get('rdb_bgsave_in_progress', '')  # 一个标志值，记录服务器是否正在创建RDB文件
        rdb_last_save_time = info.get('rdb_last_save_time', '')  # 最近一次成功创建RDB文件的UNIX时间
        rdb_last_bgsave_status = info.get('rdb_last_bgsave_status', '')  # 一个标志值，记录了最后一次创建RDB文件的结果是成功还是失败
        rdb_last_bgsave_time_sec = info.get('rdb_last_bgsave_time_sec', '')  # 记录最后一次创建RDB文件耗费的秒数
        rdb_current_bgsave_time_sec = info.get('rdb_current_bgsave_time_sec',
                                               '')  # 如果服务器正在创建RDB文件，那么这个值记录的就是当前的创建RDB操作已经耗费了多长时间（单位为秒）
        aof_enabled = info.get('aof_enabled', '')  # 一个标志值，记录了AOF是否处于打开状态
        aof_rewrite_in_progress = info.get('aof_rewrite_in_progress', '')  # 一个标志值，记录了服务器是否正在创建AOF文件
        aof_rewrite_scheduled = info.get('aof_rewrite_scheduled', '')  # 一个标志值，记录了RDB文件创建完之后，是否需要执行预约的AOF重写操作
        aof_last_rewrite_time_sec = info.get('aof_last_rewrite_time_sec', '')  # 记录了最后一次AOF重写操作的耗时
        aof_current_rewrite_time_sec = info.get('aof_current_rewrite_time_sec',
                                                '')  # 如果服务器正在进行AOF重写操作，那么这个值记录的就是当前重写操作已经耗费的时间（单位是秒）
        aof_last_bgrewrite_status = info.get('aof_last_bgrewrite_status', '')  # 一个标志值，记录了最后一次重写AOF文件的结果是成功还是失败

        # Stats
        total_connections_received = info.get('total_connections_received', '')  # 服务器已经接受的连接请求数量
        total_commands_processed = info.get('total_commands_processed', '')  # 服务器已经执行的命令数量
        instantaneous_ops_per_sec = info.get('instantaneous_ops_per_sec', '')  # 服务器每秒中执行的命令数量
        rejected_connections = info.get('rejected_connections', '')  # 因为最大客户端数量限制而被拒绝的连接请求数量
        expired_keys = info.get('expired_keys', '')  # 因为过期而被自动删除的数据库键数量
        evicted_keys = info.get('evicted_keys', '')  # 因为最大内存容量限制而被驱逐（evict）的键数量
        keyspace_hits = info.get('keyspace_hits', '')  # 查找数据库键成功的次数
        keyspace_misses = info.get('keyspace_misses', '')  # 查找数据库键失败的次数
        pubsub_channels = info.get('pubsub_channels', '')  # 目前被订阅的频道数量
        pubsub_patterns = info.get('pubsub_patterns', '')  # 目前被订阅的模式数量
        latest_fork_usec = info.get('latest_fork_usec', '')  # 最近一次fork()操作耗费的时间(毫秒)

        # Replication
        role = info.get('role', '')  # 在主从复制中，充当的角色。如果没有主从复制，单点的，它充当的角色也是master
        connected_slaves = info.get('connected_slaves', '')  # 有多少个slave节点

        # CPU
        used_cpu_sys = info.get('used_cpu_sys', '')  # Redis服务器耗费的系统CPU
        used_cpu_user = info.get('used_cpu_user', '')  # Redis服务器耗费的用户CPU
        used_cpu_sys_children = info.get('used_cpu_sys_children',
                                         '')  # Redis后台进程耗费的系统CPU（后台包括RDB文件的消耗，master，slave同步产生的消耗等等）
        used_cpu_user_children = info.get('used_cpu_user_children', '')  # Redis后台进程耗费的用户CPU

        # replication
        if role == 'slave':
            # print info
            master_host = info.get('master_host', '')
            master_port = info.get('master_port', '')
            master_link_status = info.get('master_link_status', '')
            master_last_io_seconds_ago = info.get('master_last_io_seconds_ago', '')
            master_sync_in_progress = info.get('master_sync_in_progress', '')
            slave_priority = info.get('slave_priority', '')
            slave_read_only = info.get('slave_read_only', '')
        else:
            master_host = ''
            master_port = ''
            master_link_status = ''
            master_last_io_seconds_ago = ''
            master_sync_in_progress = ''
            slave_priority = ''
            slave_read_only = ''

        if not ret:
            return info
    except Exception as e:
        logger.error(e)


def main(servers_list):
    if servers_list:
        plist = []

        for row in servers_list:
            host = row[0]
            port = row[1]
            passwd = row[2]
            p = Process(target=check_redis, args=(host, port, passwd))
            plist.append(p)
            p.start()

        for p in plist:
            p.join()
