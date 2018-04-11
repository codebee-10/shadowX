# shadowX_Server

- Stable: V3.2.4
- Beta: V3.2.6
- Dispatch: V3.2.7

## Server端部署
1. 不同的机房进行单独部署Server
2. 修改配置为当前机房
3. 启动Beat 和 Worker

## 分布式
1. 运行run/master
2. 运行run/client连接到其他服务端master进行监控和任务分片处理
3. 去中心化，动态选将master

## 任务分片、定时器
1. 通过client轮循连接多个master，如master出现异常，client会将master中任务分配到其他master的任务队列中；
2. 定时器Beat通过最小堆算法排序任务执行时间序列；
3. 异步执行任务、动态导入监控项
