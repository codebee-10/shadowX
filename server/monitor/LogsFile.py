from logs import logger
from datetime import datetime


class LogsFile():
    def __init__(self):
        self.monitor_log_file = "monitor_"+datetime.now().strftime("%Y-%m-%d")+".log"
        self.redis_log_file = "monitor_"+datetime.now().strftime("%Y-%m-%d")+".log"

    def get_monitor_logs(self):
        monitor = logger.Logger(log_name='moniter', logger="logs/files/" + self.monitor_log_file).getlog()
        return monitor

    def get_monitor_redis(self):
        redis_log = logger.Logger(log_name='redis', logger="logs/files/" + self.redis_log_file).getlog()
        return redis_log